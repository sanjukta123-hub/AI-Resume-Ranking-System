from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rank_resumes(job_embedding, resume_embeddings):
    job_embedding = np.array(job_embedding).reshape(1, -1)
    resume_embeddings = np.array(resume_embeddings)

    scores = cosine_similarity(resume_embeddings, job_embedding)
    return scores.flatten()