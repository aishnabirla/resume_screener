import spacy
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

nlp = spacy.load("en_core_web_sm")

SKILLS_DATABASE = [
    # ── Languages ──
    "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift",
    "kotlin", "typescript", "matlab", "scala", "perl", "bash", "shell",
    "r", "go", "julia", "rust", "groovy",

    # ── Web & Frontend ──
    "html", "css", "react", "angular", "vue", "node", "django", "flask",
    "fastapi", "spring", "graphql", "rest api", "microservices",

    # ── AI / ML / DL ──
    "tensorflow", "pytorch", "keras", "scikit-learn", "opencv", "nltk", "spacy",
    "machine learning", "deep learning", "nlp", "computer vision",
    "artificial intelligence", "neural networks", "data science",
    "ai", "ml", "ai/ml", "feature engineering", "model serving",
    "llm", "generative ai", "transformers", "hugging face",

    # ── Data Engineering ──
    "spark", "pyspark", "apache spark",
    "kafka", "apache kafka",
    "airflow", "apache airflow",
    "hadoop", "apache hadoop",
    "hive", "hdfs", "emr", "glue", "s3",
    "flink", "kafka streams",
    "dbt", "etl", "elt",
    "data pipeline", "data pipelines",
    "data warehouse", "data lake", "data lakehouse",
    "data modeling", "data engineering", "data integration",
    "data quality", "batch processing", "streaming", "real time",

    # ── Cloud Platforms ──
    "aws", "azure", "gcp",
    "google cloud", "amazon web services", "microsoft azure",
    "cloud computing", "cloud native",

    # ── Cloud Services ──
    "databricks", "snowflake", "redshift", "bigquery",
    "delta lake", "delta",
    "dynamo", "hbase", "cassandra", "cosmos db",
    "azure cosmos db", "azure blob",

    # ── Databases ──
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis",
    "sqlalchemy", "impala", "sql server",

    # ── DevOps & Infra ──
    "docker", "kubernetes", "k8s",
    "jenkins", "ci/cd", "cicd",
    "terraform", "ansible",
    "git", "github", "svn",
    "linux", "devops",

    # ── Data Analysis & BI ──
    "pandas", "numpy", "matplotlib", "seaborn",
    "data analysis", "data visualization",
    "big data", "excel", "power bi", "tableau",

    # ── Enterprise Systems ──
    "sap", "sap abap", "abap", "oracle",
    "salesforce", "workday", "servicenow",

    # ── Methodology & Practices ──
    "agile", "scrum", "data structures", "algorithms",
    "object oriented", "unit testing", "code review",

    # ── Other Tech ──
    "blockchain", "iot", "cybersecurity",
    "flutter", "react native", "android", "ios",
    "selenium", "pytest", "junit", "postman",
    "jira", "confluence",
    "visual studio", "jupyter", "jupyter notebook",
    "power automate", "ms office",
    "solidity", "web3", "ethereum",
    "computer networks", "operating systems",
]

# Remove duplicates while preserving order
seen = set()
SKILLS_DATABASE = [
    s for s in SKILLS_DATABASE
    if not (s in seen or seen.add(s))
]

SKILL_ALIASES = {
    # Apache prefixed variants
    "apache spark":   ["spark", "pyspark"],
    "apache kafka":   ["kafka"],
    "apache airflow": ["airflow"],
    "apache hadoop":  ["hadoop"],

    # Spark family
    "spark":   ["pyspark", "apache spark"],
    "pyspark": ["spark", "apache spark"],

    # Cloud platforms
    "aws":   ["amazon web services"],
    "azure": ["microsoft azure"],
    "gcp":   ["google cloud"],

    # Databases
    "postgresql":  ["postgres"],
    "sql server":  ["mssql", "ms sql"],
    "cosmos db":   ["azure cosmos db"],
    "delta lake":  ["delta"],

    # DevOps
    "kubernetes": ["k8s"],
    "ci/cd":      ["cicd", "jenkins"],

    # ML libraries
    "scikit-learn": ["sklearn"],
    "tensorflow":   ["tf"],

    # Languages & frameworks
    "javascript": ["js"],
    "typescript": ["ts"],
    "react":      ["reactjs", "react.js"],
    "node":       ["nodejs", "node.js"],
}

# Short skills that need exact word boundary matching to avoid false positives
# e.g. "r" shouldn't match "error", "c" shouldn't match "science"
EXACT_MATCH_SKILLS = ["r", "go", "c", "perl", "julia"]

STOP_WORDS = set(stopwords.words('english'))

COMMON_WORDS_TO_IGNORE = {
    "education", "experience", "skills", "objective", "summary",
    "projects", "certifications", "publications", "activities",
    "leadership", "technical", "work", "profile", "contact",
    "interests", "languages", "references", "achievements",
    "responsibilities", "date", "name", "email", "phone",
    "address", "linkedin", "github", "university", "college",
    "institute", "school", "bachelor", "master", "degree"
}

