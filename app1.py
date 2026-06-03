import math as m

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
import os
import json

# ----------------------------
# PDF TEXT EXTRACTION
# ----------------------------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


# ----------------------------
# GEMINI SETUP
# ----------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="CareerPilot AI", page_icon="🤖", layout="wide")

# ----------------------------
# CHAT HISTORY
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hi! I'm CareerPilot AI. Ask me anything about careers, coding, AI, placements, interviews, resumes, or studying abroad."
        }
    ]

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.title("🤖 CareerPilot AI")
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        analysis_prompt = f"""
        Analyze this resume.

        Give:
        1. ATS Score out of 100
        2. Strengths
        3. Weaknesses
        4. Suggestions for improvement

        Resume:
        {resume_text}
        """

        with st.spinner("Analyzing Resume..."):
            analysis = model.generate_content(analysis_prompt)

        st.success("Resume Analyzed!")
        st.write(analysis.text)

    st.markdown("---")

    career_dropdown = st.selectbox(
        "🎯 Career Roadmap",
        [
            "Select",
            "AI Engineer",
            "Data Scientist",
            "Web Developer",
            "Product Manager",
            "Cyber Security"
        ]
    )

    career_custom = st.text_input("Or Enter Any Career")
    career_goal = career_custom if career_custom else career_dropdown

    if st.button("Generate Roadmap") and career_goal != "Select":
        roadmap_prompt = f"""
        Create a roadmap for becoming a {career_goal}.

        Include:
        - Skills
        - Projects
        - Certifications
        - Internship Plan
        - Timeline
        """
        roadmap = model.generate_content(roadmap_prompt)
        st.write(roadmap.text)

    st.markdown("---")

    role_dropdown = st.selectbox(
        "🎤 Interview Coach",
        [
            "Select",
            "AI Engineer",
            "Software Engineer",
            "Data Scientist",
            "Product Manager"
        ]
    )

    role_custom = st.text_input("Or Enter Any Job Role")
    role = role_custom if role_custom else role_dropdown

    if st.button("Generate Questions") and role != "Select":
        interview_prompt = f"""
        Generate 5 interview questions for a {role}.

        For each question include:
        -easy, medium, or hard difficulty
        -Expected answer points
        - Difficulty
        - Expected Answer Points
        """
        interview_response = model.generate_content(interview_prompt)
        st.write(interview_response.text)
    
        st.markdown("---")
    st.write("### Features")
    st.write("✅ Career Guidance")
    st.write("✅ Coding Help")
    st.write("✅ AI Learning")
    st.write("✅ Resume Analyzer")
    st.write("✅ Interview Coach")
    st.write("✅ Career Roadmap")
    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hi! I'm CareerPilot AI. Ask me anything about careers, coding, AI, placements, interviews, resumes, or studying abroad."
            }
        ]
        st.rerun()

# ----------------------------
# MAIN PAGE
# ----------------------------
st.title("🤖 CareerPilot AI")
st.caption("Your AI-Powered Career Mentor")

col1, col2, col3, col4 = st.columns(4)
with col1:
    show_resume = st.button("📄 Resume Analyzer")
with col2:
    show_roadmap = st.button("🎯 Career Roadmap")
with col3:
    show_interview = st.button("🎤 Interview Coach")
with col4:
    show_history = st.button("🕒 Chat History")

# ----------------------------
# DISPLAY CHAT HISTORY
# ----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if show_history:
    st.subheader("🕒 Chat History")
    try:
        with open("chat_history.txt", "r", encoding="utf-8") as f:
            history = f.read()
        st.text_area("Previous Chats", history, height=400)
    except FileNotFoundError:
        st.info("No history available yet.")

# ----------------------------
# USER INPUT
# ----------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            career_prompt = f"""
            You are CareerPilot AI.

            You help students with:
            - Career guidance
            - AI engineering
            - Product management
            - Coding
            - Interview preparation
            - Resume building
            - Higher studies abroad

            Answer clearly, professionally, and in a beginner-friendly manner.

            Question:
            {prompt}
            """
            response = model.generate_content(career_prompt)

            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

            with open("chat_history.txt", "a", encoding="utf-8") as f:
                f.write(f"\nUSER: {prompt}\nAI: {response.text}\n")

        except Exception as e:
            st.error(f"Error: {e}")
