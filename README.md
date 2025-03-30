# AI Resume Analyzer

## 📌 Overview

AI-powered resume analyzer that compares resumes against a given job description, providing keyword analysis, match scores, and improvement suggestions.

## 🚀 Features

- Extracts text from **PDF** and **DOCX** resumes
- Identifies **missing keywords** from the job description
- Suggests **alternative keywords** based on resume content
- Calculates **match score** between the resume and job description
- Provides **AI-generated improvement advice**
- Supports **batch processing** of multiple resumes
- Available in **CLI mode** and **GUI mode (Streamlit)**

## 🛠️ Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ikbalmed/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```sh
   cp .env.example .env  # Rename and edit with your API key
   ```
   - Add your **Google Gemini API Key** in the `.env` file:
     ```
     GEMINI_API_KEY=your_api_key_here
     GEMINI_MODEL=gemini-2.0-flash
     ```

## 🔥 Usage

### 🎨 GUI Mode (Streamlit)

Run the Streamlit web app:

```sh
streamlit run resume_analyzer.py
```

- Paste the **job description**
- Upload **one or more resumes (PDF/DOCX)**
- View **match scores, missing/suggested keywords, and AI advice**

### 🖥️ CLI Mode

Run in terminal:

```sh
python resume_analyzer.py --cli --resume_folder path/to/resumes --job path/to/job_description.txt
```

- Outputs ranked resumes with **match scores** and **suggested improvements**

## 📊 Example Output

```
📊 Resume Ranking Based on Match Score:
1. resume1.pdf - Score: 85%
   🔍 Missing: leadership, Python, machine learning
   🔹 Suggested: AI, data science, programming
   🤖 AI Advice: Emphasize your leadership experience and Python skills.
--------------------------------------------------
2. resume2.docx - Score: 78%
   🔍 Missing: teamwork, cloud computing
   🔹 Suggested: collaboration, AWS, DevOps
   🤖 AI Advice: Highlight experience with cloud technologies.
```

## 📌 Tech Stack

- **Python**
- **Streamlit** (GUI)
- **Google Gemini AI** (Keyword analysis & suggestions)
- **pandas** (Data handling)
- **python-docx** (DOCX extraction)
- **PyMuPDF** (PDF extraction)
- **dotenv** (Environment variables management)

## 🔗 License

MIT License. Free to use and modify.

## ✨ Contributors

Made by **Mohamed Ikbal** - Contributions & issues are welcomed!

