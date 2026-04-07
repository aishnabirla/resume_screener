from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from src.nlp import extract_skills
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------------------
# EMBEDDING CACHE
# ---------------------------
skill_embedding_cache = {}

def get_embedding(skill):
    if skill not in skill_embedding_cache:
        skill_embedding_cache[skill] = model.encode(skill)
    return skill_embedding_cache[skill]

def semantic_skill_similarity(skill1, skill2):
    try:
        emb1 = get_embedding(skill1)
        emb2 = get_embedding(skill2)
        return cosine_similarity([emb1], [emb2])[0][0]
    except:
        return 0.0


# ---------------------------
# TF-IDF
# ---------------------------
def calculate_tfidf_score(jd_text, resume_text):
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform([jd_text, resume_text])
        return cosine_similarity(vectors[0], vectors[1])[0][0]
    except:
        return 0.0


# ---------------------------
# BERT
# ---------------------------
def calculate_bert_score(jd_text, resume_text):
    try:
        emb = model.encode([jd_text, resume_text], show_progress_bar=False)
        return cosine_similarity([emb[0]], [emb[1]])[0][0]
    except:
        return 0.0


# ---------------------------
# EQUIVALENT SKILLS
# ---------------------------
EQUIVALENT_SKILLS = [
    {"spark", "pyspark", "apache spark"},
    {"kafka", "apache kafka"},
    {"airflow", "apache airflow"},
    {"hadoop", "apache hadoop"},
    {"postgres", "postgresql"},
    {"git", "github"},
    {"etl", "elt"},
    {"kubernetes", "k8s"},
    {"ci/cd", "jenkins", "cicd"},
    {"databricks", "delta lake"},
    {"ml", "machine learning", "ai/ml", "artificial intelligence"},
    {"redshift", "aws redshift"},
    {"bigquery", "google bigquery"},
]

SKILL_FAMILIES = {
    "data_engineering": ["etl", "elt", "data pipeline", "airflow"],
    "big_data": ["spark", "pyspark", "hadoop", "kafka"],
    "cloud": ["aws", "azure", "gcp"],
    "ml": ["ml", "ai", "machine learning", "ai/ml"],
    "data_storage": ["snowflake", "redshift", "bigquery", "databricks"]
}

def same_family(s1, s2):
    for family in SKILL_FAMILIES.values():
        if s1 in family and s2 in family:
            return True
    return False


# ---------------------------
# SKILL MATCH (SELF-LEARNING)
# ---------------------------
def skills_match_score(skill1, skill2):
    s1 = skill1.lower().strip()
    s2 = skill2.lower().strip()

    if s1 == s2:
        return 1.0

    if len(s1) > 3 and len(s2) > 3:
        if s1 in s2 or s2 in s1:
            return 0.9

    for group in EQUIVALENT_SKILLS:
        if s1 in group and s2 in group:
            return 0.75

    if same_family(s1, s2):
        return 0.6

    # semantic fallback (self-learning)
    sim = semantic_skill_similarity(s1, s2)

    if sim > 0.80:
        return 0.85
    elif sim > 0.65:
        return 0.7
    elif sim > 0.50:
        return 0.5

    return 0.0


# ---------------------------
# SKILL WEIGHTING
# ---------------------------
def get_skill_weight(skill):
    skill = skill.lower()

    core = ["python", "sql", "spark", "pyspark", "airflow", "kafka", "etl", "elt", "data modeling"]
    important = ["aws", "azure", "databricks", "docker", "kubernetes"]
    optional = ["sap", "salesforce", "workday", "snowflake", "bigquery",
                "redshift", "gcp", "pandas", "ai", "ml", "ai/ml", "data quality"]

    if any(k in skill for k in core):
        return 1.0
    elif any(k in skill for k in important):
        return 0.7
    elif any(k in skill for k in optional):
        return 0.3

    return 0.5


# ---------------------------
# SECTION SPLIT
# ---------------------------
def split_jd_sections(jd_text):
    jd = jd_text.lower()
    for delimiter in ["nice-to-have", "nice to have", "preferred qualifications", "good to have"]:
        if delimiter in jd:
            parts = jd.split(delimiter)
            return parts[0], parts[1]
    return jd, ""


