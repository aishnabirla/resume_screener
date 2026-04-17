import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resume_screener.db')
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resume_screener.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def save_job_description(user_id, title, content):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO job_descriptions (user_id, title, content) VALUES (?, ?, ?)",
        (user_id, title, content)
    )
    jd_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jd_id


def save_resume(jd_id, candidate_name, candidate_email, file_name, raw_text):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO resumes
        (jd_id, candidate_name, candidate_email, file_name, raw_text)
        VALUES (?, ?, ?, ?, ?)""",
        (jd_id, candidate_name, candidate_email, file_name, raw_text)
    )
    resume_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return resume_id


def save_evaluation(resume_id, jd_id, match_score, matched_skills, missing_skills, education, experience):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO evaluations
        (resume_id, jd_id, match_score, matched_skills, missing_skills, education, experience)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (resume_id, jd_id, match_score,
         ", ".join(matched_skills),
         ", ".join(missing_skills),
         education, experience)
    )
    conn.commit()
    conn.close()


def get_evaluations_by_jd(jd_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT e.*, r.candidate_name, r.candidate_email, r.file_name
        FROM evaluations e
        JOIN resumes r ON e.resume_id = r.id
        WHERE e.jd_id = ?
        ORDER BY e.match_score DESC""",
        (jd_id,)
    )
    results = cursor.fetchall()
    conn.close()
    return results


def get_resume_by_id(resume_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes WHERE id = ?", (resume_id,))
    resume = cursor.fetchone()
    conn.close()
    return resume


def get_job_description_by_id(jd_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_descriptions WHERE id = ?", (jd_id,))
    jd = cursor.fetchone()
    conn.close()
    return jd


def get_all_job_descriptions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM job_descriptions WHERE user_id = ? ORDER BY uploaded_at DESC",
        (user_id,)
    )
    jds = cursor.fetchall()
    conn.close()
    return jds


def get_all_resumes_by_jd(jd_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM resumes WHERE jd_id = ? ORDER BY uploaded_at DESC",
        (jd_id,)
    )
    resumes = cursor.fetchall()
    conn.close()
    return resumes


def delete_job_description(jd_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM evaluations WHERE jd_id = ?", (jd_id,))
    cursor.execute("DELETE FROM resumes WHERE jd_id = ?", (jd_id,))
    cursor.execute("DELETE FROM job_descriptions WHERE id = ?", (jd_id,))
    conn.commit()
    conn.close()