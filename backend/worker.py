import os
import json
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

genai.configure(api_key=GEMINI_API_KEY)

PROGRESS_FILE = "../data/progress.json"
REPORTS_FOLDER = "../reports"

def load_progress():
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def calculate_percentage(progress):
    total = 1 + 13 + 6 + 16
    completed = 0
    if progress["chapters"]["Quick Start"]["status"] == "completed":
        completed += 1
    completed += len(progress["chapters"]["AI Prompting 2026"]["completed_concepts"])
    completed += len(progress["chapters"]["How to Think in AI Era"]["completed_disciplines"])
    completed += len(progress["chapters"]["The Agent Factory Thesis"]["completed_arguments"])
    return round((completed / total) * 100)

def load_book_data():
    with open("data1.txt", "r", encoding="utf-8") as f:
        data1 = f.read()
    with open("data2.txt", "r", encoding="utf-8") as f:
        data2 = f.read()
    with open("data3.txt", "r", encoding="utf-8") as f:
        data3 = f.read()
    with open("data4.txt", "r", encoding="utf-8") as f:
        data4 = f.read()
    return data1, data2, data3, data4

def generate_study_plan(progress, data1, data2, data3, data4):
    percentage = calculate_percentage(progress)
    
    prompt = f"""
You are a study planner. Based on the student's progress:

Overall completion: {percentage}%

Progress details:
- Quick Start: {progress['chapters']['Quick Start']['status']}
- AI Prompting 2026: {len(progress['chapters']['AI Prompting 2026']['completed_concepts'])}/13 concepts completed
- How to Think: {len(progress['chapters']['How to Think in AI Era']['completed_disciplines'])}/6 disciplines completed
- The Agent Factory Thesis: {len(progress['chapters']['The Agent Factory Thesis']['completed_arguments'])}/16 arguments completed

Generate a weekly study plan with:
1. What to study next week (3 specific topics from the book)
2. Estimated time for each topic
3. A 3-week exam prep roadmap

Use bullet points with dashes. Be specific.
"""
    
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text

def create_pdf_report(progress, study_plan):
    today = datetime.now().strftime("%Y-%m-%d")
    percentage = calculate_percentage(progress)
    
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    pdf_path = f"{REPORTS_FOLDER}/{today}_study_report.pdf"
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=24, alignment=TA_CENTER, spaceAfter=20)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=16, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor('#4f46e5'))
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=11, spaceAfter=6)
    
    story = []
    
    story.append(Paragraph("Weekly Study Report", title_style))
    story.append(Paragraph(f"Generated: {today}", styles['Italic']))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("Your Progress", heading_style))
    story.append(Paragraph(f"Overall Completion: {percentage}%", normal_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("Chapter Breakdown:", heading_style))
    story.append(Paragraph(f"- Quick Start: {progress['chapters']['Quick Start']['status']}", normal_style))
    story.append(Paragraph(f"- AI Prompting 2026: {len(progress['chapters']['AI Prompting 2026']['completed_concepts'])}/13 concepts", normal_style))
    story.append(Paragraph(f"- How to Think in AI Era: {len(progress['chapters']['How to Think in AI Era']['completed_disciplines'])}/6 disciplines", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("Next Week's Study Plan", heading_style))
    clean_plan = study_plan.replace('\n', '<br/>')
    story.append(Paragraph(clean_plan, normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("Recent Study Activity", heading_style))
    for entry in progress['daily_log'][-7:]:
        story.append(Paragraph(f"- {entry['date']}: {entry['chapter']} - {entry['completed']}", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("Exam Preparation", heading_style))
    story.append(Paragraph("- Review completed concepts weekly", normal_style))
    story.append(Paragraph("- Practice the 6 error types from Discipline 3", normal_style))
    story.append(Paragraph("- Use Prediction Lock before any AI query", normal_style))
    story.append(Paragraph("- Complete all 13 concepts before exam", normal_style))
    
    doc.build(story)
    return pdf_path

def main():
    print("Mode 2 Worker Starting...")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    progress = load_progress()
    data1, data2, data3, data4 = load_book_data()
    
    print("Generating study plan with Gemini...")
    study_plan = generate_study_plan(progress, data1, data2, data3, data4)
    
    print("Creating PDF report...")
    pdf_path = create_pdf_report(progress, study_plan)
    
    print(f"Report saved: {pdf_path}")
    print("Worker completed successfully!")

if __name__ == "__main__":
    main()