import openai
from django.conf import settings

CAREER_SKILLS = {
    "Software Engineer": {
        "skills": ["Python", "Java", "JavaScript", "SQL", "Git", "Docker", "AWS", "React", "Django", "REST API", "Agile"],
        "description": "Design, develop and maintain software systems",
        "avg_salary": "$95,000 - $150,000",
        "growth": "25%",
        "icon": "bi-code-slash"
    },
    "Data Scientist": {
        "skills": ["Python", "Machine Learning", "SQL", "TensorFlow", "Statistics", "Tableau", "R", "Deep Learning", "NLP", "Pandas"],
        "description": "Extract insights from complex datasets using statistical methods",
        "avg_salary": "$100,000 - $160,000",
        "growth": "35%",
        "icon": "bi-bar-chart-line"
    },
    "UX Designer": {
        "skills": ["Figma", "Adobe XD", "User Research", "Prototyping", "CSS", "HTML", "Sketch", "Usability Testing", "Information Architecture"],
        "description": "Create intuitive and engaging user experiences",
        "avg_salary": "$80,000 - $130,000",
        "growth": "13%",
        "icon": "bi-palette"
    },
    "Product Manager": {
        "skills": ["Agile", "Jira", "Data Analysis", "Communication", "Leadership", "SQL", "Roadmapping", "Stakeholder Management"],
        "description": "Lead product strategy and cross-functional teams",
        "avg_salary": "$110,000 - $170,000",
        "growth": "10%",
        "icon": "bi-kanban"
    },
    "Cybersecurity Analyst": {
        "skills": ["Networking", "Linux", "Python", "SIEM", "Penetration Testing", "Firewalls", "Incident Response", "CISSP"],
        "description": "Protect systems and networks from digital attacks",
        "avg_salary": "$90,000 - $140,000",
        "growth": "35%",
        "icon": "bi-shield-check"
    },
    "DevOps Engineer": {
        "skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Python", "Terraform", "Jenkins", "Git", "Monitoring"],
        "description": "Bridge development and operations for faster delivery",
        "avg_salary": "$100,000 - $155,000",
        "growth": "22%",
        "icon": "bi-gear-wide-connected"
    },
    "Digital Marketing Manager": {
        "skills": ["SEO", "Google Analytics", "Content Marketing", "Social Media", "Email Marketing", "PPC", "CRM", "Copywriting"],
        "description": "Drive brand growth through digital channels",
        "avg_salary": "$70,000 - $120,000",
        "growth": "10%",
        "icon": "bi-megaphone"
    },
    "Business Analyst": {
        "skills": ["SQL", "Excel", "Data Analysis", "Communication", "BPMN", "Requirements Gathering", "Tableau", "Agile"],
        "description": "Bridge business needs and technical solutions",
        "avg_salary": "$75,000 - $120,000",
        "growth": "11%",
        "icon": "bi-briefcase"
    },
    "Cloud Architect": {
        "skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Networking", "Security", "Terraform", "Python"],
        "description": "Design and oversee cloud computing strategies",
        "avg_salary": "$130,000 - $200,000",
        "growth": "30%",
        "icon": "bi-cloud"
    },
    "AI/ML Engineer": {
        "skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "MLOps", "Statistics", "Docker"],
        "description": "Build and deploy machine learning models at scale",
        "avg_salary": "$120,000 - $190,000",
        "growth": "40%",
        "icon": "bi-cpu"
    },
}

COURSE_DATABASE = {
    "python": {"name": "Python Bootcamp", "platform": "Udemy", "url": "https://udemy.com", "free": False},
    "machine learning": {"name": "ML Specialization", "platform": "Coursera", "url": "https://coursera.org", "free": True},
    "sql": {"name": "SQL for Data Science", "platform": "Coursera", "url": "https://coursera.org", "free": True},
    "docker": {"name": "Docker Mastery", "platform": "Udemy", "url": "https://udemy.com", "free": False},
    "aws": {"name": "AWS Cloud Practitioner", "platform": "AWS Training", "url": "https://aws.amazon.com/training", "free": True},
    "react": {"name": "React - The Complete Guide", "platform": "Udemy", "url": "https://udemy.com", "free": False},
    "figma": {"name": "Figma UI Design", "platform": "YouTube", "url": "https://youtube.com", "free": True},
    "tensorflow": {"name": "Deep Learning Specialization", "platform": "Coursera", "url": "https://coursera.org", "free": True},
    "kubernetes": {"name": "Kubernetes for Developers", "platform": "Linux Foundation", "url": "https://training.linuxfoundation.org", "free": False},
    "javascript": {"name": "JavaScript Algorithms", "platform": "freeCodeCamp", "url": "https://freecodecamp.org", "free": True},
    "networking": {"name": "CompTIA Network+", "platform": "CompTIA", "url": "https://comptia.org", "free": False},
    "agile": {"name": "Agile Scrum Master", "platform": "Coursera", "url": "https://coursera.org", "free": True},
    "excel": {"name": "Excel for Business", "platform": "Coursera", "url": "https://coursera.org", "free": True},
    "tableau": {"name": "Tableau Desktop Specialist", "platform": "Tableau", "url": "https://tableau.com", "free": False},
    "linux": {"name": "Linux Command Line Basics", "platform": "edX", "url": "https://edx.org", "free": True},
}

