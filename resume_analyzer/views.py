from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resume
from .parser import extract_text_from_file, extract_skills, extract_education, extract_experience_years, calculate_ats_score, get_resume_feedback
import openai
from django.conf import settings
import os

@login_required
def upload_resume(request):
    if request.method == 'POST':
        file = request.FILES.get('resume')
        if not file:
            messages.error(request, 'Please select a file to upload.')
            return redirect('upload_resume')

        allowed_types = ['.pdf', '.docx', '.txt']
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in allowed_types:
            messages.error(request, 'Please upload a PDF, DOCX, or TXT file.')
            return redirect('upload_resume')

        resume = Resume.objects.create(
            user=request.user,
            file=file,
            original_filename=file.name,
        )

        try:
            text = extract_text_from_file(resume.file.path)
            skills = extract_skills(text)
            education = extract_education(text)
            exp_years = extract_experience_years(text)
            ats_score = calculate_ats_score(text)
            feedback_data = get_resume_feedback(text, skills, ats_score)

            ai_feedback = ""
            if settings.OPENAI_API_KEY and text and len(text) > 100:
                try:
                    openai.api_key = settings.OPENAI_API_KEY
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{
                            "role": "system",
                            "content": "You are an expert resume reviewer and career coach."
                        }, {
                            "role": "user",
                            "content": f"Review this resume and provide specific, actionable feedback in 5 bullet points:\n\n{text[:2500]}"
                        }],
                        max_tokens=500,
                        temperature=0.6
                    )
                    ai_feedback = response.choices[0].message['content']
                except Exception as e:
                    ai_feedback = "AI feedback unavailable. Add your OpenAI API key for detailed AI analysis."

            resume.extracted_text = text[:5000]
            resume.skills_found = skills
            resume.education_level = education
            resume.experience_years = exp_years
            resume.ats_score = ats_score
            resume.feedback = str(feedback_data) + "\n\n" + ai_feedback
            resume.word_count = len(text.split())
            resume.save()

            messages.success(request, f'Resume analyzed successfully! ATS Score: {ats_score}/100')
            return redirect('resume_result', pk=resume.pk)

        except Exception as e:
            resume.ats_score = 0
            resume.feedback = f"Error analyzing resume: {str(e)}"
            resume.save()
            messages.warning(request, 'Resume uploaded but analysis encountered an issue.')
            return redirect('resume_result', pk=resume.pk)

    previous_resumes = Resume.objects.filter(user=request.user)[:5]
    return render(request, 'resume_analyzer/upload.html', {'previous_resumes': previous_resumes})

@login_required
def resume_result(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    import ast
    feedback_data = {'improvements': [], 'strengths': []}
    try:
        raw = resume.feedback
        if raw.startswith('{'):
            end = raw.find('\n\n')
            dict_str = raw[:end] if end > 0 else raw
            feedback_data = ast.literal_eval(dict_str)
            ai_feedback = raw[end+2:].strip() if end > 0 else ""
        else:
            ai_feedback = raw
    except:
        ai_feedback = resume.feedback

    return render(request, 'resume_analyzer/result.html', {
        'resume': resume,
        'feedback_data': feedback_data,
        'ai_feedback': ai_feedback,
    })

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume_analyzer/list.html', {'resumes': resumes})

@login_required
def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        if resume.file and os.path.exists(resume.file.path):
            os.remove(resume.file.path)
        resume.delete()
        messages.success(request, 'Resume deleted.')
    return redirect('resume_list')
