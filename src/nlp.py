import spacy
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

nlp = spacy.load("en_core_web_sm")

# ─────────────────────────────────────────────
# SKILLS DATABASE
# ─────────────────────────────────────────────
SKILLS_DATABASE = [
    # Programming
    "python", "java", "javascript", "c++", "c#", "ruby", "php",
    "swift", "kotlin", "typescript", "scala", "matlab", "perl",
    "bash", "shell", "groovy", "rust",

    # Web
    "html", "css", "react", "angular", "vue", "node", "django",
    "flask", "fastapi", "spring", "graphql", "rest api",

    # AI/ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "artificial intelligence", "neural networks", "data science",
    "tensorflow", "pytorch", "keras", "scikit-learn", "opencv",
    "transformers", "llm", "generative ai", "mlops", "mlflow",

    # Data Engineering
    "spark", "pyspark", "kafka", "airflow", "hadoop",
    "hive", "hdfs", "flink", "dbt", "etl", "elt",
    "data pipeline", "data warehouse", "data lake",
    "data modeling", "data engineering", "data quality",
    "streaming", "batch processing", "delta lake",

    # Cloud
    "aws", "azure", "gcp", "cloud computing",

    # Cloud Services
    "databricks", "snowflake", "redshift", "bigquery",
    "cassandra", "cosmos db", "dynamo",
    "azure data factory", "azure synapse",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite",
    "oracle", "redis", "sqlalchemy", "teradata",

    # DevOps
    "docker", "kubernetes", "jenkins", "ci/cd",
    "terraform", "ansible", "git", "github", "linux", "devops",

    # BI/Analytics
    "pandas", "numpy", "matplotlib", "tableau", "power bi",
    "data analysis", "data visualization", "big data", "excel",

    # Enterprise
    "sap", "salesforce", "workday", "servicenow", "jira",

    # Design
    "figma", "adobe xd", "sketch", "illustrator", "photoshop",
    "canva", "ui design", "ux design", "wireframing", "prototyping",
    "user research", "design thinking",

    # Marketing
    "seo", "sem", "google ads", "content writing", "copywriting",
    "social media", "google analytics", "hubspot", "wordpress",

    # Project Management
    "agile", "scrum", "kanban", "confluence", "project management",

    # Finance
    "financial modeling", "accounting", "taxation",
    "financial analysis", "budgeting", "forecasting",

    # Teaching
    "curriculum design", "lesson planning", "classroom management",
    "pedagogy", "e-learning", "instructional design",

    # Healthcare
    "patient care", "clinical", "medical coding", "ehr", "emr",
    "hipaa", "nursing", "diagnosis", "treatment planning",

    # Legal
    "legal research", "contract drafting", "compliance",
    "litigation", "corporate law", "intellectual property",

    # HR
    "recruitment", "talent acquisition", "onboarding",
    "performance management", "employee relations", "payroll",

    # General Engineering
    "data structures", "algorithms", "system design",
    "unit testing", "code review", "microservices",
    "computer networks", "operating systems", "object oriented",

    # Other Tech
    "blockchain", "iot", "cybersecurity",
    "flutter", "react native", "android", "ios",
    "selenium", "pytest", "junit", "postman",
    "jupyter", "visual studio", "power automate",
]

EXACT_MATCH_SKILLS = ["r", "go", "c"]

STOP_WORDS = set(stopwords.words('english'))

# ─────────────────────────────────────────────
# NOISE WORDS
# ─────────────────────────────────────────────
NOISE_WORDS = {
    # Qualifiers
    "strong", "solid", "proven", "hands-on", "hands", "advanced",
    "proficient", "excellent", "good", "great", "effective",
    "efficient", "robust", "modern", "scalable", "production",
    "enterprise", "native", "based", "driven", "oriented",
    "grade", "level", "senior", "junior", "lead", "principal",
    "real", "end", "large", "well", "cross", "full", "back",
    "front", "open", "source", "high", "low",
    # Verbs
    "including", "using", "leveraging", "building", "developing",
    "develop", "designing", "managing", "leading", "working",
    "writing", "understanding", "ensuring", "implementing",
    "optimizing", "collaborating", "maintaining", "creating",
    "delivering", "integrating", "deploying", "supporting",
    # Generic nouns
    "proficiency", "familiarity", "knowledge", "ability",
    "tools", "practices", "frameworks", "platforms",
    "systems", "solutions", "services", "concepts",
    "methodologies", "technologies", "libraries",
    "environments", "applications", "processes",
    "reliability", "performance", "reusable",
    # Single chars / fragments
    "ci", "cd", "or", "and", "cost", "cloud",
    "data", "code", "design", "hands",
    "years", "year", "months", "month",
}