def extract_skills(text, jd_text=None):
    """
    Fully JD-driven skill extraction.
    
    If jd_text is provided (resume evaluation context):
        - Extract skill candidates from JD
        - Check which ones appear in the resume text
        - No hardcoded database needed
    
    If jd_text is not provided (extracting FROM the JD itself):
        - Use NLP to pull noun phrases and technical terms
        - Fall back to SKILLS_DATABASE as a supplementary boost only
    """
    import re
    text_lower = text.lower()
    found_skills = []

    # ── Layer 1: If JD text provided, extract skills FROM JD and check resume ──
    if jd_text:
        jd_lower = jd_text.lower()
        
        # Split JD into candidate skill tokens by common delimiters
        candidates = re.split(r'[,\n•\-\|/\(\)]', jd_lower)
        for candidate in candidates:
            candidate = candidate.strip()
            # Valid skill: 2-40 chars, not a stop word, not a common resume section word
            if (2 <= len(candidate) <= 40
                    and candidate not in STOP_WORDS
                    and candidate not in COMMON_WORDS_TO_IGNORE
                    and not candidate.isdigit()):
                # Check if this JD skill appears in the resume
                if re.search(r'\b' + re.escape(candidate) + r'\b', text_lower):
                    found_skills.append(candidate)

    # ── Layer 2: SKILLS_DATABASE as supplementary boost ──
    # Catches skills that may be phrased differently in JD but present in resume
    for skill in SKILLS_DATABASE:
        if skill not in found_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)

    return list(set(found_skills))

def extract_education(text):
    education_keywords = [
        "bachelor", "master", "phd", "b.tech", "m.tech", "mba", "bca",
        "mca", "b.sc", "m.sc", "degree", "diploma", "graduate",
        "undergraduate", "university", "college", "institute", "school",
        "cgpa", "gpa", "computer science", "engineering",
        "information technology"
    ]
    doc = nlp(text)
    education = []
    sentences = [sent.text for sent in doc.sents]
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in education_keywords):
            education.append(sentence.strip())
    return " | ".join(education[:3]) if education else "Not found"


def extract_experience(text):
    experience_patterns = [
        r'\d+\+?\s*years?\s*of\s*experience',
        r'experience\s*of\s*\d+\+?\s*years?',
        r'\d+\+?\s*years?\s*experience',
        r'worked\s*at\s*\w+',
        r'internship\s*at\s*\w+',
        r'intern\s*at\s*\w+',
    ]
    found_experience = []
    for pattern in experience_patterns:
        matches = re.findall(pattern, text.lower())
        found_experience.extend(matches)
    doc = nlp(text)
    org_names = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    if org_names:
        found_experience.append(
            "Organizations: " + ", ".join(org_names[:3]))
    return " | ".join(found_experience[:3]) if found_experience else "Not found"


def extract_candidate_name(text):
    # Try spaCy PERSON entity first
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            if 2 <= len(name.split()) <= 4:
                return name

    # Try first non-empty line that looks like a name
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        # Remove phone numbers, emails, special chars
        cleaned = re.sub(r'[\d\+\-\(\)\@\.\,\|]', '', line).strip()
        # A name is 2-4 words, all letters
        words = cleaned.split()
        if 2 <= len(words) <= 4:
            if all(w.replace("'", "").isalpha() for w in words):
                return cleaned

    # Try finding name near common resume keywords
    name_pattern = r'^([A-Z][a-z]+(?:\s[A-Z][a-z]+){1,3})'
    for line in lines[:8]:
        match = re.match(name_pattern, line.strip())
        if match:
            return match.group(1)

    # Fallback — use filename without extension
    return "Candidate"


def extract_candidate_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else "Not found"


def process_resume(text, jd_text=None):
    return {
        "name": extract_candidate_name(text),
        "email": extract_candidate_email(text),
        "skills": extract_skills(text, jd_text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }


def process_jd(text):
    required_skills = []
    preferred_skills = []

    text_lower = text.lower()

    required_section = ""
    preferred_section = ""

    if "required" in text_lower:
        parts = text_lower.split("required")
        if len(parts) > 1:
            required_section = parts[1][:500]

    if "preferred" in text_lower or "nice to have" in text_lower:
        split_word = "preferred" if "preferred" in text_lower else "nice to have"
        parts = text_lower.split(split_word)
        if len(parts) > 1:
            preferred_section = parts[1][:500]

    if required_section:
        required_skills = extract_skills(required_section)
    if preferred_section:
        preferred_skills = extract_skills(preferred_section)

    all_skills = extract_skills(text)

    return {
        "required_skills": required_skills if required_skills else all_skills,
        "preferred_skills": preferred_skills,
        "all_skills": all_skills,
        "education": extract_education(text),
        "experience": extract_experience(text)
    }