def get_career_recommendations(scores):
    career_map = {
        "tech": ["Software Engineer", "DevOps Engineer", "AI/ML Engineer"],
        "data": ["Data Scientist", "Business Analyst", "AI/ML Engineer"],
        "creative": ["UX Designer", "Digital Marketing Manager"],
        "social": ["Product Manager", "Business Analyst", "Digital Marketing Manager"],
        "business": ["Business Analyst", "Product Manager", "Digital Marketing Manager"],
        "science": ["Data Scientist", "AI/ML Engineer", "Cybersecurity Analyst"],
        "security": ["Cybersecurity Analyst", "DevOps Engineer", "Cloud Architect"],
        "cloud": ["Cloud Architect", "DevOps Engineer", "Software Engineer"],
    }
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_categories = [cat for cat, score in sorted_scores[:3] if score > 0]
    recommendations = []
    seen = set()
    for cat in top_categories:
        for career in career_map.get(cat, []):
            if career not in seen:
                recommendations.append(career)
                seen.add(career)
    return recommendations[:6]

def analyze_skill_gap(user_skills_str, target_career):
    user_skills = set([s.strip().lower() for s in user_skills_str.split(',') if s.strip()])
    career_data = CAREER_SKILLS.get(target_career, {})
    required = career_data.get('skills', [])
    required_lower = {s.lower(): s for s in required}

    matched = [required_lower[s] for s in user_skills if s in required_lower]
    missing = [s for s in required if s.lower() not in user_skills]

    match_pct = (len(matched) / len(required) * 100) if required else 0

    courses = []
    for skill in missing[:5]:
        course = COURSE_DATABASE.get(skill.lower())
        if course:
            courses.append({**course, 'skill': skill})
        else:
            courses.append({'skill': skill, 'name': f'{skill} Fundamentals', 'platform': 'Google', 'url': f'https://google.com/search?q={skill}+course', 'free': True})

    return {
        'target_career': target_career,
        'career_info': career_data,
        'required_skills': required,
        'matched_skills': matched,
        'missing_skills': missing,
        'match_percentage': round(match_pct, 1),
        'courses_suggested': courses,
    }

def get_ai_career_advice(user, quiz_scores, recommended_careers):
    if not settings.OPENAI_API_KEY:
        return generate_fallback_advice(recommended_careers, quiz_scores)
    try:
        openai.api_key = settings.OPENAI_API_KEY
        prompt = f"""
You are an expert career counselor. Provide structured career advice based on this profile:

User Skills: {user.current_skills or 'Not specified'}
Desired Career: {user.desired_career or 'Not specified'}
Experience: {user.experience_years} years
Assessment Scores: {quiz_scores}
Top Recommended Careers: {', '.join(recommended_careers[:3])}

Provide:
1. **Best Career Match**: Which career suits them best and why
2. **Key Strengths**: 3 strengths based on their profile
3. **Action Plan**: 3 concrete next steps to take this month
4. **Learning Path**: Top 3 skills to acquire in priority order
5. **Timeline**: Realistic timeline to reach their career goal

Keep it encouraging, specific, and actionable. Format with clear sections.
"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional career counselor with 20 years of experience helping people find fulfilling careers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message['content']
    except Exception as e:
        return generate_fallback_advice(recommended_careers, quiz_scores)

def generate_fallback_advice(recommended_careers, scores):
    top_career = recommended_careers[0] if recommended_careers else "Software Engineer"
    career_info = CAREER_SKILLS.get(top_career, {})
    return f"""**Best Career Match: {top_career}**
Based on your assessment, {top_career} aligns well with your interests and aptitudes.
{career_info.get('description', '')}

**Your Key Strengths**
• Strong analytical and problem-solving mindset
• Good balance of technical and interpersonal skills
• High motivation and self-awareness

**Action Plan for This Month**
1. Update your LinkedIn profile to reflect your target career
2. Complete one online course in a required skill area
3. Connect with 3 professionals in your target field

**Learning Path**
Priority skills: {', '.join(career_info.get('skills', [])[:4])}

**Timeline**
With consistent effort, you can transition into {top_career} within 6-12 months."""