# ─────────────────────────────────────────────
# SECTION HEADERS
# ─────────────────────────────────────────────
SECTION_HEADERS = {
    "objective", "summary", "projects", "certifications",
    "publications", "activities", "contact", "interests",
    "references", "profile", "overview", "about",
    "key skills", "key responsibilities",
    "nice to have", "required", "preferred",
    "responsibilities", "qualifications",
}
RESUME_SECTION_WORDS = {
    "summary", "professional summary", "career objective",
    "profile", "about me", "overview", "objective",
}
# ─────────────────────────────────────────────
# KNOWN REAL SKILLS WHITELIST
# ─────────────────────────────────────────────
KNOWN_REAL_SKILLS = {
    # Tech
    "window functions", "query optimization", "performance tuning",
    "data pipeline", "data modeling", "data quality",
    "data engineering", "data integration", "data warehouse",
    "data lake", "data science", "data analysis",
    "machine learning", "deep learning", "computer vision",
    "natural language processing", "real time",
    "batch processing", "streaming", "ci/cd", "rest api",
    "object oriented", "unit testing", "code review",
    "system design", "big data", "cloud computing",
    # ServiceNow
    "flow designer", "business rules", "client scripts",
    "script includes", "employee center", "virtual agent",
    "service catalog", "service portal", "hr service delivery",
    # Design
    "user research", "design thinking", "wireframing",
    "ui design", "ux design", "prototyping",
    # Marketing
    "content writing", "social media", "google analytics",
    "seo", "sem", "email marketing", "lead generation",
    # Finance
    "financial modeling", "financial analysis",
    "cash flow", "balance sheet", "profit loss",
    # HR
    "talent acquisition", "performance management",
    "employee relations", "succession planning",
    # Teaching
    "curriculum design", "lesson planning",
    "classroom management", "student assessment",
    # Healthcare
    "patient care", "treatment planning", "clinical trials",
    "medical coding", "care coordination",
}

# ─────────────────────────────────────────────
# JOB TITLE WORDS — domain agnostic
# ─────────────────────────────────────────────
JOB_TITLE_WORDS = {
    "engineer", "developer", "analyst", "scientist", "manager",
    "lead", "architect", "consultant", "specialist", "director",
    "officer", "intern", "associate", "senior", "junior", "head",
    "vp", "president", "executive", "contact", "profile", "resume",
    "cv", "software", "solutions", "technical", "ai", "ml",
    "full", "stack", "backend", "frontend", "data", "cloud",
    "servicenow", "hrsd", "itsm", "sme",
    "teacher", "professor", "instructor", "trainer",
    "doctor", "nurse", "physician", "therapist",
    "accountant", "auditor", "advisor", "designer",
    "writer", "editor", "coordinator", "administrator",
}

# ─────────────────────────────────────────────
# CONTACT WORDS — used in name extraction
# ─────────────────────────────────────────────
CONTACT_WORDS = {
    "mobile", "phone", "email", "linkedin", "github", "contact",
    "address", "location", "website", "twitter", "skype", "tel",
    "gmail", "yahoo", "outlook", "hotmail", "whatsapp", "fax",
}

# ─────────────────────────────────────────────
# ORG BLACKLIST
# ─────────────────────────────────────────────
ORG_BLACKLIST = {
    # Tech tools
    "spark", "python", "java", "sql", "hadoop", "kafka",
    "airflow", "docker", "kubernetes", "git", "linux",
    "tensorflow", "pytorch", "scala", "pyspark", "aws",
    "azure", "gcp", "databricks", "snowflake", "redshift",
    "bigquery", "hive", "hdfs", "servicenow", "salesforce",
    # Job titles
    "data engineer", "software engineer", "data scientist",
    "developer", "analyst", "engineer", "manager", "consultant",
    # Domain terms
    "medallion architecture", "predictive analytics",
    "itsm", "hrsd", "itam", "cmdb",
}


