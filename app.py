import streamlit as st
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Helper Functions
# -----------------------------

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def preprocess(text):
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

def get_similarity(resume, jd):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, jd])
    return cosine_similarity(matrix)[0][1]

def extract_keywords(text):
    doc = nlp(text)
    return list(set([token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]]))

# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="AI Job Analyzer", layout="wide")

st.title("🤖 AI Job Analyzer")
st.markdown("Upload your **Resume** and paste **Job Description** to analyze match score")

# Layout
col1, col2 = st.columns(2)

# Resume Upload
with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

# Job Description Input
with col2:
    st.subheader("📝 Job Description")
    jd_text = st.text_area("Paste Job Description here", height=250)

# Analyze Button
if st.button("🔍 Analyze"):
    if uploaded_file and jd_text:

        # Extract resume text
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

        # Preprocess
        resume_clean = preprocess(resume_text)
        jd_clean = preprocess(jd_text)

        # Similarity Score
        score = get_similarity(resume_clean, jd_clean)

        # Keywords
        resume_keywords = set(extract_keywords(resume_text))
        jd_keywords = set(extract_keywords(jd_text))

        missing_skills = jd_keywords - resume_keywords

        # -----------------------------
        # Results
        # -----------------------------
        st.success(f"✅ Match Score: {round(score*100, 2)}%")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("📌 Resume Skills")
            st.write(", ".join(list(resume_keywords)[:30]))

        with col4:
            st.subheader("🎯 Missing Skills")
            st.write(", ".join(list(missing_skills)[:30]))

        # Suggestions
        st.subheader("💡 Suggestions")
        if score > 0.75:
            st.write("Great match! You are well aligned with this job.")
        elif score > 0.5:
            st.write("Good match. Add missing skills and improve keywords.")
        else:
            st.write("Low match. Consider updating your resume significantly.")

        if missing_skills:
            st.write("👉 Consider adding these skills:", ", ".join(list(missing_skills)[:10]))

    else:
        st.warning("⚠️ Please upload resume and paste job description")