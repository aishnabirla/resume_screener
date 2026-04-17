# import streamlit as st
# import pandas as pd
# import os
# import tempfile
# from src.auth import login_user, logout_user, is_logged_in, get_current_user
# from src.auth import generate_otp, send_otp_email, reset_password, signup_user
# from src.parser import extract_text_from_pdf, extract_text_from_string
# from src.nlp import process_resume, process_jd
# from src.matcher import match_resume_to_jd, rank_resumes
# from src.database import (save_job_description, save_resume,
#                            save_evaluation, get_evaluations_by_jd,
#                            get_job_description_by_id)
# from src.exporter import export_csv, export_pdf, export_excel

# st.set_page_config(
#     page_title="HireIQ",
#     page_icon="🔍",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

#     html, body, [class*="css"] {
#         font-family: 'DM Sans', sans-serif;
#         background-color: #f5f7fa;
#     }

#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}

#     .main .block-container {
#         padding-top: 1.5rem;
#         padding-bottom: 2rem;
#         max-width: 1000px;
#     }

#     /* ── Login ── */
#     .brand-title {
#         font-size: 2.6rem;
#         font-weight: 700;
#         color: #1a73e8;
#         text-align: center;
#         letter-spacing: -1px;
#     }
#     .brand-sub {
#         font-size: 0.95rem;
#         color: #888;
#         text-align: center;
#         margin-bottom: 1.8rem;
#     }
#     .login-card {
#         background: white;
#         padding: 2.2rem 2.4rem;
#         border-radius: 18px;
#         box-shadow: 0 4px 28px rgba(0,0,0,0.07);
#     }

#     /* ── Progress Bar ── */
#     .progress-wrap {
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 0;
#         margin-bottom: 2rem;
#         background: white;
#         padding: 1rem 2rem;
#         border-radius: 14px;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#     }
#     .step-pill {
#         display: flex;
#         align-items: center;
#         gap: 8px;
#         padding: 8px 20px;
#         border-radius: 30px;
#         font-size: 0.85rem;
#         font-weight: 500;
#         color: #aaa;
#         background: #f5f7fa;
#         border: 2px solid transparent;
#         transition: all 0.3s;
#         white-space: nowrap;
#     }
#     .step-pill.active {
#         color: #1a73e8;
#         background: #e8f0fe;
#         border-color: #1a73e8;
#         font-weight: 600;
#     }
#     .step-pill.done {
#         color: #34a853;
#         background: #e6f4ea;
#         border-color: #34a853;
#     }
#     .step-num {
#         width: 22px;
#         height: 22px;
#         border-radius: 50%;
#         display: inline-flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 0.75rem;
#         font-weight: 700;
#         background: currentColor;
#     }
#     .step-line {
#         flex: 0 0 40px;
#         height: 2px;
#         background: #e0e0e0;
#         margin: 0 4px;
#     }
#     .step-line.done {
#         background: #34a853;
#     }

#     /* ── Top bar ── */
#     .topbar {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         background: white;
#         padding: 0.9rem 1.5rem;
#         border-radius: 14px;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#         margin-bottom: 1.4rem;
#     }
#     .topbar-brand { font-size: 1.3rem; font-weight: 700; color: #1a73e8; }
#     .topbar-user { font-size: 0.85rem; color: #666; }

#     /* ── Cards ── */
#     .card {
#         background: white;
#         border-radius: 14px;
#         padding: 1.4rem 1.6rem;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#         margin-bottom: 1rem;
#     }
#     .card-title {
#         font-size: 1rem;
#         font-weight: 600;
#         color: #333;
#         margin-bottom: 1rem;
#         padding-bottom: 0.6rem;
#         border-bottom: 2px solid #e8f0fe;
#     }
#     .info-chip {
#         display: inline-block;
#         background: #e8f0fe;
#         color: #1a73e8;
#         padding: 4px 12px;
#         border-radius: 20px;
#         font-size: 0.82rem;
#         font-weight: 500;
#         margin: 2px;
#     }

#     /* ── JD Preview Modal ── */
#     .jd-preview-box {
#         background: #f8f9fa;
#         border: 1px solid #e0e0e0;
#         border-radius: 10px;
#         padding: 1.2rem;
#         font-size: 0.88rem;
#         color: #444;
#         line-height: 1.7;
#         max-height: 300px;
#         overflow-y: auto;
#         white-space: pre-wrap;
#         margin-top: 0.8rem;
#     }

#     /* ── Result cards ── */
#     .result-card {
#         background: white;
#         border-radius: 14px;
#         padding: 1.3rem 1.5rem;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#         margin-bottom: 1rem;
#         border-left: 5px solid #1a73e8;
#         transition: box-shadow 0.2s;
#     }
#     .result-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
#     .result-card.high { border-left-color: #34a853; }
#     .result-card.medium { border-left-color: #fbbc04; }
#     .result-card.low { border-left-color: #ea4335; }

#     .result-name {
#         font-size: 1.05rem;
#         font-weight: 600;
#         color: #222;
#     }
#     .result-score {
#         font-size: 1.6rem;
#         font-weight: 700;
#         color: #1a73e8;
#     }
#     .score-label {
#         font-size: 0.75rem;
#         color: #999;
#         font-weight: 400;
#     }

#     /* Skill badges */
#     .badge-matched {
#         display: inline-block;
#         background: #e6f4ea;
#         color: #2d7a4f;
#         padding: 3px 10px;
#         border-radius: 20px;
#         font-size: 0.78rem;
#         margin: 2px;
#         font-weight: 500;
#     }
#     .badge-missing {
#         display: inline-block;
#         background: #fce8e6;
#         color: #c5221f;
#         padding: 3px 10px;
#         border-radius: 20px;
#         font-size: 0.78rem;
#         margin: 2px;
#         font-weight: 500;
#     }

#     /* Table styling */
#     .stDataFrame { border-radius: 12px; overflow: hidden; }

#     /* Rank badge */
#     .rank-badge {
#         display: inline-flex;
#         align-items: center;
#         justify-content: center;
#         width: 28px;
#         height: 28px;
#         border-radius: 50%;
#         background: #1a73e8;
#         color: white;
#         font-size: 0.8rem;
#         font-weight: 700;
#         margin-right: 8px;
#     }

#     /* Button tweaks */
#     .stButton > button {
#         border-radius: 8px;
#         font-weight: 500;
#         font-family: 'DM Sans', sans-serif;
#     }
# </style>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# #  PROGRESS BAR
# # ─────────────────────────────────────────────
# def show_progress_bar(current_step):
#     steps = ["Upload JD", "Upload Resumes", "Evaluate"]
#     pills = ""
#     for i, label in enumerate(steps):
#         num = i + 1
#         if num < current_step:
#             css = "step-pill done"
#             icon = "✓"
#         elif num == current_step:
#             css = "step-pill active"
#             icon = str(num)
#         else:
#             css = "step-pill"
#             icon = str(num)

#         pills += f'<div class="{css}"><span>{icon}</span> Step {num}: {label}</div>'
#         if i < len(steps) - 1:
#             line_cls = "step-line done" if num < current_step else "step-line"
#             pills += f'<div class="{line_cls}"></div>'

