import re

SKILL_KEYWORDS = [
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Ruby', 'Go', 'Rust', 'PHP', 'Swift', 'Kotlin',
    'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring Boot', 'Rails', 'Laravel',
    'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Cassandra', 'Oracle',
    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Ansible', 'Jenkins', 'CI/CD',
    'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'NLP', 'Computer Vision',
    'Pandas', 'NumPy', 'Matplotlib', 'Tableau', 'Power BI', 'Excel', 'R', 'MATLAB',
    'Git', 'GitHub', 'Jira', 'Confluence', 'Agile', 'Scrum', 'Kanban',
    'Figma', 'Adobe XD', 'Sketch', 'Photoshop', 'Illustrator',
    'HTML', 'CSS', 'Bootstrap', 'Tailwind', 'GraphQL', 'REST API', 'Microservices',
    'Linux', 'Bash', 'PowerShell', 'Networking', 'CISCO',
    'Project Management', 'Leadership', 'Communication', 'Problem Solving', 'Team Management',
    'SEO', 'Google Analytics', 'Content Marketing', 'Social Media', 'Email Marketing',
    'Cybersecurity', 'Penetration Testing', 'CISSP', 'CEH', 'SIEM',
]

EDUCATION_LEVELS = {
    'phd': 'PhD / Doctorate',
    'doctorate': 'PhD / Doctorate',
    'master': "Master's Degree",
    'mba': 'MBA',
    'bachelor': "Bachelor's Degree",
    'b.tech': "Bachelor's Degree",
    'b.e.': "Bachelor's Degree",
    'b.sc': "Bachelor's Degree",
    'associate': "Associate's Degree",
    'diploma': 'Diploma',
    'certification': 'Certification',
}

def extract_text_from_file(file_path):
    text = ""
    try:
        if file_path.lower().endswith('.pdf'):
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                text = f"[PDF extraction error: {str(e)}]"
        elif file_path.lower().endswith('.docx'):
            try:
                import docx
                doc = docx.Document(file_path)
                text = '\n'.join([para.text for para in doc.paragraphs])
            except Exception as e:
                text = f"[DOCX extraction error: {str(e)}]"
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
    except Exception as e:
        text = f"[File read error: {str(e)}]"
    return text

def extract_skills(text):
    found = []
    text_lower = text.lower()
    for skill in SKILL_KEYWORDS:
        if skill.lower() in text_lower:
            found.append(skill)
    return list(dict.fromkeys(found))

def extract_education(text):
    text_lower = text.lower()
    for keyword, level in EDUCATION_LEVELS.items():
        if keyword in text_lower:
            return level
    return 'Not Specified'

def extract_experience_years(text):
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'experience\s*(?:of\s*)?(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience',
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return float(match.group(1))
    return None

def calculate_ats_score(text):
    score = 0
    checks = {
        'email': (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 10),
        'phone': (r'\b[\+]?[\d\s\-\(\)]{10,15}\b', 10),
        'linkedin': (r'linkedin\.com', 8),
        'github': (r'github\.com', 7),
    }
    for key, (pattern, pts) in checks.items():
        if re.search(pattern, text, re.IGNORECASE):
            score += pts

    sections = {
        'experience': 8, 'education': 8, 'skills': 8,
        'summary': 6, 'objective': 5, 'projects': 7,
        'achievements': 6, 'certifications': 5,
    }
    for section, pts in sections.items():
        if section in text.lower():
            score += pts

    word_count = len(text.split())
    if 300 <= word_count <= 800:
        score += 10
    elif word_count > 800:
        score += 5

    skill_count = len(extract_skills(text))
    if skill_count >= 10:
        score += 7
    elif skill_count >= 5:
        score += 4

    return min(score, 100)

def get_resume_feedback(text, skills, ats_score):
    tips = []
    if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        tips.append("❌ Add your email address - it's essential for recruiters to contact you.")
    if not re.search(r'linkedin\.com', text, re.I):
        tips.append("💡 Add your LinkedIn profile URL to increase credibility.")
    if not re.search(r'github\.com', text, re.I):
        tips.append("💡 Add your GitHub profile to showcase your technical work.")
    if len(skills) < 8:
        tips.append(f"📊 Currently {len(skills)} skills detected. Aim for 10-15 relevant technical skills.")
    if 'summary' not in text.lower() and 'objective' not in text.lower():
        tips.append("✍️ Add a professional summary at the top to make a strong first impression.")
    if 'project' not in text.lower():
        tips.append("🚀 Include a Projects section to demonstrate practical experience.")
    if len(text.split()) < 300:
        tips.append("📝 Your resume seems short. Add more details about your experience and achievements.")
    if ats_score < 60:
        tips.append("⚠️ Use standard section headings like 'Experience', 'Education', 'Skills' for better ATS parsing.")

    strengths = []
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        strengths.append("✅ Contact information is present")
    if len(skills) >= 8:
        strengths.append(f"✅ Good skill coverage ({len(skills)} skills identified)")
    if 'experience' in text.lower():
        strengths.append("✅ Experience section included")
    if 'education' in text.lower():
        strengths.append("✅ Education section included")

    return {'improvements': tips, 'strengths': strengths}
