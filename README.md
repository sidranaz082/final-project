 Final Project Report
Project Title: LLM-Powered Resume & Cover Letter Generator
Developer: Sidra Naz
Date: 13 August 2025

1. Introduction
This project is a web-based Resume and Cover Letter Generator built using Flask and integrated with an LLM (Large Language Model).
It allows users to input career details (skills, experience, job title, etc.) and instantly generate a professionally written resume and customized cover letter in PDF format.

2. Objectives
Provide a simple and interactive tool for job seekers.

Integrate AI capabilities to produce human-like professional documents.

Allow users to download generated resumes/cover letters as PDFs.

3. Key Features
AI-Powered Text Generation – Uses an LLM wrapper to create personalized resumes and cover letters.

Flask Web Interface – User-friendly form for entering details.

PDF Export – Documents are auto-formatted and downloadable.

Modular Code Structure – Separate files for app.py (Flask routes) and llm_wrapper.py (AI logic).

Local Development Setup – Works without cloud hosting initially, deployable later.

4. Tech Stack
Frontend: HTML, CSS (via Flask templates)

Backend: Python (Flask)

AI Model: LLM via llm_wrapper.py 

PDF Generation: fpdf Python library

Environment Management: venv

5. Setup & Installation
Step 1: Clone the Project
git clone <project_repo_url>
cd llm_folder2

Step 2: Create a Virtual Environment
python -m venv .venv

Step 3: Activate Virtual Environment
.venv\Scripts\activate

Step 4: Install Dependencies
pip install flask fpdf openai

Step 5: Run the Flask App
python app.py

Step 6: Access in Browser
http://127.0.0.1:5000/


6. Project Workflow
User Input Form → Name, Skills, Job Title, Experience.

Flask Backend → Receives data via POST request.

LLM Wrapper → Generates professional text.

PDF Creation → Uses FPDF to structure and style content.


7. Future Improvements
Add multiple resume templates.

Support multilingual resume generation.

Enable cloud deployment (Render, Railway, Vercel).

Include AI-powered job matching suggestions.

 Reflection Note
Working on this LLM-powered Flask project was an enriching and challenging experience.
I learned:

How to structure a Flask project with modular files (app.py, llm_wrapper.py).

How to integrate an AI model to generate human-like professional content.

How to export AI-generated text into PDF using fpdf.

The importance of virtual environments for managing dependencies.

How to debug common issues like "ModuleNotFoundError" and import path errors.

This project improved my problem-solving skills, Flask development experience, and AI integration knowledge.
It also gave me confidence in creating real-world, user-facing applications that can have a direct positive impact on job seekers.



live link :https://final-project-git-main-sidra-nazs-projects.vercel.app