#     st.markdown(
#         f'<div class="progress-wrap">{pills}</div>',
#         unsafe_allow_html=True
#     )


# # ─────────────────────────────────────────────
# #  TOP BAR
# # ─────────────────────────────────────────────
# def show_topbar(user, show_new_eval=False):
#     col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
#     with col1:
#         st.markdown('<div class="topbar-brand">🔍 HireIQ</div>', unsafe_allow_html=True)
#     with col2:
#         st.markdown(
#             f'<div class="topbar-user">👤 {user["name"]} &nbsp;|&nbsp; {user["email"]}</div>',
#             unsafe_allow_html=True
#         )
#     with col3:
#         if show_new_eval:
#             if st.button("+ New Evaluation", type="primary", use_container_width=True):
#                 st.session_state['page'] = 'dashboard'
#                 st.session_state['wizard_step'] = 1
#                 st.session_state['results'] = None
#                 st.session_state['jd_text'] = None
#                 st.session_state['jd_title'] = None
#                 st.rerun()
#     with col4:
#         if st.button("Logout", use_container_width=True):
#             logout_user()
#             st.rerun()

# # ─────────────────────────────────────────────
# #  LOGIN PAGE
# # ─────────────────────────────────────────────
# def show_login_page():
#     col1, col2, col3 = st.columns([1, 1.2, 1])
#     with col2:
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.markdown('<div class="brand-title">🔍 HireIQ</div>', unsafe_allow_html=True)
#         st.markdown('<div class="brand-sub">AI-Powered Resume Screener</div>', unsafe_allow_html=True)

#         tab1, tab2, tab3 = st.tabs(["Sign In", "Sign Up", "Forgot Password"])

#         with tab1:
#             with st.form("login_form"):
#                 email = st.text_input(
#                     "Email Address",
#                     placeholder="you@example.com"
#                 )
#                 password = st.text_input(
#                     "Password",
#                     type="password",
#                     placeholder="Enter your password"
#                 )
#                 st.markdown("<br>", unsafe_allow_html=True)
#                 submitted = st.form_submit_button(
#                     "Sign In",
#                     use_container_width=True,
#                     type="primary"
#                 )
#                 if submitted:
#                     if email and password:
#                         success, result = login_user(email, password)
#                         if success:
#                             st.session_state.update({
#                                 'logged_in': True,
#                                 'user': result,
#                                 'page': 'dashboard',
#                                 'wizard_step': 1
#                             })
#                             st.rerun()
#                         else:
#                             st.error(result)
#                     else:
#                         st.warning("Please enter both email and password")

#         with tab2:
#             with st.form("signup_form"):
#                 new_name = st.text_input("Full Name", placeholder="e.g. Your name", key="su_name")
#                 new_email = st.text_input("Email Address", placeholder="you@example.com", key="su_email")
#                 new_pw = st.text_input("Password", type="password", placeholder="Minimum 6 characters", key="su_pw")
#                 confirm_pw = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="su_confirm")
#                 st.markdown("<br>", unsafe_allow_html=True)
#                 submitted = st.form_submit_button(
#                     "Create Account",
#                     use_container_width=True,
#                     type="primary"
#                 )
#                 if submitted:
#                     if new_pw != confirm_pw:
#                         st.error("Passwords do not match")
#                     else:
#                         success, message = signup_user(new_name, new_email, new_pw)
#                         if success:
#                             st.success(message)
#                             st.info("Go to Sign In tab to login")
#                         else:
#                             st.error(message)

#         with tab3:
#             fp_email = st.text_input("Registered Email", key="fp_email")
#             if 'otp_sent' not in st.session_state:
#                 st.session_state['otp_sent'] = False
#             if st.button("Send OTP", use_container_width=True, key="otp_btn"):
#                 if fp_email:
#                     otp = generate_otp()
#                     sent = send_otp_email(fp_email, otp)
#                     if sent:
#                         st.session_state.update({'otp_sent': True, 'generated_otp': otp, 'fp_email_stored': fp_email})
#                         st.success("OTP sent!")
#                     else:
#                         st.info("Email not configured. Contact admin to reset password.")
#                 else:
#                     st.warning("Please enter your email")
#             if st.session_state.get('otp_sent'):
#                 otp_in = st.text_input("Enter OTP", key="otp_in")
#                 np1 = st.text_input("New Password", type="password", key="np1")
#                 np2 = st.text_input("Confirm Password", type="password", key="np2")
#                 if st.button("Reset Password", use_container_width=True, key="reset_btn"):
#                     if otp_in == st.session_state.get('generated_otp'):
#                         if np1 == np2 and len(np1) >= 6:
#                             reset_password(st.session_state['fp_email_stored'], np1)
#                             st.success("Password reset! Please sign in.")
#                             st.session_state['otp_sent'] = False
#                         else:
#                             st.error("Passwords do not match or too short")
#                     else:
#                         st.error("Incorrect OTP")

#         st.markdown('</div>', unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# #  DASHBOARD
# # ─────────────────────────────────────────────
# def show_dashboard():
#     user = get_current_user()
#     show_topbar(user)

#     if 'wizard_step' not in st.session_state:
#         st.session_state['wizard_step'] = 1
#     if 'jd_text' not in st.session_state:
#         st.session_state['jd_text'] = None
#     if 'jd_title' not in st.session_state:
#         st.session_state['jd_title'] = None

#     show_progress_bar(st.session_state['wizard_step'])

#     step = st.session_state['wizard_step']
#     if step == 1:
#         show_step1()
#     elif step == 2:
#         show_step2()
#     elif step == 3:
#         show_step3()


# # ─────────────────────────────────────────────
# #  STEP 1 — JD Upload
# # ─────────────────────────────────────────────
# def show_step1():
#     st.markdown('<div class="card"><div class="card-title">📋 Job Description</div>', unsafe_allow_html=True)

#     jd_title = st.text_input(
#         "Job Title",
#         placeholder="e.g. Software Engineer, Data Analyst, Graphic Designer, Sales Executive",
#         value=st.session_state.get('jd_title', '')
#     )

#     st.markdown("<br>", unsafe_allow_html=True)
#     jd_option = st.radio(
#         "How would you like to provide the JD?",
#         ["Upload a file (PDF or TXT)", "Paste as text"],
#         horizontal=True
#     )

#     jd_text = None

#     if jd_option == "Upload a file (PDF or TXT)":
#         jd_file = st.file_uploader("Upload Job Description", type=["pdf", "txt"])
#         if jd_file:
#             if jd_file.name.endswith('.pdf'):
#                 with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
#                     tmp.write(jd_file.read())
#                     tmp_path = tmp.name
#                 jd_text = extract_text_from_pdf(tmp_path)
#                 os.unlink(tmp_path)
#             else:
#                 jd_text = extract_text_from_string(jd_file.read().decode('utf-8'))
#             st.success(f"Loaded: {jd_file.name}")
#     else:
#         jd_input = st.text_area(
#             "Paste job description here",
#             height=200,
#             placeholder="We are looking for ..."
#         )
#         if jd_input.strip():
#             jd_text = extract_text_from_string(jd_input)