# ---------------------------
# SKILL SCORE
# ---------------------------
def calculate_skill_score(jd_text, resume_text):
    try:
        required_text, preferred_text = split_jd_sections(jd_text)

        req_skills = list(set(extract_skills(required_text, required_text)))
        pref_skills = list(set(extract_skills(preferred_text, preferred_text))) if preferred_text else []
        resume_skills = list(set(extract_skills(resume_text, jd_text)))

        total_weight = 0
        matched_weight = 0
        missing = []
        matched_all = []

        for jd_skill in req_skills:
            weight = get_skill_weight(jd_skill)
            total_weight += weight

            best_score = max(
                [skills_match_score(jd_skill, rs) for rs in resume_skills],
                default=0
            )

            if best_score > 0:
                matched_weight += best_score * weight
                matched_all.append(jd_skill)
            else:
                missing.append(jd_skill)

        req_score = matched_weight / total_weight if total_weight else 0

        matched_pref = [
            skill for skill in pref_skills
            if any(skills_match_score(skill, rs) > 0 for rs in resume_skills)
        ]

        pref_score = len(matched_pref) / len(pref_skills) if pref_skills else 0

        final_skill_score = (0.85 * req_score) + (0.15 * pref_score)

        matched_all.extend(matched_pref)

        return round(final_skill_score, 4), matched_all, missing

    except Exception as e:
        print(f"Skill error: {e}")
        return 0.0, [], []


# ---------------------------
# EXPERIENCE
# ---------------------------
def calculate_experience_score(jd_text, resume_text):
    try:
        jd = jd_text.lower()
        res = resume_text.lower()

        jd_range = re.findall(r'(\d+)\s*[-to]+\s*(\d+)\s*years?', jd)
        res_years = re.findall(r'(\d+)\+?\s*years?', res)

        if not res_years:
            return 0.5

        candidate = max([int(x) for x in res_years if int(x) < 50])

        if jd_range:
            jd_min, jd_max = int(jd_range[0][0]), int(jd_range[0][1])
        else:
            return 0.6

        if jd_min <= candidate <= jd_max:
            return 1.0
        elif candidate > jd_max:
            return 0.9
        elif candidate >= jd_min - 2:
            return 0.7
        else:
            return 0.4

    except:
        return 0.5


# ---------------------------
# TITLE
# ---------------------------
def calculate_title_score(jd_text, resume_text):
    try:
        jd = jd_text.lower()
        res = resume_text.lower()

        roles = ["data engineer", "software engineer", "data scientist"]

        jd_role = next((r for r in roles if r in jd), None)
        res_role = next((r for r in roles if r in res), None)

        if not jd_role or not res_role:
            return 0.5

        if jd_role == res_role:
            return 1.0
        elif jd_role in res_role or res_role in jd_role:
            return 0.85
        else:
            return 0.4

    except:
        return 0.5


# ---------------------------
# FINAL SCORE
# ---------------------------
def calculate_final_score(tfidf, bert, skill, exp=0.5, title=0.5):
    return round((
        tfidf * 0.05 +
        bert * 0.35 +
        skill * 0.35 +
        exp * 0.15 +
        title * 0.10
    ) * 100, 2)


# ---------------------------
# MAIN
# ---------------------------
def match_resume_to_jd(jd_text, resume_text):
    tfidf = calculate_tfidf_score(jd_text, resume_text)
    bert = calculate_bert_score(jd_text, resume_text)
    skill, matched, missing = calculate_skill_score(jd_text, resume_text)
    exp = calculate_experience_score(jd_text, resume_text)
    title = calculate_title_score(jd_text, resume_text)

    final = calculate_final_score(tfidf, bert, skill, exp, title)

    return {
        "final_score": final,
        "tfidf_score": round(tfidf * 100, 2),
        "bert_score": round(bert * 100, 2),
        "skill_score": round(skill * 100, 2),
        "experience_score": round(exp * 100, 2),
        "title_score": round(title * 100, 2),
        "matched_skills": matched,
        "missing_skills": missing
    }


# ---------------------------
# RANKING
# ---------------------------
def rank_resumes(jd_text, resumes):
    results = []

    for resume in resumes:
        match = match_resume_to_jd(jd_text, resume["text"])

        results.append({
            "name": resume["name"],
            "email": resume["email"],
            "file_name": resume["file_name"],
            "final_score": match["final_score"],
            "tfidf_score": match["tfidf_score"],
            "bert_score": match["bert_score"],
            "skill_score": match["skill_score"],
            "experience_score": match["experience_score"],
            "title_score": match["title_score"],
            "matched_skills": match["matched_skills"],
            "missing_skills": match["missing_skills"]
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results