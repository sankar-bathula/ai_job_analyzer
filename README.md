# ai_job_analyzer
import os
from datetime import datetime

# File name
file_name = "job_analysis.md"

# Sample content (you can customize this)
content = f"""
# 📊 AI Job Analyzer Report

**Generated On:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🧑 Candidate Details
- Name: Sankar
- Role: Python Developer

## 💼 Job Description Summary
- Required Skills: Python, AWS, Docker, APIs
- Experience: 3-5 years

## 🔍 Matching Analysis
- Python: ✅ Match
- AWS: ⚠️ Partial
- Docker: ❌ Missing

## 📈 Score
**Overall Match Score: 75%**

## 📝 Suggestions
- Improve Docker knowledge
- Gain hands-on AWS experience
"""

# Create file
with open(file_name, "w", encoding="utf-8") as f:
    f.write(content)

print(f"{file_name} created successfully!")