#     # JD Preview Toggle
#     if jd_text:
#         if st.button("👁 View Job Description"):
#             st.session_state['show_jd_preview'] = not st.session_state.get('show_jd_preview', False)
#         if st.session_state.get('show_jd_preview', False):
#             st.markdown(f'<div class="jd-preview-box">{jd_text}</div>', unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)
#     st.markdown("<br>", unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([2, 1, 2])
#     with col2:
#         if st.button("Next →", type="primary", use_container_width=True):
#             if not jd_title:
#                 st.error("Please enter a job title")
#             elif not jd_text:
#                 st.error("Please upload or paste a job description")
#             else:
#                 st.session_state['jd_title'] = jd_title
#                 st.session_state['jd_text'] = jd_text
#                 st.session_state['wizard_step'] = 2
#                 st.session_state['show_jd_preview'] = False
#                 st.rerun()


# # ─────────────────────────────────────────────
# #  STEP 2 — Resume Upload
# # ─────────────────────────────────────────────
# def show_step2():
#     st.markdown(
#         f'<div class="info-chip">📋 {st.session_state["jd_title"]}</div>',
#         unsafe_allow_html=True
#     )
#     st.markdown("<br>", unsafe_allow_html=True)

#     st.markdown('<div class="card"><div class="card-title">📄 Candidate Resumes</div>', unsafe_allow_html=True)

#     resume_files = st.file_uploader(
#         "Upload candidate resumes (PDF only)",
#         type=["pdf"],
#         accept_multiple_files=True,
#         help="You can select multiple PDFs at once"
#     )

#     if resume_files:
#         st.success(f"{len(resume_files)} resume(s) ready")
#         for i, f in enumerate(resume_files):
#             st.write(f"📄 {i+1}. {f.name}")

#     st.markdown('</div>', unsafe_allow_html=True)
#     st.markdown("<br>", unsafe_allow_html=True)

#     col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
#     with col2:
#         if st.button("← Back", use_container_width=True):
#             st.session_state['wizard_step'] = 1
#             st.rerun()
#     with col4:
#         if st.button("Next →", type="primary", use_container_width=True):
#             if not resume_files:
#                 st.error("Please upload at least one resume")
#             else:
#                 st.session_state['resume_files_data'] = [
#                     {"name": f.name, "data": f.read()} for f in resume_files
#                 ]
#                 st.session_state['wizard_step'] = 3
#                 st.rerun()


# # ─────────────────────────────────────────────
# #  STEP 3 — Evaluate
# # ─────────────────────────────────────────────
# def show_step3():
#     user = get_current_user()
#     resume_files_data = st.session_state.get('resume_files_data', [])

#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown(f'<div class="info-chip">📋 {st.session_state["jd_title"]}</div>', unsafe_allow_html=True)
#     with col2:
#         st.markdown(f'<div class="info-chip">👥 {len(resume_files_data)} candidate(s)</div>', unsafe_allow_html=True)

#     st.markdown("<br>", unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([2, 1, 2])
#     with col2:
#         evaluate = st.button("Initiate Evaluation", type="primary", use_container_width=True)

#     if evaluate:
#         jd_text = st.session_state['jd_text']
#         jd_title = st.session_state['jd_title']
#         progress_bar = st.progress(0)
#         status = st.empty()
#         jd_id = save_job_description(user['id'], jd_title, jd_text)
#         results = []

#         for i, resume_data in enumerate(resume_files_data):
#             status.info(f"⏳ Evaluating {resume_data['name']}... ({i+1}/{len(resume_files_data)})")
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
#                 tmp.write(resume_data['data'])
#                 tmp_path = tmp.name
#             resume_text = extract_text_from_pdf(tmp_path)
#             os.unlink(tmp_path)
#             resume_info = process_resume(resume_text, jd_text)
#             if resume_info['name'] in ("Candidate", "Unknown"):
#                 name_from_file = resume_data['name'].replace('.pdf', '').replace('_', ' ').replace('-', ' ').title()
#                 resume_info['name'] = name_from_file
#             resume_id = save_resume(jd_id, resume_info['name'], resume_info['email'], resume_data['name'], resume_text)
#             match_result = match_resume_to_jd(jd_text, resume_text)
#             save_evaluation(resume_id, jd_id, match_result['final_score'],
#                             match_result['matched_skills'], match_result['missing_skills'],
#                             resume_info['education'], resume_info['experience'])
#             results.append({
#                 "name": resume_info['name'],
#                 "email": resume_info['email'] or "Not provided",
#                 "file_name": resume_data['name'],
#                 "final_score": match_result['final_score'],
#                 "skill_score": match_result['skill_score'],
#                 "matched_skills": match_result['matched_skills'] or [],
#                 "missing_skills": match_result['missing_skills'] or [],
#                 "education": resume_info['education'] or "Not found",
#                 "experience": resume_info['experience'] or "Not found"
#             })
#             progress_bar.progress((i + 1) / len(resume_files_data))

#         results.sort(key=lambda x: x['final_score'], reverse=True)

#         for r in results:
#             r['name'] = r['name'] if r['name'] else "Unknown"
#             r['email'] = r['email'] if r['email'] else "Not provided"
#             r['education'] = r['education'] if r['education'] not in [None, "None", "none", ""] else "Not found"
#             r['experience'] = r['experience'] if r['experience'] not in [None, "None", "none", ""] else "Not found"
#             r['matched_skills'] = r['matched_skills'] if r['matched_skills'] else []
#             r['missing_skills'] = r['missing_skills'] if r['missing_skills'] else []

#         status.success("✅ Evaluation complete!")

#         # Normalise skills — convert stringified lists to real lists
#         def normalise_skills(val):
#             if isinstance(val, str) and val.startswith("["):
#                 import ast
#                 try:
#                     return ast.literal_eval(val)
#                 except Exception:
#                     return []
#             return val if isinstance(val, list) else []

#         for r in results:
#             r['matched_skills'] = normalise_skills(r['matched_skills'])
#             r['missing_skills'] = normalise_skills(r['missing_skills'])

#         st.session_state['results'] = results
#         st.session_state['page'] = 'results'
#         st.rerun()

#     col1, col2, col3 = st.columns([2, 1, 2])
#     with col2:
#         if st.button("← Back", use_container_width=True):
#             st.session_state['wizard_step'] = 2
#             st.rerun()

# # ─────────────────────────────────────────────
# #  RESULTS PAGE
# # ─────────────────────────────────────────────
# def show_results_page():
#     user = get_current_user()
#     show_topbar(user, show_new_eval=True)

#     results = st.session_state.get('results', [])
#     jd_title = st.session_state.get('jd_title', 'Job Description')

#     st.markdown(f"### 📊 Results — {jd_title}")
#     st.markdown(f"**{len(results)} candidate(s) evaluated and ranked**")
#     st.markdown("---")

