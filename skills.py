import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills(text, skill_list):
    found_skills = []

    if not text:
        return found_skills

    text = text.lower()

    for skill in skill_list:
        if skill.lower() in text:
            found_skills.append(skill.lower())

    return list(set(found_skills))