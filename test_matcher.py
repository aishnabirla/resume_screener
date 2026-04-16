# from src.parser import extract_text_from_pdf
# from src.matcher import match_resume_to_jd

# jd_text = extract_text_from_pdf('data/job_descriptions/Senior_Data_Engineer_JD.pdf')
# resume_text = extract_text_from_pdf('data/resumes/LAKSHAY GOEL_Data_Engineer.pdf')

# result = match_resume_to_jd(jd_text, resume_text)

# print('Final Score:   ', result['final_score'], '%')
# print('TF-IDF Score:  ', result['tfidf_score'], '%')
# print('BERT Score:    ', result['bert_score'], '%')
# print('Skill Score:   ', result['skill_score'], '%')
# print('Matched Skills:', result['matched_skills'])
# print('Missing Skills:', result['missing_skills'])





from src.parser import extract_text_from_pdf
from src.nlp import extract_candidate_name

files = [
    'data/resumes/MOHAMMED FARIDH_Data_Engineer.pdf',
    'data/resumes/Bharath Servicenow HRSD.pdf',
]
for f in files:
    from src.parser import extract_text_from_pdf
    text = extract_text_from_pdf(f)
    print(f.split('/')[-1], '->', extract_candidate_name(text))



# from src.nlp import _collapse_spaced_name
# text = 'MOHAMMEDFARIDH AI DATA ENGINEER'
# proc = _collapse_spaced_name(text)
# print(repr(proc))
# import re
# word = 'Mohammedfaridh'
# parts = re.findall(r'[A-Z][a-z]+', word)
# print('Parts:', parts)