#     ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 1.5])
#     with ctrl1:
#         min_score = st.slider("Min score filter", 0, 100, 0, 5)
#     with ctrl2:
#         view_mode = st.radio("View", ["Cards", "Table"], horizontal=True)
#     with ctrl3:
#         if st.button("👁 View JD"):
#             st.session_state['show_jd_results'] = not st.session_state.get('show_jd_results', False)

#     if st.session_state.get('show_jd_results', False):
#         st.markdown(
#             f'<div class="jd-preview-box">{st.session_state["jd_text"]}</div>',
#             unsafe_allow_html=True
#         )
#         st.markdown("<br>", unsafe_allow_html=True)

#     filtered = [
#         r for r in results
#         if isinstance(r.get('final_score'), (int, float)) and r['final_score'] >= min_score
#     ]
#     filtered = [r for r in filtered if r is not None]
#     filtered.sort(key=lambda x: x['final_score'], reverse=True)

#     st.markdown(f"*Showing {len(filtered)} candidate(s)*")
#     st.markdown("---")

#     # ── Card View ──
#     if view_mode == "Cards":
#         for i, c in enumerate(filtered):
#             score = c['final_score']
#             badge = "🟢 Strong" if score >= 70 else "🟡 Partial" if score >= 40 else "🔴 Weak"

#             with st.expander(
#                 f"#{i+1}  {c['name']}  —  {score}%  {badge}",
#                 expanded=(i == 0)
#             ):
#                 left, right = st.columns([1, 2])
#                 with left:
#                     st.metric("Final Score", f"{score}%")
#                     st.metric("Skill Match", f"{c['skill_score']}%")
#                     st.caption(f"Email: {c['email']}")
#                     st.caption(f"Resume: {c['file_name']}")
#                 with right:
#                     st.markdown("**✅ Matched Skills**")
#                     if c['matched_skills']:
#                         badges = " ".join([
#                             f'<span class="badge-matched">{s}</span>'
#                             for s in c['matched_skills']
#                         ])
#                         st.markdown(badges, unsafe_allow_html=True)
#                     else:
#                         st.caption("None matched")

#                     st.markdown("<br>", unsafe_allow_html=True)
#                     st.markdown("**❌ Missing Skills**")
#                     if c['missing_skills']:
#                         badges = " ".join([
#                             f'<span class="badge-missing">{s}</span>'
#                             for s in c['missing_skills']
#                         ])
#                         st.markdown(badges, unsafe_allow_html=True)
#                     else:
#                         st.caption("No missing skills")

#                 st.markdown("---")
#                 edu = c['education']
#                 exp = c['experience']
#                 if edu and edu not in ['None', 'Not found', 'none']:
#                     st.caption(f"Education: {edu}")
#                 if exp and exp not in ['None', 'Not found', 'none']:
#                     st.caption(f"Experience: {exp}")

#     # ── Table View ──
#     else:
#         df = pd.DataFrame([{
#             "Rank": i + 1,
#             "Name": r['name'],
#             "Email": r['email'],
#             "Final Score (%)": r['final_score'],
#             "Skill Match (%)": r['skill_score'],
#             "Matched Skills": ", ".join(r['matched_skills']) if isinstance(r['matched_skills'], list) else str(r['matched_skills']),
#             "Missing Skills": ", ".join(r['missing_skills']) if isinstance(r['missing_skills'], list) else str(r['missing_skills']),
#         } for i, r in enumerate(filtered)])
#         st.dataframe(df, use_container_width=True, hide_index=True)

#     # ── Export ──
#     st.markdown("---")
#     st.markdown("### 📌 Export Results")

#     exp1, exp2, exp3 = st.columns(3)

#     with exp1:
#         st.download_button(
#             label="📥 Download CSV",
#             data=export_csv(filtered),
#             file_name=f"{jd_title}_results.csv",
#             mime="text/csv",
#             use_container_width=True
#         )

#     with exp2:
#         st.download_button(
#             label="📊 Download Excel",
#             data=export_excel(filtered, jd_title),
#             file_name=f"{jd_title}_results.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#             use_container_width=True
#         )

#     with exp3:
#         st.download_button(
#             label="📄 Download PDF",
#             data=export_pdf(filtered, jd_title),
#             file_name=f"{jd_title}_report.pdf",
#             mime="application/pdf",
#             use_container_width=True
#         )

# # ─────────────────────────────────────────────
# #  MAIN
# # ─────────────────────────────────────────────
# def main():
#     # FIX: initialise ALL session state keys upfront so no key is ever missing
#     # mid-render, which was causing session flicker on first load
#     defaults = {
#         'logged_in': False,
#         'page': 'login',
#         'user': None,
#         'wizard_step': 1,
#         'jd_text': None,
#         'jd_title': None,
#         'results': None,
#         'show_jd_preview': False,
#         'show_jd_results': False,
#         'otp_sent': False,
#     }
#     for key, val in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = val

#     if not st.session_state['logged_in']:
#         show_login_page()
#     elif st.session_state['page'] == 'results':
#         show_results_page()
#     else:
#         show_dashboard()


# if __name__ == "__main__":
#     main()





import streamlit as st
import pandas as pd
import re
import os
import tempfile
from src.parser import extract_text_from_pdf, extract_text_from_string
from src.nlp import process_resume, process_jd
from src.matcher import match_resume_to_jd, rank_resumes
from src.database import (save_job_description, save_resume,
                           save_evaluation, get_evaluations_by_jd,
                           get_job_description_by_id)
from src.exporter import export_csv, export_pdf, export_excel
from src.auth import (login_user, logout_user, is_logged_in,
                       get_current_user, generate_otp,
                       send_otp_email, reset_password, is_admin)
