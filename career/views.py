from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Option, AssessmentResult, SkillGapAnalysis
from .ai_recommender import get_career_recommendations, get_ai_career_advice, analyze_skill_gap, CAREER_SKILLS
from resume_analyzer.models import Resume
from chatbot.models import ChatSession

@login_required
def dashboard(request):
    latest_result = AssessmentResult.objects.filter(user=request.user).first()
    latest_resume = Resume.objects.filter(user=request.user).first()
    latest_gap = SkillGapAnalysis.objects.filter(user=request.user).first()
    chat_count = ChatSession.objects.filter(user=request.user).count()

    stats = {
        'quiz_done': AssessmentResult.objects.filter(user=request.user).count(),
        'resumes': Resume.objects.filter(user=request.user).count(),
        'skill_analyses': SkillGapAnalysis.objects.filter(user=request.user).count(),
        'chat_sessions': chat_count,
    }

    all_careers = list(CAREER_SKILLS.keys())
    context = {
        'latest_result': latest_result,
        'latest_resume': latest_resume,
        'latest_gap': latest_gap,
        'stats': stats,
        'all_careers': all_careers,
    }
    return render(request, 'career/dashboard.html', context)

@login_required
def quiz_view(request):
    questions = Question.objects.prefetch_related('options').order_by('order')
    if not questions.exists():
        seed_questions()
        questions = Question.objects.prefetch_related('options').order_by('order')

    if request.method == 'POST':
        answers = {}
        scores = {"tech": 0, "data": 0, "creative": 0, "social": 0,
                  "business": 0, "science": 0, "security": 0, "cloud": 0}

        for question in questions:
            option_id = request.POST.get(f'q_{question.id}')
            if option_id:
                try:
                    option = Option.objects.get(id=option_id)
                    answers[str(question.id)] = option_id
                    for key, val in option.weight.items():
                        scores[key] = scores.get(key, 0) + val
                except Option.DoesNotExist:
                    pass

        recommended = get_career_recommendations(scores)
        ai_advice = get_ai_career_advice(request.user, scores, recommended)

        result = AssessmentResult.objects.create(
            user=request.user, answers=answers,
            scores=scores, recommended_careers=recommended, ai_advice=ai_advice
        )
        messages.success(request, 'Assessment complete! Here are your personalized results.')
        return redirect('quiz_result', pk=result.pk)

    categories = {}
    for q in questions:
        categories.setdefault(q.get_category_display(), []).append(q)

    return render(request, 'career/quiz.html', {'questions': questions, 'categories': categories, 'total': questions.count()})

@login_required
def quiz_result_view(request, pk):
    result = get_object_or_404(AssessmentResult, pk=pk, user=request.user)
    career_details = []
    for career in result.recommended_careers[:4]:
        info = CAREER_SKILLS.get(career, {})
        career_details.append({'name': career, **info})

    top_score = max(result.scores.values()) if result.scores else 1
    score_percentages = {k: round(v / top_score * 100) for k, v in result.scores.items()}

    return render(request, 'career/result.html', {
        'result': result,
        'career_details': career_details,
        'score_percentages': score_percentages,
    })

@login_required
def skill_gap_view(request):
    all_careers = list(CAREER_SKILLS.keys())
    analysis = None

    if request.method == 'POST':
        target_career = request.POST.get('target_career')
        user_skills = request.POST.get('user_skills', request.user.current_skills or '')

        if target_career:
            analysis = analyze_skill_gap(user_skills, target_career)
            SkillGapAnalysis.objects.create(
                user=request.user,
                target_career=target_career,
                matched_skills=analysis['matched_skills'],
                missing_skills=analysis['missing_skills'],
                match_percentage=analysis['match_percentage'],
                courses_suggested=[c['name'] for c in analysis['courses_suggested']],
            )

    history = SkillGapAnalysis.objects.filter(user=request.user)[:5]
    return render(request, 'career/skill_gap.html', {
        'all_careers': all_careers,
        'analysis': analysis,
        'history': history,
        'user_skills': request.user.current_skills or '',
    })

def seed_questions():
    questions_data = [
        {"text": "I enjoy solving complex logical problems and puzzles", "category": "interest", "order": 1,
         "options": [("Strongly Agree", {"tech": 3, "data": 3, "science": 2}),
                     ("Agree", {"tech": 2, "data": 2, "science": 1}),
                     ("Neutral", {"business": 1}),
                     ("Disagree", {"creative": 2, "social": 2})]},
        {"text": "I like working with data to find patterns and insights", "category": "interest", "order": 2,
         "options": [("Strongly Agree", {"data": 3, "science": 2, "business": 1}),
                     ("Agree", {"data": 2, "business": 1}),
                     ("Neutral", {}),
                     ("Disagree", {"creative": 1, "social": 1})]},
        {"text": "I enjoy designing visuals and creating aesthetically pleasing things", "category": "interest", "order": 3,
         "options": [("Strongly Agree", {"creative": 3}),
                     ("Agree", {"creative": 2}),
                     ("Neutral", {"business": 1}),
                     ("Disagree", {"tech": 1, "data": 1})]},
        {"text": "I prefer working with people over working with machines/computers", "category": "personality", "order": 4,
         "options": [("Strongly Agree", {"social": 3, "business": 2}),
                     ("Agree", {"social": 2, "business": 1}),
                     ("Neutral", {}),
                     ("Disagree", {"tech": 2, "data": 2, "security": 1})]},
        {"text": "I am interested in how things are secured and protected from threats", "category": "interest", "order": 5,
         "options": [("Strongly Agree", {"security": 3, "tech": 1}),
                     ("Agree", {"security": 2}),
                     ("Neutral", {"tech": 1}),
                     ("Disagree", {"creative": 1, "social": 1})]},
        {"text": "I enjoy leading projects and managing teams to achieve goals", "category": "skill", "order": 6,
         "options": [("Strongly Agree", {"business": 3, "social": 2}),
                     ("Agree", {"business": 2, "social": 1}),
                     ("Neutral", {}),
                     ("Disagree", {"tech": 1, "data": 1})]},
        {"text": "I am excited by cloud computing and scalable infrastructure", "category": "interest", "order": 7,
         "options": [("Strongly Agree", {"cloud": 3, "tech": 2}),
                     ("Agree", {"cloud": 2, "tech": 1}),
                     ("Neutral", {"tech": 1}),
                     ("Disagree", {"creative": 1, "social": 1})]},
        {"text": "I like conducting research and experimenting with new ideas", "category": "interest", "order": 8,
         "options": [("Strongly Agree", {"science": 3, "data": 2}),
                     ("Agree", {"science": 2, "data": 1}),
                     ("Neutral", {"business": 1}),
                     ("Disagree", {"creative": 1, "social": 1})]},
        {"text": "I value job stability and a clear career progression path", "category": "value", "order": 9,
         "options": [("Strongly Agree", {"business": 2, "tech": 1}),
                     ("Agree", {"business": 1}),
                     ("Neutral", {}),
                     ("Disagree", {"creative": 2})]},
        {"text": "I enjoy building and programming software applications", "category": "skill", "order": 10,
         "options": [("Strongly Agree", {"tech": 3, "cloud": 1}),
                     ("Agree", {"tech": 2}),
                     ("Neutral", {"data": 1}),
                     ("Disagree", {"creative": 1, "social": 2})]},
    ]

    for qd in questions_data:
        q = Question.objects.create(text=qd['text'], category=qd['category'], order=qd['order'])
        for opt_text, weight in qd['options']:
            Option.objects.create(question=q, text=opt_text, weight=weight)
