from src.parser import extract_text_from_pdf
from src.matcher import match_resume_to_jd

jd_text = extract_text_from_pdf('data/job_descriptions/Senior_Data_Engineer_JD.pdf')
resume_text = extract_text_from_pdf('data/resumes/LAKSHAY GOEL_Data_Engineer.pdf')

result = match_resume_to_jd(jd_text, resume_text)

print('Final Score:   ', result['final_score'], '%')
print('TF-IDF Score:  ', result['tfidf_score'], '%')
print('BERT Score:    ', result['bert_score'], '%')
print('Skill Score:   ', result['skill_score'], '%')
print('Matched Skills:', result['matched_skills'])
print('Missing Skills:', result['missing_skills'])