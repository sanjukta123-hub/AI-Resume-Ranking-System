import streamlit as st
import PyPDF2
import pandas as pd
import plotly.graph_objects as go
import re
from docx import Document 

from utils.preprocessing import clean_text
from utils.embedding import get_embeddings
from utils.ranking import rank_resumes
from utils.skills import extract_skills


# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(page_title="AI-based Resume Ranking and Intelligent Recruitment System", layout="wide")

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
AI-based Resume Ranking and Intelligent Recruitment System
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# Skill List
# ---------------------------------------------------
skill_list = [
    "python", "java", "sql", "machine learning",
    "deep learning", "excel", "power bi",
    "tensorflow", "pytorch", "statistics",
    "nlp", "hadoop"
]

# ---------------------------------------------------
# Experience Extraction
# ---------------------------------------------------
def extract_experience(text):
    import re
    
    if not text:
        return 0

    text = text.lower()
    text = text.replace("\n", " ")

    # Very flexible pattern
    pattern = r'(\d+)\s*\.?\s*(\d+)?\s*\+?\s*(years?|yrs?)'

    matches = re.findall(pattern, text)

    if matches:
        years = []
        for match in matches:
            # match[0] is main number
            years.append(int(match[0]))
        return max(years)

    return 0
# ---------------------------------------------------
# ATS Score Functions
# ---------------------------------------------------

def keyword_density_score(text, job_skills):
    if not text:
        return 0
    
    text = text.lower()
    total_words = len(text.split())
    
    if total_words == 0:
        return 0

    keyword_count = 0
    for skill in job_skills:
        keyword_count += text.count(skill.lower())

    density = keyword_count / total_words
    
    # Scale and limit to 1
    return min(density * 10, 1)


def section_score(text):
    sections = ["education", "skills", "experience", "projects"]
    text = text.lower()
    
    score = 0
    for sec in sections:
        if sec in text:
            score += 1
    
    return score / len(sections)


def formatting_score(text):
    words = len(text.split())

    # Ideal resume length
    if 300 <= words <= 800:
        return 1
    elif 200 <= words <= 1000:
        return 0.7
    else:
        return 0.4


def calculate_ats_score(text, job_skills):
    kd = keyword_density_score(text, job_skills)
    sec = section_score(text)
    fmt = formatting_score(text)

    ats = (0.5 * kd) + (0.3 * sec) + (0.2 * fmt)

    return ats, kd, sec, fmt
# ---------------------------------------------------
# Input Section
# ---------------------------------------------------
job_text = st.text_area("Job Description")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF or Word format)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# ---------------------------------------------------
# Processing
# ---------------------------------------------------
if st.button("Analyze"):

    if job_text.strip() == "":
        st.warning("Please enter Job Description.")
        st.stop()

    if not uploaded_files:
        st.warning("Please upload at least one resume.")
        st.stop()

    with st.spinner("Processing resumes..."):

        clean_job = clean_text(job_text)
        job_emb = get_embeddings([clean_job])
        job_skills = extract_skills(clean_job, skill_list)
        required_experience = extract_experience(clean_job)
    
        resume_texts = []
        resume_names = []

        for file in uploaded_files:
            text = ""

            if file.name.endswith(".pdf"):
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

            elif file.name.endswith(".docx"):
                doc = Document(file)
                for para in doc.paragraphs:
                    text += para.text + " "

            clean_resume = clean_text(text)
            resume_texts.append(clean_resume)
            resume_names.append(file.name)

        resume_emb = get_embeddings(resume_texts)
        similarity_scores = rank_resumes(job_emb[0], resume_emb)

        results = []

        for i in range(len(resume_texts)):

            similarity = float(similarity_scores[i])
            resume_skills = extract_skills(resume_texts[i], skill_list)
            experience_years = extract_experience(resume_texts[i])
        
            if required_experience > 0:
                  experience_score = min(experience_years / required_experience, 1)
            else:
                experience_score = 0

            if len(job_skills) > 0:
                skill_score = len(set(resume_skills) & set(job_skills)) / len(job_skills)
            else:
                skill_score = 0

            final_score = float(
                (0.6 * similarity) +
                (0.25 * skill_score) +
                (0.15 * experience_score)
            )
            
            ats_score, kd_score, sec_score, fmt_score = calculate_ats_score(
                 resume_texts[i],
                 job_skills
            )

            results.append({
                "name": resume_names[i],
                "similarity": similarity,
                "skill_score": skill_score,
                "experience_years": experience_years,
                "experience_score": experience_score,
                "final_score": final_score,
                "resume_skills": resume_skills,
                "resume_text": resume_texts[i],
                "ats_score": ats_score,
                "keyword_score": kd_score,
                "section_score": sec_score,
                "format_score": fmt_score
            })

        results = sorted(results, key=lambda x: x["final_score"], reverse=True)

        st.session_state["results"] = results
        st.session_state["job_skills"] = job_skills


