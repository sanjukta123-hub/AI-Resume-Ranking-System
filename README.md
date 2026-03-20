🤖 AI Resume Ranking & ATS Optimization System

Project Overview

This project presents an end-to-end AI-powered resume ranking system designed to automate candidate evaluation based on job descriptions.

The system leverages Natural Language Processing (NLP), semantic similarity, and ATS (Applicant Tracking System) scoring techniques to identify the most suitable candidates efficiently.

It combines AI-driven analysis with interactive dashboards to support smarter and faster hiring decisions.



Input Data

• Job Description (user input)

• Candidate Resumes (PDF / DOCX format)

The system processes unstructured resume data and converts it into meaningful insights.


⚙️ Project Workflow


1. Data Extraction & Preprocessing


• Extracted text from PDF and DOCX resumes

• Cleaned and normalized text (removing noise, formatting issues)

• Converted all text into a consistent format for analysis


2. Skill & Experience Extraction


• Extracted relevant technical skills using predefined skill dictionary

• Identified years of experience using regex-based pattern matching

• Compared candidate skills with job requirements



3. Semantic Similarity (AI Matching)


• Generated embeddings for job description and resumes

• Calculated similarity scores using vector-based comparison

• Captured contextual meaning beyond keyword matching



4. Resume Scoring System


Final Score Calculation:

Final Score =
0.6 × Semantic Similarity

+ 0.25 × Skill Match
+ 0.15 × Experience Score

Skill Matching:

• Compared overlap between job skills and candidate skills

Experience Matching:

• Evaluated candidate experience vs required experience



5. ATS Score Simulation


The system evaluates resumes like an ATS using:

• Keyword Density Score

• Section Presence (Education, Skills, Experience, Projects)

• Formatting Score (based on resume length)

ATS Score Formula:

ATS Score =
0.5 × Keyword Density

+ 0.3 × Section Match
+ 0.2 × Formatting


6. Visualization & Dashboard


Interactive dashboards built using
Streamlit & Plotly:

• 🏆 Resume Ranking Table

• 📊 Performance Overview Dashboard

• 📈 Skill Gap Analysis

• 📑 Candidate Comparison

• 📡 Radar Chart (Skill Visualization)

• 🤖 AI Feedback System

• 📝 ATS Screening Simulation



7. Output


• Ranked list of candidates

• Detailed candidate insights

• Skill gap identification

• ATS compatibility results

• Downloadable CSV report


Technologies Used


Programming & Frameworks

• Python

• Streamlit

Libraries


• PyPDF2 (PDF parsing)

• python-docx (DOCX parsing)

• Pandas (data processing)

• Plotly (visualization)

• Regex (text extraction)


AI Components


• NLP Text Preprocessing

• Embedding-based Similarity

• Skill Extraction Algorithm


Model Deployment


The system is deployed as a Streamlit web application that allows users to:

• Upload multiple resumes

• Input job descriptions

• Analyze and rank candidates instantly

• Visualize insights through dashboards


📊 Key Features


• Multi-resume processing (PDF & DOCX)

• AI-based semantic matching (not just keywords)

• ATS scoring simulation

• Interactive analytics dashboards

• Skill gap identification

• Candidate comparison tools

• Exportable reports



Business Impact



This system helps organizations:

• Automate resume screening

• Reduce manual hiring effort

• Improve candidate-job matching accuracy

• Identify skill gaps quickly

• Enhance recruitment efficiency