# ─────────────────────────────────────────────
# NAME HELPERS
# ─────────────────────────────────────────────
def _collapse_spaced_name(text):
    """
    Collapses spaced names like 'M O H A M M E D F A R I D H'
    Detects word boundaries by looking for 2+ consecutive spaced single letters
    then a gap of 2+ spaces before another group starts.
    """
    # Match groups of single uppercase letters separated by single spaces
    # Groups are separated from each other by 2+ spaces
    pattern = r'(?:[A-Z] +){2,}[A-Z]'
    spaced = re.findall(pattern, text)
    result = text
    for match in spaced:
        # Split by 2+ spaces to find word boundaries within the match
        parts = re.split(r' {2,}', match.strip())
        if len(parts) > 1:
            # Multiple groups — collapse each separately and join with space
            collapsed = ' '.join(p.replace(' ', '') for p in parts)
        else:
            # Single group — collapse all letters together
            # Try to detect first/last name boundary by double space
            collapsed = match.replace(' ', '').strip()
        result = result.replace(match, collapsed + ' ', 1)
    return result

def _is_valid_name(words):
    if not (2 <= len(words) <= 3):
        return False
    if not all(w.replace("'", "").replace("-", "").isalpha() for w in words):
        return False
    if any(w.lower() in JOB_TITLE_WORDS for w in words):
        return False
    if any(w.lower() in CONTACT_WORDS for w in words):
        return False
    if any(len(w) == 1 and not w.isupper() for w in words):
        return False
    return True


# ─────────────────────────────────────────────
# NAME EXTRACTION — domain agnostic
# ─────────────────────────────────────────────
def extract_candidate_name(text):
    text_proc = _collapse_spaced_name(text)
    lines = text_proc.strip().split('\n')

    for line in lines[:10]:
        line = line.strip()
        if not line or len(line) < 2:
            continue

        line_lower = line.lower()

        # Skip contact/label lines
        if any(cw in line_lower for cw in CONTACT_WORDS):
            continue
        if '@' in line:
            continue
        if re.search(r'\d{5,}', line):
            continue
        if line.startswith('http') or 'linkedin' in line_lower:
            continue

        # ── Handle "Name: Bharath" format ──
        if ':' in line:
            colon_parts = line.split(':', 1)
            label = colon_parts[0].strip().lower()
            value = colon_parts[1].strip()
            if label in {'name', 'full name', 'candidate name'} and value:
                # Remove any trailing job title words
                cleaned = re.sub(r'[^\w\s\'-]', ' ', value).strip()
                cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                if cleaned.isupper():
                    cleaned = cleaned.title()
                words = cleaned.split()
                # Return first valid name portion
                for end in range(len(words), 0, -1):
                    candidate = words[:end]
                    if _is_valid_name(candidate):
                        return ' '.join(candidate)
                # If no multi-word valid name, return single word if it looks like a name
                if len(words) >= 1 and words[0].replace("'","").isalpha():
                    w = words[0]
                    if w.lower() not in JOB_TITLE_WORDS and w.lower() not in CONTACT_WORDS:
                        return w.capitalize()
            continue  # skip all other colon lines

        # Clean line
        cleaned = re.sub(r'[^\w\s\'-]', ' ', line).strip()
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        if not cleaned:
            continue

        # Normalise ALL CAPS to Title Case
        if cleaned.isupper():
            cleaned = cleaned.title()

        words = cleaned.split()

        # ── Handle collapsed single-word full name like MOHAMMEDFARIDH ──
        if len(words) == 1 and len(words[0]) > 6 and words[0].replace("'","").isalpha():
            word = words[0]

            # Try 1: CamelCase boundary split (works for MohammedFaridh)
            parts = re.findall(r'[A-Z][a-z]+', word)
            if 2 <= len(parts) <= 3 and all(p.replace("'","").isalpha() for p in parts):
                candidate = ' '.join(parts)
                if _is_valid_name(candidate.split()):
                    return candidate

            # Try 2: title() then boundary split (works after normalisation)
            titled = word.title()
            parts = re.findall(r'[A-Z][a-z]+', titled)
            if 2 <= len(parts) <= 3 and all(p.replace("'","").isalpha() for p in parts):
                candidate = ' '.join(parts)
                if _is_valid_name(candidate.split()):
                    return candidate

            # Try 3: Split long word at midpoint if all alpha and long enough
            # e.g. MOHAMMEDFARIDH (14 chars) → try all split points
            if len(word) >= 8:
                best = None
                for i in range(3, len(word) - 3):
                    part1 = word[:i].title()
                    part2 = word[i:].title()
                    if (part1.replace("'","").isalpha() and
                            part2.replace("'","").isalpha() and
                            len(part1) >= 3 and len(part2) >= 3 and
                            part1.lower() not in JOB_TITLE_WORDS and
                            part2.lower() not in JOB_TITLE_WORDS):
                        # Prefer splits that give roughly equal halves
                        if best is None or abs(len(part1)-len(part2)) < abs(len(best[0])-len(best[1])):
                            best = (part1, part2)
                if best:
                    candidate = f"{best[0]} {best[1]}"
                    if _is_valid_name(candidate.split()):
                        return candidate

            # Cannot resolve single word — return Candidate so filename fallback runs
            return "Candidate"