# ---------------------------------------------------
# Display Section
# ---------------------------------------------------
if "results" in st.session_state:

    results = st.session_state["results"]
    job_skills = st.session_state["job_skills"]

    st.success("Ranking")

    top_candidate = results[0]
    st.success(
        f"🏆 Top Candidate: {top_candidate['name']} "
        f"({round(top_candidate['final_score']*100,2)}%)"
    )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏆 Detailed Ranking",
    "📊 Dashboard Overview",
    "📈 Skill Gap Analysis",
    "📑 Candidate Comparison",
    "📡 Radar Chart",
    "📋 AI Feedback",
    "📝 ATS Score Simulation"
 ])
# -----------------------------
# 1️⃣ Detailed Ranking
# -----------------------------
    with tab1:

     st.subheader("📋 Ranking Summary Table")

     summary_df = pd.DataFrame([
     {
        "Rank": idx + 1,
        "Name": r["name"],
        "Final Score (%)": round(r["final_score"] * 100, 2),
        "Similarity (%)": round(r["similarity"] * 100, 2),
        "Experience (Years)": r["experience_years"],
        "ATS Score (%)": round(r["ats_score"] * 100, 2)
     }
       for idx, r in enumerate(results)
     ])
     st.dataframe(summary_df, use_container_width=True)

     st.markdown("---")

     selected_name = st.selectbox(
        "🔎 Select Candidate to View Detailed Analysis",
        [r["name"] for r in results]
     )

     selected_result = next(r for r in results if r["name"] == selected_name)

     st.markdown("## 📊 Detailed Candidate Analysis")
  
     st.success(f"Final Score: {round(selected_result['final_score']*100,2)}%")

     col1, col2 = st.columns(2)
 
     with col1:
        st.write("Similarity:", round(selected_result["similarity"] * 100, 2), "%")
        st.write("Skill Score:", round(selected_result["skill_score"] * 100, 2), "%")
        st.write("Experience (Years):", selected_result["experience_years"])

     with col2:
        st.write("ATS Score:", round(selected_result["ats_score"] * 100, 2), "%")

     st.progress(selected_result["final_score"])

     matched = list(set(selected_result["resume_skills"]) & set(job_skills))
     missing = list(set(job_skills) - set(selected_result["resume_skills"]))

     st.write("Matched Skills:", matched)
     st.write("Missing Skills:", missing)
            
    # -----------------------------
    # 2️⃣ Dashboard
    # -----------------------------
    with tab2:
        df = pd.DataFrame(results)

        col1, col2, col3 = st.columns(3)

        col1.metric("Top Score", f"{round(df['final_score'].max()*100,2)} %")
        col2.metric("Average Score", f"{round(df['final_score'].mean()*100,2)} %")
        col3.metric("Total Candidates", len(df))

        st.bar_chart(df.set_index("name")["final_score"])
        
        csv = df.to_csv(index=False).encode("utf-8")
        
        fig = go.Figure(data=[go.Pie(
           labels=["Semantic Score", "Skill Score", "Experience Score"],
           values=[
               top_candidate["similarity"],
               top_candidate["skill_score"],
               top_candidate["experience_score"]
         ]
       )])

        fig.update_layout(title="Top Candidate Score Distribution")

        st.plotly_chart(fig)
        
        csv = df.to_csv(index=False).encode("utf-8")


        st.download_button(
            label="📥 Download Ranking Report",
            data=csv,
            file_name="resume_ranking_report.csv",
            mime="text/csv"
        )

    # -----------------------------
    # 3️⃣ Skill Gap
    # -----------------------------
    with tab3:

        all_missing = []

        for result in results:
            missing = list(set(job_skills) - set(result["resume_skills"]))
            all_missing.extend(missing)

        if all_missing:
            missing_df = pd.DataFrame(all_missing, columns=["Missing Skill"])
            skill_counts = missing_df["Missing Skill"].value_counts()
            st.bar_chart(skill_counts)
        else:
            st.success("All required skills covered 🎉")

       # -----------------------------
    # 4️⃣ Candidate Comparison
    # -----------------------------
    with tab4:

        st.markdown("## 📊 Candidate Comparison Dashboard")
        st.markdown("---")
        
        st.markdown(
            f"""
            <div style="padding:15px; border-radius:10px; background-color:#1f4e79; color:white;">
                 <h3>🏆 Top Candidate: {top_candidate['name']}</h3>
                 <h4>Final Score: {round(top_candidate['final_score']*100,2)}%</h4>
            </div>
            """,
            unsafe_allow_html=True
)

        candidate_names = [r["name"] for r in results]
        top_name = results[0]["name"]

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"🏆 Top Candidate: {top_name}")

        remaining = [name for name in candidate_names if name != top_name]

        if remaining:

            with col2:
                compare_candidate = st.selectbox(
                    "Compare With",
                    remaining,
                    key="compare_candidate"
                )

            if compare_candidate:

                r1 = next(r for r in results if r["name"] == top_name)
                r2 = next(r for r in results if r["name"] == compare_candidate)

                chart_df = pd.DataFrame({
                    top_name: [
                        r1["similarity"],
                        r1["skill_score"],
                        r1["experience_score"],
                        r1["final_score"]
                    ],
                    compare_candidate: [
                        r2["similarity"],
                        r2["skill_score"],
                        r2["experience_score"],
                        r2["final_score"]
                    ]
                }, index=["Similarity", "Skill Score", "Experience Score", "Final Score"])

                fig = go.Figure()

                for col in chart_df.columns:
                   fig.add_trace(go.Bar(
                      x=chart_df.index,
                      y=chart_df[col],
                      name=col
    ))

                fig.update_layout(
                    title="Candidate Performance Comparison",
                    barmode="group"
     )

                st.plotly_chart(fig)

                if r1["final_score"] > r2["final_score"]:
                    st.success(f"🏆 {top_name} is stronger overall.")
                else:
                    st.success(f"🏆 {compare_candidate} is stronger overall.")

        else:
            st.info("Upload at least 2 resumes to enable comparison.")


    # -----------------------------
    # 5️⃣ Radar Chart
    # -----------------------------
    with tab5:

        st.subheader("Skill Radar Chart")

        radar_skills = [
            "python", "machine learning",
            "deep learning", "nlp",
            "sql", "statistics"
        ]

        candidate_names = [r["name"] for r in results]

        selected_candidates = st.multiselect(
            "Select Candidates for Radar Comparison",
            candidate_names,
            default=candidate_names[:2]
        )

        if selected_candidates:

            fig = go.Figure()

            for name in selected_candidates:
                candidate = next(r for r in results if r["name"] == name)

                skill_scores = []

                for skill in radar_skills:
                    if skill in candidate["resume_skills"]:
                        skill_scores.append(100)
                    else:
                        skill_scores.append(0)

                skill_scores.append(skill_scores[0])
                radar_labels = radar_skills + [radar_skills[0]]

                fig.add_trace(go.Scatterpolar(
                    r=skill_scores,
                    theta=radar_labels, 
                    fill='toself',
                    name=name
                ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True
            )

            st.plotly_chart(fig)

        else:
            st.info("Please select at least one candidate.")

    # -----------------------------
    # 6️⃣ AI Feedback
    # -----------------------------
    with tab6:
        st.markdown(f"""
             ### 🤖 AI Evaluation Summary

            - Candidate matches **{round(top_candidate['skill_score']*100,2)}%** of required skills.
              Experience detected: **{top_candidate['experience_years']} years**.
            - Overall ranking score: **{round(top_candidate['final_score']*100,2)}%**.
             This candidate is classified as a **Strong Fit** for the role.
           """)

        matched = list(set(top_candidate["resume_skills"]) & set(job_skills))
        missing = list(set(job_skills) - set(top_candidate["resume_skills"]))

        st.write("✅ Strengths:", matched)
        st.write("⚠ Needs Improvement:", missing)

        if missing:
            st.info(f"To improve ranking, candidate should learn: {', '.join(missing)}")
        else:
            st.success("Candidate matches all required skills 🎉")
            
# -----------------------------
# 7️⃣ ATS Score Simulation
# -----------------------------
    with tab7:

       st.subheader("📝 ATS Compatibility Analysis")

       rejected_candidates = []
       passed_candidates = []

       for result in results:

          st.markdown(f"### {result['name']}")

          ats_percent = round(result["ats_score"] * 100, 2)

          if ats_percent >= 75:
              st.success(f"ATS Score: {ats_percent}% (Excellent)")
              passed_candidates.append(result["name"])

          elif ats_percent >= 50:
              st.warning(f"ATS Score: {ats_percent}% (Moderate)")
              passed_candidates.append(result["name"])

          else:
              st.error(f"ATS Score: {ats_percent}% (Rejected ❌)")
              rejected_candidates.append(result["name"])

          st.write("Keyword Density Score:", round(result["keyword_score"]*100,2), "%")
          st.write("Section Match Score:", round(result["section_score"]*100,2), "%")
          st.write("Formatting Score:", round(result["format_score"]*100,2), "%")
 
          st.progress(result["ats_score"])

          st.markdown("---")

         # -----------------------------
         # Final ATS Decision Summary
         # -----------------------------
       st.markdown("## 📊 ATS Final Screening Summary")

       if passed_candidates:
          st.success(f"✅ Passed ATS Screening: {', '.join(passed_candidates)}")
       else:
            st.info("No candidates passed ATS.")

       if rejected_candidates:
            st.error(f"❌ Rejected by ATS: {', '.join(rejected_candidates)}")
       else:
            st.info("No candidates rejected.")