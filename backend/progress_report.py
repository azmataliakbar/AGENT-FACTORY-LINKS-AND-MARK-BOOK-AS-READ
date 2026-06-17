import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

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

def create_progress_pdf():
    progress = load_progress()
    today = datetime.now().strftime("%Y-%m-%d")
    percentage = calculate_percentage(progress)
    
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    pdf_path = f"{REPORTS_FOLDER}/progress_{today}.pdf"
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=24, alignment=TA_CENTER, spaceAfter=20)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=16, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor('#4f46e5'))
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=11, spaceAfter=6)
    
    story = []
    
    story.append(Paragraph("Study Progress Report", title_style))
    story.append(Paragraph(f"Generated: {today}", styles['Italic']))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph(f"Overall Progress: {percentage}%", heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("Chapter Details:", heading_style))
    
    qs_status = progress['chapters']['Quick Start']['status']
    status_symbol = "[DONE]" if qs_status == "completed" else "[IN PROG]" if qs_status == "in_progress" else "[TODO]"
    story.append(Paragraph(f"{status_symbol} Quick Start: {qs_status}", normal_style))
    
    ai_completed = len(progress['chapters']['AI Prompting 2026']['completed_concepts'])
    story.append(Paragraph(f"[AI] AI Prompting 2026: {ai_completed}/13 concepts", normal_style))
    
    think_completed = len(progress['chapters']['How to Think in AI Era']['completed_disciplines'])
    story.append(Paragraph(f"[THINK] How to Think in AI Era: {think_completed}/6 disciplines", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("Daily Study Log:", heading_style))
    for entry in progress['daily_log']:
        story.append(Paragraph(f"[{entry['date']}] {entry['chapter']}: {entry['completed']}", normal_style))
        if entry.get('notes'):
            story.append(Paragraph(f"     Note: {entry['notes']}", normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("Statistics:", heading_style))
    story.append(Paragraph(f"Total study days: {len(progress['daily_log'])}", normal_style))
    story.append(Paragraph(f"Last updated: {progress['last_updated']}", normal_style))
    
    doc.build(story)
    
    print(f"Progress report saved: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_progress_pdf()