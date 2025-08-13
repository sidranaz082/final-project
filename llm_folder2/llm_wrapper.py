# llm_wrapper.py
import threading
from transformers import pipeline, set_seed

# Lazy initialization to avoid long import time while developing
_generator = None
_lock = threading.Lock()

def _get_generator():
    global _generator
    with _lock:
        if _generator is None:
            # change model name if you want another (e.g., "gpt2-medium")
            _generator = pipeline("text-generation", model="gpt2")
            set_seed(42)
    return _generator

def _call_model(prompt, max_new_tokens=200, temperature=0.7):
    gen = _get_generator()
    # do_sample true to avoid deterministic output
    out = gen(prompt, max_new_tokens=max_new_tokens, do_sample=True, temperature=temperature)
    return out[0]["generated_text"]

def build_resume_prompt(name, title, contact, skills, experience, achievements):
    prompt = (
        f"Write a clear, professional resume for {name} applying as a {title}.\n"
        f"Contact: {contact}\n"
        f"Skills: {skills}\n"
        f"Work Experience: {experience}\n"
    )
    if achievements:
        prompt += f"Achievements: {achievements}\n"
    prompt += (
        "\nFormat the resume with sections: SUMMARY, SKILLS, EXPERIENCE, ACHIEVEMENTS (if any). "
        "Use concise bullet points and professional tone.\n\nResume:\n"
    )
    return prompt

def build_cover_letter_prompt(name, title, company, job_role, contact, skills, experience, achievements):
    prompt = (
        f"Write a persuasive, professional cover letter from {name} applying for the position of {job_role} "
        f"at {company}. {name}'s current title is {title}. Contact: {contact}.\n"
        f"Skills: {skills}\nWork Experience: {experience}\n"
    )
    if achievements:
        prompt += f"Achievements: {achievements}\n"
    prompt += (
        "\nMake the letter one page, first-person, include an opening paragraph, two body paragraphs about fit & achievements, "
        "and a closing paragraph with next steps. Keep it polite and direct.\n\nCover Letter:\n"
    )
    return prompt

def generate_resume(name, title, contact, skills, experience, achievements,
                    max_new_tokens=200, temperature=0.7):
    try:
        prompt = build_resume_prompt(name, title, contact, skills, experience, achievements)
        text = _call_model(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
        # remove prompt portion if model repeats prompt (strip before 'Resume:' if duplicated)
        if "Resume:" in text:
            text = text.split("Resume:", 1)[1].strip()
        return {"success": True, "text": text}
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_cover_letter(name, title, company, job_role, contact, skills, experience, achievements,
                          max_new_tokens=200, temperature=0.7):
    try:
        prompt = build_cover_letter_prompt(name, title, company, job_role, contact, skills, experience, achievements)
        text = _call_model(prompt, max_new_tokens=max_new_tokens, temperature=temperature)
        if "Cover Letter" in text:
            # optional cleaning
            text = text.split("Cover Letter", 1)[-1].strip()
        return {"success": True, "text": text}
    except Exception as e:
        return {"success": False, "error": str(e)}
