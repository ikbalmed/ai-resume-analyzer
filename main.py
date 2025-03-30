import argparse
import os
import streamlit as st
import pandas as pd
from text_ext import extract_text_from_pdf, extract_text_from_docx
from keyword_ext import extract_keywords
from similarity import calculate_similarity
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

genai.configure(api_key=GEMINI_API_KEY)

def analyze_resume(resume_text, job_description):
    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = set(extract_keywords(job_description))

    match_score = calculate_similarity(resume_text, job_description)
    missing_keywords = job_keywords - resume_keywords
    suggested_keywords = generate_suggested_keywords(missing_keywords, resume_keywords)
    ai_advice = generate_advice(resume_text, job_description)

    return {
        "match_score": match_score,
        "missing_keywords": list(missing_keywords),
        "suggested_keywords": suggested_keywords,
        "ai_advice": ai_advice
    }

def extract_keywords_from_response(response_text):
    """Extracts only the keywords from the AI response."""
    keywords = re.findall(r"\*\*(.*?)\*\*", response_text) 
    if not keywords:
        keywords = re.findall(r"(\b[A-Za-z0-9_-]+\b)", response_text)
    return list(set(keywords[:10]))

def generate_suggested_keywords(missing_keywords, resume_keywords):
    if not missing_keywords:
        return []

    prompt = (
        f"Missing Keywords: {', '.join(missing_keywords)}\n"
        f"Resume Keywords: {', '.join(resume_keywords)}"
    )
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return extract_keywords_from_response(response.text) if response else []
    except Exception as e:
        return [f"⚠️ Error generating suggestions: {str(e)}"]

def generate_advice(resume_text, job_description):
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(
            f"Provide improvement suggestions for the following resume based on the job description:\n\nResume: {resume_text}\n\nJob Description: {job_description}"
        )
        return response.text if response else "No advice generated."
    except Exception as e:
        return f"⚠️ Unable to generate advice: {str(e)}"

def process_multiple_resumes(resume_paths, job_description):
    results = []
    for resume_path in resume_paths:
        if resume_path.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_path)
        elif resume_path.endswith(".docx"):
            resume_text = extract_text_from_docx(resume_path)
        else:
            continue

        result = analyze_resume(resume_text, job_description)
        results.append({
            "resume": os.path.basename(resume_path),
            "match_score": result["match_score"],
            "missing_keywords": result["missing_keywords"],
            "suggested_keywords": result["suggested_keywords"],
            "ai_advice": result["ai_advice"]
        })
    
    return sorted(results, key=lambda x: x["match_score"], reverse=True)

def cli_mode(resume_folder, job_path):
    job_description = open(job_path).read()
    
    resume_paths = [
        os.path.join(resume_folder, file)
        for file in os.listdir(resume_folder)
        if file.endswith((".pdf", ".docx"))
    ]

    results = process_multiple_resumes(resume_paths, job_description)

    print("\n📊 **Resume Ranking Based on Match Score:**\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['resume']} - Score: {result['match_score']}%")
        print(f"   🔍 Missing: {', '.join(result['missing_keywords'])}")
        print(f"   🔹 Suggested: {', '.join(result['suggested_keywords'])}")
        print(f"   🤖 AI Advice: {result['ai_advice']}")
        print("-" * 50)

def gui_mode():
    st.title("📄 AI Resume Scanner - Batch Mode")

    job_desc = st.text_area("📝 Paste Job Description Here", "")
    uploaded_files = st.file_uploader("📂 Upload Resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

    if uploaded_files and job_desc:
        resume_paths = []
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
                resume_paths.append(uploaded_file.name)

        with st.spinner("Processing..."):
            results = process_multiple_resumes(resume_paths, job_desc)

        st.success("✅ Resume Analysis Complete")
        
        df = pd.DataFrame(results)
        st.dataframe(df[["resume", "match_score"]].sort_values("match_score", ascending=False))

        selected_resume = st.selectbox("📂 Select a Resume to View Details", df["resume"])
        details = next(item for item in results if item["resume"] == selected_resume)

        st.write("### 🔍 Keywords Analysis")
        st.table({"Missing Keywords": details["missing_keywords"], "Suggested Keywords": details["suggested_keywords"]})
        
        st.write("### 🤖 AI Advice")
        st.write(details["ai_advice"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Resume Ranking")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--resume_folder", type=str, help="Folder containing resume files")
    parser.add_argument("--job", type=str, help="Path to job description text file")

    args = parser.parse_args()

    if args.cli and args.resume_folder and args.job:
        cli_mode(args.resume_folder, args.job)
    else:
        gui_mode()