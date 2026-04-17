import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx

# Load NLP model
# Use a lazy loader or load it globally
nlp = None

def get_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")
    return nlp

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
    nlp_model = get_nlp()
    doc = nlp_model(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

def get_similarity(resume_clean, jd_clean):
    if not resume_clean or not jd_clean:
        return 0.0
    cv = CountVectorizer()
    try:
        matrix = cv.fit_transform([resume_clean, jd_clean])
        return cosine_similarity(matrix)[0][1]
    except Exception:
        return 0.0

def extract_keywords(text):
    nlp_model = get_nlp()
    doc = nlp_model(text)
    return list(set([token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]]))

def calculate_match(resume_text, jd_text):
    """
    Complete analysis of match between resume and job description.
    """
    resume_clean = preprocess(resume_text)
    jd_clean = preprocess(jd_text)
    
    score = get_similarity(resume_clean, jd_clean)
    
    resume_keywords = set(extract_keywords(resume_text))
    jd_keywords = set(extract_keywords(jd_text))
    
    missing_skills = jd_keywords - resume_keywords
    
    return {
        "score": score,
        "resume_keywords": list(resume_keywords),
        "jd_keywords": list(jd_keywords),
        "missing_skills": list(missing_skills)
    }