from src.matcher import is_valid_jd
from src.matcher import is_valid_resume
from src.nlp import JOB_TITLE_WORDS
st.set_page_config(
    page_title="HireIQ",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #f5f7fa;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }

    /* ── Login ── */
    .brand-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #1a73e8;
        text-align: center;
        letter-spacing: -1px;
    }
    .brand-sub {
        font-size: 0.95rem;
        color: #888;
        text-align: center;
        margin-bottom: 1.8rem;
    }
    .login-card {
        background: white;
        padding: 2.2rem 2.4rem;
        border-radius: 18px;
        box-shadow: 0 4px 28px rgba(0,0,0,0.07);
    }

    /* ── Progress Bar ── */
    .progress-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin-bottom: 2rem;
        background: white;
        padding: 1rem 2rem;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .step-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #aaa;
        background: #f5f7fa;
        border: 2px solid transparent;
        transition: all 0.3s;
        white-space: nowrap;
    }
    .step-pill.active {
        color: #1a73e8;
        background: #e8f0fe;
        border-color: #1a73e8;
        font-weight: 600;
    }
    .step-pill.done {
        color: #34a853;
        background: #e6f4ea;
        border-color: #34a853;
    }
    .step-num {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        background: currentColor;
    }
    .step-line {
        flex: 0 0 40px;
        height: 2px;
        background: #e0e0e0;
        margin: 0 4px;
    }
    .step-line.done {
        background: #34a853;
    }

    /* ── Top bar ── */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        padding: 0.9rem 1.5rem;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1.4rem;
    }
    .topbar-brand { font-size: 1.3rem; font-weight: 700; color: #1a73e8; }
    .topbar-user { font-size: 0.85rem; color: #666; }

    /* ── Cards ── */
    .card {
        background: white;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
        padding-bottom: 0.6rem;
        border-bottom: 2px solid #e8f0fe;
    }
    .info-chip {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 2px;
    }

    /* ── JD Formatted Display ── */
    .jd-preview-box {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.4rem 1.6rem;
        font-size: 0.88rem;
        color: #333;
        line-height: 1.8;
        max-height: 400px;
        overflow-y: auto;
        margin-top: 0.8rem;
    }
    .jd-section-heading {
        font-size: 0.92rem;
        font-weight: 700;
        color: #1a73e8;
        margin-top: 1rem;
        margin-bottom: 0.3rem;
        padding-bottom: 0.2rem;
        border-bottom: 1px solid #e8f0fe;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .jd-bullet {
        padding: 0.15rem 0 0.15rem 1rem;
        color: #444;
        position: relative;
    }
    .jd-para {
        padding: 0.2rem 0;
        color: #555;
    }

    /* ── Result cards ── */
    .result-card {
        background: white;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border-left: 5px solid #1a73e8;
        transition: box-shadow 0.2s;
    }
    .result-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
    .result-card.high { border-left-color: #34a853; }
    .result-card.medium { border-left-color: #fbbc04; }
    .result-card.low { border-left-color: #ea4335; }

    .result-name {
        font-size: 1.05rem;
        font-weight: 600;
        color: #222;
    }
    .result-score {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a73e8;
    }
    .score-label {
        font-size: 0.75rem;
        color: #999;
        font-weight: 400;
    }

    /* Skill badges */
    .badge-matched {
        display: inline-block;
        background: #e6f4ea;
        color: #2d7a4f;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        margin: 2px;
        font-weight: 500;
    }
    .badge-missing {
        display: inline-block;
        background: #fce8e6;
        color: #c5221f;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        margin: 2px;
        font-weight: 500;
    }

    /* Table styling */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    /* Rank badge */
    .rank-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #1a73e8;
        color: white;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 8px;
    }

    /* Button tweaks */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        font-family: 'DM Sans', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

def show_admin_panel():
    from src.auth import (
        admin_create_user,
        admin_get_all_users,
        admin_delete_user,
        admin_reset_user_password,
        is_admin
    )

    if not is_admin():
        st.error("Access denied. Admin only.")
        return

    user = get_current_user()

    # ─────────────────────────────────────────────
    # TOP BAR (CUSTOM FOR ADMIN PANEL)
    # ─────────────────────────────────────────────
    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        st.markdown('<div class="topbar-brand">🔍 HireIQ</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(
            f'<div class="topbar-user">👤 {user["name"]} | {user["email"]}</div>',
            unsafe_allow_html=True
        )

    with col3:
        btn1, btn2 = st.columns(2)

        with btn1:
            if st.button("← Dashboard", use_container_width=True):
                st.session_state['page'] = 'dashboard'
                st.rerun()

        with btn2:
            if st.button("Logout", use_container_width=True):
                logout_user()
                st.rerun()

    # ─────────────────────────────────────────────
    # PAGE TITLE
    # ─────────────────────────────────────────────
    st.markdown("### Admin Panel — User Management")
    st.markdown("---")

    # ─────────────────────────────────────────────
    # CREATE USER
    # ─────────────────────────────────────────────
    st.markdown("#### Create New HR User")

    with st.form("create_user_form"):
        new_name = st.text_input("Full Name", placeholder="Your full name")
        new_email = st.text_input("Email Address", placeholder="email@example.com")
        new_password = st.text_input(
            "Temporary Password",
            type="password",
            placeholder="Minimum 6 characters"
        )
        new_role = st.selectbox("Role", ["hr", "admin"])

        create_submitted = st.form_submit_button(
            "Create Account",
            type="primary",
            use_container_width=True
        )

        if create_submitted:
            if not new_name or not new_email or not new_password:
                st.warning("Please fill all fields")
            else:
                success, message = admin_create_user(
                    new_name, new_email, new_password, new_role
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)

    st.markdown("---")

    # ─────────────────────────────────────────────
    # USERS LIST
    # ─────────────────────────────────────────────
    st.markdown("#### 👥 All Users")

    users = admin_get_all_users()

    if users:
        for u in users:
            col1, col2, col3, col4, col5 = st.columns([2, 2.5, 1, 1.5, 1])

            with col1:
                st.write(f"**{u['name']}**")

            with col2:
                st.write(u['email'])

            with col3:
                st.markdown(
                    f"<span style='background:#e8f0fe;color:#1a73e8;"
                    f"padding:4px 10px;border-radius:12px;font-size:0.75rem'>"
                    f"{u['role']}</span>",
                    unsafe_allow_html=True
                )

            with col4:
                st.caption(u['created_at'][:10])

            with col5:
                current = get_current_user()

                if u['email'] != current['email']:
                    if st.button("🗑 Delete", key=f"del_{u['id']}"):
                        admin_delete_user(u['id'])
                        st.rerun()
                else:
                    st.caption("You")

    else:
        st.info("No users found")

# ─────────────────────────────────────────────
#  PROGRESS BAR
# ─────────────────────────────────────────────

def format_jd_for_display(text):
    if not text:
        return ""

    lines = text.strip().split('\n')
    html_lines = []

    # Keywords that indicate a section heading
    # Matched using 'contains' not exact equality
    # so "Required Qualifications" matches "required"
    heading_keywords = [
        "responsibility", "responsibilities",
        "requirement", "requirements",
        "qualification", "qualifications",
        "preferred", "preference",
        "nice to have", "nice-to-have",
        "good to have",
        "must have", "must-have",
        "key skills", "technical skills",
        "skills required", "required skills",
        "education",
        "about the role", "about the job",
        "about us", "about the company",
        "who you are", "what you will do",
        "what you'll do", "what we offer",
        "benefits", "perks",
        "overview", "summary", "objective",
        "job description", "role", "position",
        "duties", "profile", "key responsibilities",
        "minimum qualifications",
        "basic qualifications",
        "additional qualifications",
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        line_lower = line.lower().strip().rstrip(':').strip()

        # Check 1: line ends with colon and is short
        ends_with_colon = line.endswith(':') and len(line) < 80

        # Check 2: line contains a heading keyword
        # Uses 'in' so "Required Qualifications" matches "requirement"
        contains_keyword = any(kw in line_lower for kw in heading_keywords)

        # Check 3: short ALL-CAPS line (e.g. "KEY SKILLS")
        is_all_caps = line.isupper() and len(line) < 60

        # Check 4: short line (under 55 chars) that contains a keyword
        # This catches "Nice to Have" or "Preferred" without colon
        is_short_keyword_line = (
            len(line) < 55
            and contains_keyword
            and not line.startswith(('•', '-', '*', '●', '○', '▪', '◦'))
        )

        is_heading = (
            ends_with_colon
            or is_all_caps
            or is_short_keyword_line
        )

        is_bullet = line.startswith(('•', '-', '*', '●', '○', '▪', '◦'))

        if is_heading:
            html_lines.append(
                f'<div class="jd-section-heading">{line}</div>'
            )
        elif is_bullet:
            content = line.lstrip('•-*●○▪◦').strip()
            html_lines.append(
                f'<div class="jd-bullet">• {content}</div>'
            )
        else:
            html_lines.append(
                f'<div class="jd-para">{line}</div>'
            )

    return '\n'.join(html_lines)

def show_progress_bar(current_step):
    steps = ["Upload JD", "Upload Resumes", "Evaluate"]
    pills = ""
    for i, label in enumerate(steps):
        num = i + 1
        if num < current_step:
            css = "step-pill done"
            icon = "✓"
        elif num == current_step:
            css = "step-pill active"
            icon = str(num)
        else:
            css = "step-pill"
            icon = str(num)

        pills += f'<div class="{css}"><span>{icon}</span> Step {num}: {label}</div>'
        if i < len(steps) - 1:
            line_cls = "step-line done" if num < current_step else "step-line"
            pills += f'<div class="{line_cls}"></div>'

    st.markdown(
        f'<div class="progress-wrap">{pills}</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
#  TOP BAR
# ─────────────────────────────────────────────
def show_topbar(user, show_new_eval=False):
    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
    with col1:
        st.markdown('<div class="topbar-brand">🔍 HireIQ</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(
            f'<div class="topbar-user">👤 {user["name"]} &nbsp;|&nbsp; {user["email"]}</div>',
            unsafe_allow_html=True
        )
    with col3:
        if show_new_eval:
            if st.button("+ New Evaluation", type="primary", use_container_width=True):
                st.session_state['page'] = 'dashboard'
                st.session_state['wizard_step'] = 1
                st.session_state['results'] = None
                st.session_state['jd_text'] = None
                st.session_state['jd_title'] = None
                st.rerun()
        elif user.get('role') == 'admin':
            if st.button("Admin Panel", use_container_width=True):
                st.session_state['page'] = 'admin'
                st.rerun()
    with col4:
        if st.button("Logout", use_container_width=True):
            logout_user()
            st.rerun()

# ─────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────
def show_login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="brand-title">🔍 HireIQ</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">AI-Powered Resume Screener</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("login_form"):
            st.markdown("**Sign in to your account**")
            st.markdown("<br>", unsafe_allow_html=True)
            email = st.text_input("Email Address", placeholder="you@example.com")
            password = st.text_input("Password", type="password",
                                     placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "Sign In", use_container_width=True, type="primary"
            )
            if submitted:
                if email and password:
                    success, result = login_user(email, password)
                    if success:
                        st.session_state.update({
                            'logged_in': True,
                            'user': result,
                            'page': 'dashboard',
                            'wizard_step': 1
                        })
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("Please enter both email and password")

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("Forgot Password?"):
            fp_email = st.text_input("Enter your registered email", key="fp_email")
            if 'otp_sent' not in st.session_state:
                st.session_state['otp_sent'] = False
            if st.button("Send OTP", use_container_width=True, key="otp_btn"):
                if fp_email:
                    otp = generate_otp()
                    sent = send_otp_email(fp_email, otp)
                    if sent:
                        st.session_state.update({
                            'otp_sent': True,
                            'generated_otp': otp,
                            'fp_email_stored': fp_email
                        })
                        st.success("OTP sent!")
                    else:
                        st.info("Email not configured. Contact your admin to reset password.")
                else:
                    st.warning("Please enter your email")
            if st.session_state.get('otp_sent'):
                otp_in = st.text_input("Enter OTP", key="otp_in")
                np1 = st.text_input("New Password", type="password", key="np1")
                np2 = st.text_input("Confirm Password", type="password", key="np2")
                if st.button("Reset Password", use_container_width=True, key="reset_btn"):
                    if otp_in == st.session_state.get('generated_otp'):
                        if np1 == np2 and len(np1) >= 6:
                            reset_password(st.session_state['fp_email_stored'], np1)
                            st.success("Password reset! Please sign in.")
                            st.session_state['otp_sent'] = False
                        else:
                            st.error("Passwords do not match or too short")
                    else:
                        st.error("Incorrect OTP")

# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────
def show_dashboard():
    user = get_current_user()
    show_topbar(user)

    if 'wizard_step' not in st.session_state:
        st.session_state['wizard_step'] = 1
    if 'jd_text' not in st.session_state:
        st.session_state['jd_text'] = None
    if 'jd_title' not in st.session_state:
        st.session_state['jd_title'] = None

    show_progress_bar(st.session_state['wizard_step'])

    step = st.session_state['wizard_step']
    if step == 1:
        show_step1()
    elif step == 2:
        show_step2()
    elif step == 3:
        show_step3()

# ─────────────────────────────────────────────
#  STEP 1 — JD Upload
# ─────────────────────────────────────────────
def show_step1():
    st.markdown('<div class="card"><div class="card-title">📋 Job Description</div>', unsafe_allow_html=True)

    jd_title = st.text_input(
        "Job Title",
        placeholder="e.g. Software Engineer, Data Analyst, Graphic Designer, Sales Executive",
        value=st.session_state.get('jd_title', '')
    )

    st.markdown("<br>", unsafe_allow_html=True)
    jd_option = st.radio(
        "How would you like to provide the JD?",
        ["Upload a file (PDF or TXT)", "Paste as text"],
        horizontal=True
    )

    jd_text = None

    if jd_option == "Upload a file (PDF or TXT)":
        jd_file = st.file_uploader("Upload Job Description", type=["pdf", "txt"])
        if jd_file:
            if jd_file.name.endswith('.pdf'):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    tmp.write(jd_file.read())
                    tmp_path = tmp.name
                jd_text = extract_text_from_pdf(tmp_path)
                os.unlink(tmp_path)
            else:
                jd_text = extract_text_from_string(jd_file.read().decode('utf-8'))
            st.success(f"Loaded: {jd_file.name}")
    else:
        jd_input = st.text_area(
            "Paste job description here",
            height=200,
            placeholder="We are looking for ..."
        )
        if jd_input.strip():
            jd_text = extract_text_from_string(jd_input)

    # JD Preview Toggle
    if jd_text:
        if st.button("👁 View Job Description"):
            st.session_state['show_jd_preview'] = not st.session_state.get('show_jd_preview', False)
        if st.session_state.get('show_jd_preview', False):
            st.markdown(f'<div class="jd-preview-box">{format_jd_for_display(jd_text)}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Next →", type="primary", use_container_width=True):
            if not jd_title:
                st.error("Please enter a job title")

            elif not jd_text:
                st.error("Please upload or paste a job description")

            elif not is_valid_jd(jd_text):   # MAIN FIX
                st.error("Invalid Job Description. Please provide a proper JD with roles, responsibilities, and requirements.")

            else:
                st.session_state['jd_title'] = jd_title
                st.session_state['jd_text'] = jd_text
                st.session_state['wizard_step'] = 2
                st.session_state['show_jd_preview'] = False
                st.rerun()

# ─────────────────────────────────────────────
#  STEP 2 — Resume Upload
# ─────────────────────────────────────────────
def show_step2():
    st.markdown(
        f'<div class="info-chip">📋 {st.session_state["jd_title"]}</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">📄 Candidate Resumes</div>', unsafe_allow_html=True)

    resume_files = st.file_uploader(
        "Upload candidate resumes (PDF only)",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can select multiple PDFs at once"
    )

    if resume_files:
        st.success(f"{len(resume_files)} resume(s) ready")
        for i, f in enumerate(resume_files):
            st.write(f"📄 {i+1}. {f.name}")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state['wizard_step'] = 1
            st.rerun()
    with col4:
        if st.button("Next →", type="primary", use_container_width=True):
            if not resume_files:
                st.error("Please upload at least one resume")

            else:
                import tempfile
                valid_resumes = []
                invalid_files = []

                for f in resume_files:
                    # Save temp file to extract text
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                        tmp.write(f.read())
                        tmp_path = tmp.name

                    resume_text = extract_text_from_pdf(tmp_path)
                    os.unlink(tmp_path)

                    # VALIDATION
                    if not is_valid_resume(resume_text):
                        invalid_files.append(f.name)
                    else:
                        valid_resumes.append({
                            "name": f.name,
                            "data": f.getvalue()  # keep original file
                        })

                # If all resumes invalid
                if not valid_resumes:
                    st.error("❌ All uploaded files are invalid resumes. Please upload proper resumes.")

                else:
                    # If some invalid
                    if invalid_files:
                        st.warning(f"⚠️ Skipped invalid resumes: {', '.join(invalid_files)}")

                    # Save only valid resumes
                    st.session_state['resume_files_data'] = valid_resumes
                    st.session_state['wizard_step'] = 3
                    st.rerun()
# ─────────────────────────────────────────────
#  STEP 3 — Evaluate
# ─────────────────────────────────────────────
def show_step3():
    user = get_current_user()
    resume_files_data = st.session_state.get('resume_files_data', [])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="info-chip">📋 {st.session_state["jd_title"]}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="info-chip">👥 {len(resume_files_data)} candidate(s)</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        evaluate = st.button("Initiate Evaluation", type="primary", use_container_width=True)

    if evaluate:
        jd_text = st.session_state['jd_text']
        jd_title = st.session_state['jd_title']
        progress_bar = st.progress(0)
        progress_text = st.empty()
        status = st.empty()
        jd_id = save_job_description(user['id'], jd_title, jd_text)
        results = []

        for i, resume_data in enumerate(resume_files_data):
            status.info(
                f"⏳ Evaluating **{resume_data['name']}**  \n"
                f"📄 {i+1} of {len(resume_files_data)} resumes"
            )
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(resume_data['data'])
                tmp_path = tmp.name
            resume_text = extract_text_from_pdf(tmp_path)
            os.unlink(tmp_path)
            resume_info = process_resume(resume_text, jd_text)

            # Use filename fallback if name looks wrong
            bad_names = {
                "Candidate", "Unknown", "Work Experience", "Summary Professional",
                "Summary", "Professional", "Objective", "Profile", "Overview",
                "Specializing In", "Data Engineer", "Software Engineer",
            }
            name = resume_info.get('name') or ""

            if (name in bad_names or
                name.lower() in {n.lower() for n in bad_names}):
                raw = resume_data['name'].replace('.pdf', '')
                parts = re.split(r'[_\-\s]+', raw)
                name_parts = []
                for p in parts:
                    p_clean = p.strip()
                    if (p_clean and
                            p_clean.replace("'", "").isalpha() and
                            p_clean.lower() not in JOB_TITLE_WORDS and
                            len(p_clean) > 1):
                        name_parts.append(p_clean.title())
                    else:
                        break  # stop at first non-name word
                if name_parts:
                    resume_info['name'] = ' '.join(name_parts[:3])
                else:
                    resume_info['name'] = raw.title()[:30]
            resume_id = save_resume(jd_id, resume_info['name'], resume_info['email'], resume_data['name'], resume_text)
            match_result = match_resume_to_jd(jd_text, resume_text)
            save_evaluation(resume_id, jd_id, match_result['final_score'],
                            match_result['matched_skills'], match_result['missing_skills'],
                            resume_info['education'], resume_info['experience'])

            results.append({
                "name":             resume_info['name'],
                "email":            resume_info['email'] or "Not provided",
                "phone":            resume_info.get('phone', 'Not provided'),
                "file_name":        resume_data['name'],
                "final_score":      match_result['final_score'],
                "tfidf_score":      match_result.get('tfidf_score', 0),
                "bert_score":       match_result.get('bert_score', 0),
                "skill_score":      match_result.get('skill_score', 0),
                "experience_score": match_result.get('experience_score', 0),
                "title_score":      match_result.get('title_score', 0),
                "matched_skills":   match_result.get('matched_skills', []),
                "missing_skills":   match_result.get('missing_skills', []),
                "education":        resume_info['education'] or "Not found",
                "experience":       resume_info['experience'] or "Not found"
            })
 
            progress = int(((i + 1) / len(resume_files_data)) * 100)

            progress_bar.progress(progress)
            progress_text.markdown(f"**Progress: {progress}%**")

        results.sort(key=lambda x: x['final_score'], reverse=True)

        for r in results:
            r['name'] = r['name'] if r['name'] else "Unknown"
            r['email'] = r['email'] if r['email'] else "Not provided"
            r['education'] = r['education'] if r['education'] not in [None, "None", "none", ""] else "Not found"
            r['experience'] = r['experience'] if r['experience'] not in [None, "None", "none", ""] else "Not found"
            r['matched_skills'] = r['matched_skills'] if r['matched_skills'] else []
            r['missing_skills'] = r['missing_skills'] if r['missing_skills'] else []

        status.success("✅ Evaluation complete!")

        # Normalise skills — convert stringified lists to real lists
        def normalise_skills(val):
            if isinstance(val, str) and val.startswith("["):
                import ast
                try:
                    return ast.literal_eval(val)
                except Exception:
                    return []
            return val if isinstance(val, list) else []

        for r in results:
            r['matched_skills'] = normalise_skills(r['matched_skills'])
            r['missing_skills'] = normalise_skills(r['missing_skills'])

        st.session_state['results'] = results
        st.session_state['page'] = 'results'
        st.rerun()

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state['wizard_step'] = 2
            st.rerun()
 
def generate_score_reason(c):
    """
    Generates a one-line natural language explanation
    of why a candidate received their score.
    Based purely on the numeric scores — no AI call.
    """
    bert  = c.get('bert_score', 0)
    skill = c.get('skill_score', 0)
    exp   = c.get('experience_score', 0)
    title = c.get('title_score', 0)
    missing = c.get('missing_skills', [])
 
    parts = []
 
    # Semantic match assessment
    if bert >= 75:
        parts.append("Strong semantic match with JD")
    elif bert >= 55:
        parts.append("Moderate semantic alignment with JD")
    else:
        parts.append("Limited semantic overlap with JD")
 
    # Skill assessment
    if skill >= 78:
        parts.append("excellent skill coverage")
    elif skill >= 65:
        parts.append("good skill coverage")
    elif skill >= 40:
        parts.append("partial skill match")
    else:
        parts.append("low skill match")
 
    # Experience assessment
    if exp >= 0.95:
        parts.append("experience perfectly fits requirement")
    elif exp >= 0.80:
        parts.append("slightly overqualified on experience")
    elif exp >= 0.60:
        parts.append("slightly under required experience")
    else:
        parts.append("experience below requirement")
 
    # Missing skills note
    if missing:
        top_missing = ", ".join(missing[:3])
        if len(missing) > 3:
            top_missing += f" +{len(missing)-3} more"
        parts.append(f"gaps in: {top_missing}")
 
    return ". ".join(parts[:3]) + "."

# ─────────────────────────────────────────────
#  RESULTS PAGE
# ─────────────────────────────────────────────
def show_results_page():
    user = get_current_user()
    show_topbar(user, show_new_eval=True)

    results = st.session_state.get('results', [])
    jd_title = st.session_state.get('jd_title', 'Job Description')

    st.markdown(f"### 📊 Results — {jd_title}")
    st.markdown(f"**{len(results)} candidate(s) evaluated and ranked**")
    st.markdown("---")

    ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 1.5])
    with ctrl1:
        min_score = st.slider("Min score filter", 0, 100, 0, 5)
    with ctrl2:
        view_mode = st.radio("View", ["Cards", "Table"], horizontal=True)
    with ctrl3:
        if st.button("👁 View JD"):
            st.session_state['show_jd_results'] = not st.session_state.get('show_jd_results', False)

    if st.session_state.get('show_jd_results', False):
        st.markdown(
            f'<div class="jd-preview-box">{format_jd_for_display(st.session_state["jd_text"])}</div>',
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

    filtered = [
        r for r in results
        if isinstance(r.get('final_score'), (int, float)) and r['final_score'] >= min_score
    ]
    filtered = [r for r in filtered if r is not None]
    filtered.sort(key=lambda x: x['final_score'], reverse=True)

    st.markdown(f"*Showing {len(filtered)} candidate(s)*")
    st.markdown("---")

    # ── Card View ──
    if view_mode == "Cards":
        for i, c in enumerate(filtered):
            score = c['final_score']
            badge = "🟢 Strong" if score >= 70 else "🟡 Partial" if score >= 40 else "🔴 Weak"
 
            with st.expander(
                f"#{i+1}  {c['name']}  —  {score}%  {badge}",
                expanded=(i == 0)
            ):
                # ── Why this score ──
                reason = generate_score_reason(c)
                st.markdown(
                    f'<div style="background:#f0f4ff;border-left:3px solid #1a73e8;'
                    f'padding:0.6rem 1rem;border-radius:6px;font-size:0.84rem;'
                    f'color:#444;margin-bottom:1rem;">💡 {reason}</div>',
                    unsafe_allow_html=True
                )
 
                # ── Score metrics row ──
                m1, m2, m3, m4, m5 = st.columns(5)
                with m1:
                    st.metric("Final", f"{score}%")
                with m2:
                    st.metric("Skill", f"{c.get('skill_score', 0)}%")
                with m3:
                    st.metric("BERT", f"{c.get('bert_score', 0)}%")
                with m4:
                    st.metric("Exp", f"{c.get('experience_score', 0)}%")
                with m5:
                    st.metric("Title", f"{c.get('title_score', 0)}%")
 
                st.markdown("---")
 
                # ── Basic info row ──
                info1, info2 = st.columns(2)
                with info1:
                    st.markdown("**👤 Candidate Info**")
                    st.caption(f"📧 {c['email']}")
                    phone = c.get('phone', 'Not provided')
                    st.caption(f"📞 {phone}")
                    st.caption(f"📄 {c['file_name']}")
 
                with info2:
                    st.markdown("**💼 Experience**")
                    exp_text = c.get('experience', 'Not found')
                    if exp_text and exp_text not in ['None', 'Not found', 'none']:
                        # Show only the years part cleanly
                        exp_parts = exp_text.split('|')
                        for part in exp_parts[:2]:
                            part = part.strip()
                            if part and part != 'Not found':
                                st.caption(part)
                    else:
                        st.caption("Not found")
 
                    st.markdown("**🎓 Education**")
                    edu = c.get('education', 'Not found')
                    if edu and edu not in ['None', 'Not found', 'none']:
                        edu_short = edu[:120] + '...' if len(edu) > 120 else edu
                        st.caption(edu_short)
                    else:
                        st.caption("Not found")
 
                st.markdown("---")
 
                # ── Skills row ──
                sk1, sk2 = st.columns(2)
                with sk1:
                    st.markdown("**✅ Matched Skills**")
                    if c['matched_skills']:
                        badges = " ".join([
                            f'<span class="badge-matched">{s}</span>'
                            for s in c['matched_skills']
                        ])
                        st.markdown(badges, unsafe_allow_html=True)
                    else:
                        st.caption("None matched")
 
                with sk2:
                    st.markdown("**❌ Missing Skills**")
                    if c['missing_skills']:
                        badges = " ".join([
                            f'<span class="badge-missing">{s}</span>'
                            for s in c['missing_skills']
                        ])
                        st.markdown(badges, unsafe_allow_html=True)
                    else:
                        st.caption("No missing skills")

    # ── Table View ──
    else:
        df = pd.DataFrame([{
            "Rank":           i + 1,
            "Name":           r['name'],
            "Final Score":    f"{r['final_score']}%",
            "Skill Score":    f"{r['skill_score']}%",
            "BERT Score":     f"{r['bert_score']}%",
            "Exp Score":      f"{r.get('experience_score', 'N/A')}%",
            "Title Score":    f"{r.get('title_score', 'N/A')}%",
            "Email":          r['email'],
        } for i, r in enumerate(filtered)])
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Export ──
    st.markdown("---")
    st.markdown("### 📌 Export Results")

    exp1, exp2, exp3 = st.columns(3)

    with exp1:
        st.download_button(
            label="📥 Download CSV",
            data=export_csv(filtered),
            file_name=f"{jd_title}_results.csv",
            mime="text/csv",
            use_container_width=True
        )

    with exp2:
        st.download_button(
            label="📊 Download Excel",
            data=export_excel(filtered, jd_title),
            file_name=f"{jd_title}_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with exp3:
        st.download_button(
            label="📄 Download PDF",
            data=export_pdf(filtered, jd_title),
            file_name=f"{jd_title}_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    # Auto-create database if it does not exist
    import os
    if not os.path.exists('resume_screener.db'):
        import subprocess
        subprocess.run(['python', 'setup_db.py'], check=True)
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if not st.session_state['logged_in']:
        show_login_page()
    elif st.session_state.get('page') == 'results':
        show_results_page()
    elif st.session_state.get('page') == 'admin':
        show_admin_panel()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()