# ─────────────────────────────────────────────
# EDUCATION EXTRACTION — domain agnostic
# ─────────────────────────────────────────────
def extract_education(text):
    # Broad degree keywords covering all domains
    degree_keywords = [
        "bachelor", "master", "phd", "ph.d", "doctorate",
        "b.tech", "m.tech", "mba", "bca", "mca",
        "b.sc", "m.sc", "b.e", "m.e", "b.com", "m.com",
        "pgdm", "diploma", "b.s", "m.s", "bba", "msc",
        "bachelor of", "master of", "doctor of",
        "associate degree", "higher national",
        "llb", "llm", "mbbs", "bds", "md", "ms",
        "b.a", "m.a", "ba", "ma", "bfa", "mfa",
        "be", "btech", "mtech", "b. tech", "m. tech",
    ]
    institution_keywords = [
        "university", "college", "institute", "school",
        "academy", "polytechnic", "technology",
        "iit", "nit", "bits", "iim",
    ]
    # Words indicating this is a work sentence not education
    work_words = [
        "worked", "implemented", "developed", "managed",
        "designed", "responsible", "client", "project",
        "led", "built", "created", "configured", "deployed",
        "mentored", "optimized", "delivered", "automated",
        "migration", "experience", "stakeholder",
    ]

    education = []

    # Method 1 — find EDUCATION section header
    edu_match = re.search(
        r'\b(?:education|academic\s+qualification|qualification)[s]?\s*[:\-–]?\s*\n+((?:.*\n){1,8})',
        text,
        re.IGNORECASE
    )
    if edu_match:
        block = edu_match.group(1)
        for line in block.strip().split('\n')[:6]:
            line = line.strip()
            if not line or len(line) < 5:
                continue
            line_lower = line.lower()
            has_degree = any(kw in line_lower for kw in degree_keywords)
            has_inst = any(kw in line_lower for kw in institution_keywords)
            has_work = any(ww in line_lower for ww in work_words)
            if (has_degree or has_inst) and not has_work:
                education.append(line[:200])
        if education:
            education = [e for e in education if len(e) > 8]
            return " | ".join(education[:3])

    # Method 2 — line scan requiring degree + institution
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5 or len(line) > 180:
            continue
        line_lower = line.lower()
        has_degree = any(kw in line_lower for kw in degree_keywords)
        has_inst = any(kw in line_lower for kw in institution_keywords)
        has_work = any(ww in line_lower for ww in work_words)
        if has_work:
            continue
        if has_degree and has_inst:
            education.append(line[:180])
        elif has_degree and len(line) < 80:
            education.append(line[:180])

    if education:
        seen = set()
        unique = []
        for e in education[:5]:
            key = e[:25].lower()
            if key not in seen:
                seen.add(key)
                unique.append(e)
        return " | ".join(unique[:3])

    return "Not found"


