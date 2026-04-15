import streamlit as st
import pandas as pd
import time
from backend.app.services.matching_service import (
    extract_text_from_pdf, extract_text_from_docx, calculate_match
)
from backend.app.services.job_portal_service import search_portal_jobs

# -----------------------------
# Configuration & Styling
# -----------------------------
st.set_page_config(
    page_title="AI Job Analyzer & Matcher", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        border: 1px solid #white;
    }
    .job-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #1e2130;
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
    }
    .score-badge {
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        color: white;
    }
    .high-score { background-color: #2e7d32; }
    .mid-score { background-color: #f9a825; }
    .low-score { background-color: #c62828; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State Initialization
# -----------------------------
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'resume_keywords' not in st.session_state:
    st.session_state.resume_keywords = []
if 'portal_jobs' not in st.session_state:
    st.session_state.portal_jobs = pd.DataFrame()

# -----------------------------
# Sidebar - Resume Upload
# -----------------------------
with st.sidebar:
    st.title("📄 Resume Hub")
    uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
    
    if uploaded_file:
        with st.spinner("Extracting text..."):
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = extract_text_from_docx(uploaded_file)
            st.session_state.resume_text = text
            st.success("Resume uploaded successfully!")
    
    if st.session_state.resume_text:
        st.info(f"Resume Length: {len(st.session_state.resume_text.split())} words")

# -----------------------------
# Main Content
# -----------------------------
st.title("🤖 AI Job Analyzer & Matcher")
st.markdown("Automate your job search and matching with AI precision.")

tab1, tab2 = st.tabs(["📝 Manual Matching", "🌐 Portal Search & Match"])

# --- Tab 1: Manual Matching ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Paste Job Description")
        jd_text = st.text_area("Copy and paste the JD here...", height=300)
    
    with col2:
        st.subheader("📊 Analysis Result")
        if st.button("Analyze Match"):
            if not st.session_state.resume_text:
                st.warning("⚠️ Please upload a resume in the sidebar first.")
            elif not jd_text:
                st.warning("⚠️ Please paste a job description.")
            else:
                with st.spinner("Analyzing..."):
                    result = calculate_match(st.session_state.resume_text, jd_text)
                    
                    score = result['score']
                    color_class = "high-score" if score > 0.7 else "mid-score" if score > 0.4 else "low-score"
                    
                    st.markdown(f"### Match Score: <span class='score-badge {color_class}'>{round(score*100, 2)}%</span>", unsafe_allow_html=True)
                    
                    st.progress(score)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("🎯 Key Skills in JD")
                        st.write(", ".join(result['jd_keywords'][:20]))
                    with c2:
                        st.subheader("💡 Missing Skills")
                        st.write(", ".join(result['missing_skills'][:20]) if result['missing_skills'] else "None!")

# --- Tab 2: Portal Search ---
with tab2:
    st.subheader("🔍 Search Job Portals")
    
    with st.expander("Search Parameters", expanded=True):
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1:
            search_query = st.text_input("Job Title / Keywords", placeholder="e.g. Python Developer")
        with c2:
            location = st.text_input("Location", placeholder="e.g. India", value="India")
        with c3:
            sites = st.multiselect("Portals", ["linkedin", "indeed", "glassdoor"], default=["linkedin", "indeed"])
        
        results_count = st.slider("Jobs to fetch", 5, 20, 10)
    
    if st.button("🚀 Search & Match Jobs"):
        if not st.session_state.resume_text:
            st.warning("⚠️ Please upload a resume in the sidebar first.")
        elif not search_query:
            st.warning("⚠️ Please enter a search query.")
        else:
            with st.spinner("Fetching and matching jobs from portals..."):
                jobs_df = search_portal_jobs(
                    search_term=search_query,
                    location=location,
                    sites=sites,
                    results_wanted=results_count
                )
                
                if jobs_df.empty:
                    st.error("❌ No jobs found for your criteria.")
                else:
                    # Calculate match for each job
                    matches = []
                    for _, row in jobs_df.iterrows():
                        jd = row.get('description', '')
                        if jd:
                            analysis = calculate_match(st.session_state.resume_text, jd)
                            matches.append(analysis['score'])
                        else:
                            matches.append(0.0)
                    
                    jobs_df['match_score'] = matches
                    st.session_state.portal_jobs = jobs_df.sort_values(by='match_score', ascending=False)
    
    # Display Results
    if not st.session_state.portal_jobs.empty:
        st.write(f"Found {len(st.session_state.portal_jobs)} jobs. Sorted by match score:")
        
        for _, job in st.session_state.portal_jobs.iterrows():
            score = job['match_score']
            color_class = "high-score" if score > 0.7 else "mid-score" if score > 0.4 else "low-score"
            
            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="margin-bottom: 0;">{job['title']}</h3>
                            <p style="color: #888; margin-top: 5px;">🏢 {job['company']} | 📍 {job['location']} | 🌐 {job['site']}</p>
                        </div>
                        <div class="score-badge {color_class}">
                            {round(score*100, 1)}% Match
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View Details & Analysis"):
                    analysis = calculate_match(st.session_state.resume_text, job.get('description', ''))
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**🎯 Matching Keywords:**")
                        matching = set(analysis['jd_keywords']) & set(analysis['resume_keywords'])
                        st.write(", ".join(list(matching)[:20]) if matching else "No major keyword matches found.")
                        
                        st.markdown("**💡 Missing Skills:**")
                        st.write(", ".join(analysis['missing_skills'][:20]) if analysis['missing_skills'] else "None!")
                    
                    with col_b:
                        st.markdown("**📄 Job Link:**")
                        st.markdown(f"[Apply on {job['site'].capitalize()}]({job['job_url']})")
                        
                        if job.get('description'):
                            st.markdown("**Description Preview:**")
                            st.text(job['description'][:500] + "...")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & SpaCy")