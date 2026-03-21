# 🤖 AI Resume Ranking & ATS Optimization System

##  Project Overview

The **AI Resume Ranking & ATS Optimization System** is an end-to-end intelligent recruitment solution designed to automate candidate screening and improve hiring efficiency.

This system leverages **Natural Language Processing (NLP)**, **semantic similarity**, and **ATS-based evaluation techniques** to analyze, score, and rank resumes against job descriptions. It transforms unstructured resume data into actionable insights, enabling faster and more accurate hiring decisions.

---

## 📂 Input Data

* **Job Description** (user-provided text input)
* **Candidate Resumes** (PDF and DOCX formats)

The system processes unstructured textual data and converts it into structured insights for analysis.

---

## ⚙️ Project Workflow

### 1. Data Extraction & Preprocessing

* Extracted text from resumes using PDF and DOCX parsers
* Performed text cleaning and normalization to remove noise and inconsistencies
* Standardized content to ensure accurate downstream processing

---

### 2. Skill & Experience Extraction

* Extracted relevant technical skills using a predefined skill dictionary
* Identified years of experience using regex-based pattern recognition
* Aligned candidate profiles with job requirements

---

### 3. Semantic Similarity (AI Matching)

* Generated embeddings for job descriptions and resumes
* Computed similarity scores using vector-based comparison
* Enabled context-aware matching beyond traditional keyword search

---

### 4. Candidate Scoring Framework

#### Final Score Calculation:

Final Score =
0.6 × Semantic Similarity

* 0.25 × Skill Match Score
* 0.15 × Experience Score

- **Skill Matching:** Measured overlap between required and candidate skills
- **Experience Matching:** Evaluated candidate experience against job requirements

---

### 5. ATS Score Simulation

The system simulates real-world Applicant Tracking System (ATS) evaluation by assessing:

* Keyword Density
* Section Presence (Education, Skills, Experience, Projects)
* Resume Formatting Quality

#### ATS Score Formula:

ATS Score =
0.5 × Keyword Density

* 0.3 × Section Match
* 0.2 × Formatting

---

### 6. Visualization & Analytics

Developed interactive dashboards using **Streamlit** and **Plotly** to provide:

* 🏆 Resume Ranking Summary
* 📊 Performance Overview Dashboard
* 📈 Skill Gap Analysis
* 📑 Candidate Comparison
* 📡 Radar Chart Visualization
* 🤖 AI-Based Feedback
* 📝 ATS Screening Insights

---

### 7. Output

* Ranked list of candidates based on final score
* Detailed candidate evaluation metrics
* Skill gap identification and recommendations
* ATS compatibility analysis
* Exportable CSV reports for further use

---

## Technologies Used

### Programming & Frameworks

* Python
* Streamlit

### Libraries

* PyPDF2 (PDF text extraction)
* python-docx (Word document processing)
* Pandas (data manipulation)
* Plotly (data visualization)
* Regular Expressions (pattern extraction)

### AI Components

* NLP-based text preprocessing
* Embedding-based semantic similarity
* Rule-based skill extraction

---

##  Deployment

The application is deployed as a **Streamlit web-based interface**, enabling users to:

* Upload and analyze multiple resumes
* Input job descriptions dynamically
* Generate real-time candidate rankings
* Visualize insights through interactive dashboards

---

##  Key Features

* AI-driven resume ranking system
* Multi-format resume support (PDF & DOCX)
* Context-aware semantic matching
* ATS scoring simulation
* Interactive dashboards and visual analytics
* Skill gap detection and candidate comparison
* Exportable reports for decision-making

---

## 📈 Business Impact

This system enhances recruitment workflows by:

* Automating resume screening processes
* Reducing manual effort and screening time
* Improving candidate-job matching accuracy
* Identifying skill gaps effectively
* Enabling data-driven hiring decisions

