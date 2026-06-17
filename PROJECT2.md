Mode 2: Build an AI worker that runs every Friday at 11 AM, generates a PDF study report automatically, and tracks your daily progress without you asking.

What This Project Does
Feature	Description
Friday Auto Report	Every Friday at 11 AM, worker creates PDF with study plan + exam prep
Daily Progress Tracking	You record what you studied each day (simple command)
Progress Button	Click to generate PDF report of completed study anytime
Worker runs alone	After setup, no manual queries needed
This proves Mode 2: AI worker does work repeatedly without you asking every time.

Book Sections Used (Same 3 as Mode 1)
#	Section	Content
1	Quick Start	Mode 1 vs Mode 2, 6-stage path, time estimates
2	AI Prompting 2026	13 concepts
3	How to Think in AI Era	6 disciplines
Folder Structure
text
mode2-project/
│
├── frontend/
│   └── index.html              # Beautiful UI with Progress Button
│
├── backend/
│   ├── worker.py               # Main worker (runs Friday 11 AM auto)
│   ├── record.py               # Record daily study (manual)
│   ├── progress_report.py      # Generate PDF on demand
│   ├── data1.txt               # Copy from mode1 (Quick Start)
│   ├── data2.txt               # Copy from mode1 (AI Prompting)
│   ├── data3.txt               # Copy from mode1 (How to Think)
│   └── templates/
│       └── report_template.html # PDF template
│
├── data/
│   ├── progress.json           # Stores all study records
│   └── progress_backup.json    # Auto backup
│
├── reports/                    # Generated PDFs go here
│   └── 2026-05-30_report.pdf
│
├── static/
│   └── style.css               # UI styles
│
├── .env                        # API keys
└── README.md                   # Setup instructions

# Mode 2 Project - Weekly Study Worker

## What This Is
An AI worker that:
- Runs every Friday at 11 AM automatically
- Generates PDF study reports with next week plan
- Tracks your daily study progress
- Proves Mode 2: AI workers that work without you asking

## Installation

```bash
pip install flask flask-cors python-dotenv google-generativeai fpdf

Setup Steps
Step 1: Copy data files from Mode 1
Copy data1.txt, data2.txt, data3.txt from mode1-project/backend/ to mode2-project/backend/

Step 2: Initialize progress file
The data/progress.json file will be created automatically on first run.

Step 3: Start the backend API
bash
cd backend
python app.py
Step 4: Open frontend
Open frontend/index.html in your browser

How to Use
Daily: Record your study
bash
cd backend
python record.py
Weekly: Auto report (Friday 11 AM)
Set up scheduler (see below) or run manually:

bash
cd backend
python worker.py
Anytime: Generate progress report
Click "Generate Progress Report" button in the UI

Scheduling the Worker
Windows (Task Scheduler)
Open Task Scheduler

Create Basic Task

Trigger: Weekly, Friday, 11:00 AM

Action: Start program → python → Arguments: worker.py

Start in: C:\path\to\mode2-project\backend


Manual (still Mode 2!)
Just run python worker.py every Friday yourself. The worker still does all the work!

Files Overview
File	Purpose
worker.py	Main worker (auto runs Friday)
record.py	Record daily study
progress_report.py	Generate PDF on demand
app.py	Flask API for UI
progress.json	Stores all study data
data1-3.txt	Book content (from Mode 1)