# ─────────────────────────────────────────────
# EXPERIENCE EXTRACTION — domain agnostic
# ─────────────────────────────────────────────
def extract_experience(text):
    found = []

    # Extract years of experience — multiple patterns
    year_patterns = [
        r'\d+\+?\s*years?\s*of\s*(?:professional\s*)?experience',
        r'experience\s*of\s*\d+\+?\s*years?',
        r'\d+\+?\s*years?\s*experience',
        r'\d+\+\s*years?',
        r'over\s*\d+\s*years?',
        r'more\s*than\s*\d+\s*years?',
    ]
    for pattern in year_patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            found.append(matches[0])
            break

    # Extract organisation names via spaCy
    doc = nlp(text)
    real_orgs = []
    seen_lower = set()

    for ent in doc.ents:
        if ent.label_ != "ORG":
            continue
        org = ent.text.strip()
        org_lower = org.lower().strip()

        if len(org) < 4:
            continue
        if org_lower in seen_lower:
            continue
        if org.startswith(('•', '-', '●')):
            continue
        if org_lower in ORG_BLACKLIST:
            continue
        if any(w.lower() in ORG_BLACKLIST for w in org.split()):
            continue
        if org.isupper() and len(org) <= 4:
            continue
        if ',' in org or '/' in org:
            continue
        if org == org.lower():
            continue
        if not any(len(w) >= 3 for w in org.split()):
            continue

        real_orgs.append(org)
        seen_lower.add(org_lower)

    if real_orgs:
        found.append("Organizations: " + ", ".join(real_orgs[:4]))

    return " | ".join(found[:2]) if found else "Not found"


# ─────────────────────────────────────────────
# SKILL EXTRACTION — domain agnostic
# ─────────────────────────────────────────────
def extract_skills(text, jd_text=None):
    text_lower = text.lower()
    found_skills = set()

    # Layer 1: JD-driven dynamic extraction
    if jd_text:
        jd_lower = jd_text.lower()
        candidates = re.split(r'[,\n•\-\|/\(\)\[\]]', jd_lower)

        for candidate in candidates:
            candidate = candidate.strip()
            candidate = re.sub(r'\s+', ' ', candidate)

            # Whitelist bypass
            if candidate in KNOWN_REAL_SKILLS:
                if re.search(
                    r'\b' + re.escape(candidate) + r'\b', text_lower
                ):
                    found_skills.add(candidate)
                continue

            # Filters
            if not (2 <= len(candidate) <= 35):
                continue
            if len(candidate.split()) > 4:
                continue
            if any(ch.isdigit() for ch in candidate):
                continue
            if ':' in candidate:
                continue
            if candidate in STOP_WORDS:
                continue
            if candidate in SECTION_HEADERS:
                continue
            if candidate in NOISE_WORDS:
                continue
            words = candidate.split()
            if all(w in NOISE_WORDS or w in STOP_WORDS for w in words):
                continue
            if not any(len(w) >= 3 for w in words):
                continue

            if re.search(
                r'\b' + re.escape(candidate) + r'\b', text_lower
            ):
                found_skills.add(candidate)

    # Layer 2: SKILLS_DATABASE fallback
    for skill in SKILLS_DATABASE:
        if skill not in found_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)

    # Layer 3: Exact match short skills
    for skill in EXACT_MATCH_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    return list(found_skills)


# ─────────────────────────────────────────────
# PROCESS FUNCTIONS
# ─────────────────────────────────────────────
def process_resume(text, jd_text=None):
    return {
        "name":       extract_candidate_name(text),
        "email":      extract_candidate_email(text),
        "phone":      extract_candidate_phone(text),
        "skills":     extract_skills(text, jd_text),
        "education":  extract_education(text),
        "experience": extract_experience(text)
    }


def process_jd(text):
    return {
        "all_skills": extract_skills(text, text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }


# ─────────────────────────────────────────────
# EMAIL EXTRACTION
# ─────────────────────────────────────────────
def extract_candidate_email(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    return emails[0] if emails else "Not provided"

# ─────────────────────────────────────────────
# PHONE EXTRACTION
# ─────────────────────────────────────────────
def extract_candidate_phone(text):
    """
    Extracts phone number from resume text.
    Handles Indian (+91), US, and general formats.
    """
    patterns = [
        r'\+91[\s\-]?\d{5}[\s\-]?\d{5}',        # +91 99999 99999
        r'\+91[\s\-]?\d{10}',                      # +91 9999999999
        r'\b91[\s\-]?\d{10}\b',                    # 91 9999999999
        r'\+\d{1,3}[\s\-]?\d{9,12}',              # general international
        r'\b\d{10}\b',                              # plain 10 digit
        r'\(\d{3}\)[\s\-]?\d{3}[\s\-]?\d{4}',    # (123) 456-7890
        r'\b\d{3}[\s\-]\d{3}[\s\-]\d{4}\b',       # 123-456-7890
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group().strip()
    return "Not provided"