import json
import openai
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from .models import ChatSession, ChatMessage

SYSTEM_PROMPT = """You are CareerAI, an expert career counselor with 20+ years of experience. 
You help people with:
- Career path selection and transitions
- Resume writing and optimization  
- Interview preparation and tips
- Skill development recommendations
- Job search strategies
- Salary negotiation advice
- Work-life balance guidance
- Industry insights and trends

Be encouraging, specific, and actionable. Use emojis occasionally to keep the conversation engaging.
Keep responses concise but informative (150-250 words max per response).
Always end with a follow-up question to continue the conversation."""

@login_required
def chatbot_view(request):
    sessions = ChatSession.objects.filter(user=request.user)[:10]
    current_session = None

    session_id = request.GET.get('session')
    if session_id:
        current_session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
    elif sessions.exists():
        current_session = sessions.first()

    messages_list = []
    if current_session:
        messages_list = current_session.messages.all()

    return render(request, 'chatbot/chat.html', {
        'sessions': sessions,
        'current_session': current_session,
        'chat_messages': messages_list,
    })

@login_required
def new_session(request):
    session = ChatSession.objects.create(user=request.user, title='New Conversation')
    return redirect(f'/chatbot/?session={session.pk}')

@login_required
def delete_session(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    session.delete()
    return redirect('chatbot')

@login_required
@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id')

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        if session_id:
            session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
        else:
            session = ChatSession.objects.create(user=request.user, title=user_message[:50])

        # Update session title from first message
        if session.messages.count() == 0:
            session.title = user_message[:60]
            session.save()

        ChatMessage.objects.create(session=session, role='user', content=user_message)

        history = list(session.messages.order_by('timestamp').values('role', 'content'))[-12:]

        if settings.OPENAI_API_KEY:
            try:
                openai.api_key = settings.OPENAI_API_KEY
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                api_messages += [{"role": m['role'], "content": m['content']} for m in history]

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=api_messages,
                    max_tokens=400,
                    temperature=0.7
                )
                reply = response.choices[0].message['content']
            except Exception as e:
                reply = get_fallback_response(user_message)
        else:
            reply = get_fallback_response(user_message)

        ChatMessage.objects.create(session=session, role='assistant', content=reply)

        return JsonResponse({
            'reply': reply,
            'session_id': session.pk,
            'session_title': session.title,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_fallback_response(message):
    message_lower = message.lower()
    responses = {
        'resume': "📄 Great question about resumes! Key tips: 1) Keep it to 1-2 pages, 2) Use action verbs, 3) Quantify achievements, 4) Include relevant keywords from job descriptions, 5) Ensure ATS-friendly formatting. Would you like specific advice for a particular industry?",
        'interview': "🎯 Interview prep is crucial! Practice the STAR method (Situation, Task, Action, Result). Research the company thoroughly, prepare 5 questions to ask the interviewer, and practice common behavioral questions. What type of interview are you preparing for?",
        'salary': "💰 Salary negotiation: Research market rates on Glassdoor and LinkedIn. Always negotiate - it's expected! Start with a range 10-20% above your target. Emphasize your value. Would you like help researching salary ranges for a specific role?",
        'skill': "🚀 Continuous learning is key! Focus on high-demand skills in your field. Use free resources: Coursera, edX, freeCodeCamp. Build a portfolio to demonstrate skills. What specific skills are you looking to develop?",
        'career': "🌟 Career planning starts with self-assessment. Consider your strengths, interests, and values. Research growth areas in your field. Set SMART goals. Would you like help with our Career Assessment Quiz for personalized recommendations?",
    }
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    return "👋 I'm CareerAI, your personal career counselor! I can help with resume tips, interview prep, salary negotiation, skill development, and career planning. Add your OpenAI API key in settings for full AI-powered responses. What career challenge can I help you with today?"
