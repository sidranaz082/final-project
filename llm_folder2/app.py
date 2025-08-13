# app.py
import io
from fpdf import FPDF
from flask import Flask, request, jsonify, render_template, send_file
from llm_wrapper import generate_resume, generate_cover_letter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Accept JSON (AJAX) or form
    data = request.get_json() if request.is_json else request.form

    name = data.get('name', '').strip()
    title = data.get('title', '').strip()
    contact = data.get('contact', '').strip()
    skills = data.get('skills', '').strip()
    experience = data.get('experience', '').strip()
    achievements = data.get('achievements', '').strip()
    doc_type = data.get('type', 'resume')  # 'resume', 'cover', 'both'
    max_tokens = int(data.get('max_tokens', 200))
    temperature = float(data.get('temperature', 0.7))

    # Basic validation
    if not name or not title:
        return jsonify({"success": False, "error": "Name and current title/role are required."}), 400

    response = {}
    if doc_type in ('resume', 'both'):
        resume = generate_resume(name, title, contact, skills, experience, achievements,
                                 max_new_tokens=max_tokens, temperature=temperature)
        response['resume'] = resume

    if doc_type in ('cover', 'both'):
        company = data.get('company', '').strip()
        job_role = data.get('job_role', title).strip()
        cover = generate_cover_letter(name, title, company, job_role, contact, skills, experience, achievements,
                                      max_new_tokens=max_tokens, temperature=temperature)
        response['cover_letter'] = cover

    return jsonify({"success": True, "result": response})

def _build_pdf_text(name, generated_resume, generated_cover):
    # build a simple PDF text body
    parts = []
    if generated_resume and generated_resume.get('success'):
        parts.append("RESUME\n")
        parts.append(generated_resume['text'])
        parts.append("\n\n")
    if generated_cover and generated_cover.get('success'):
        parts.append("COVER LETTER\n")
        parts.append(generated_cover['text'])
    full = "\n".join(parts)
    return full

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    data = request.get_json() if request.is_json else request.form
    # Generate content same as /generate but return PDF
    name = data.get('name', '').strip()
    title = data.get('title', '').strip()
    contact = data.get('contact', '').strip()
    skills = data.get('skills', '').strip()
    experience = data.get('experience', '').strip()
    achievements = data.get('achievements', '').strip()
    doc_type = data.get('type', 'resume')
    max_tokens = int(data.get('max_tokens', 400))
    temperature = float(data.get('temperature', 0.7))
    company = data.get('company', '').strip()
    job_role = data.get('job_role', title).strip()

    resume = None
    cover = None
    if doc_type in ('resume', 'both'):
        resume = generate_resume(name, title, contact, skills, experience, achievements,
                                 max_new_tokens=max_tokens, temperature=temperature)
    if doc_type in ('cover', 'both'):
        cover = generate_cover_letter(name, title, company, job_role, contact, skills, experience, achievements,
                                      max_new_tokens=max_tokens, temperature=temperature)

    pdf_text = _build_pdf_text(name, resume, cover)

    # create pdf in memory
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # write lines (simple)
    for line in pdf_text.split("\n"):
        pdf.multi_cell(0, 7, line)
    bio = io.BytesIO()
    pdf.output(bio)
    bio.seek(0)
    return send_file(bio, as_attachment=True, download_name=f"{name.replace(' ', '_')}_documents.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
