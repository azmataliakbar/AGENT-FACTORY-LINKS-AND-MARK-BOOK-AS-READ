from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Path configuration
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / 'data' / 'progress.json'
REPORTS_PATH = Path(__file__).parent / 'reports'

# Create reports directory if it doesn't exist
REPORTS_PATH.mkdir(exist_ok=True)

# ── Chapter definitions ──────────────────────────────────────────────────────
ALL_CHAPTERS = [
    "The Agent Factory Orientation",  # 1 page
    "Foundations",                    # 1 page
    "What AI Actually Is",            # 9 ideas
    "The Agent Factory Thesis",       # 16 arguments
    "The AI Operating Layer",         # 10 concepts
    "Quick Start",                    # 1 page
    "AI Prompting 2026",              # 13 concepts
    "Markdown In, HTML Out",          # 14 concepts
    "Code You Never Write",           # 13 concepts
    "Skills & Connectors Crash Course" # 6 concepts
]

def get_default_chapters():
    return {
        "The Agent Factory Orientation": {
            "total_pages": 1, "completed_pages": 0,
            "completed_topics": [], "status": "not_started"
        },
        "Foundations": {
            "total_pages": 1, "completed_pages": 0,
            "completed_topics": [], "status": "not_started"
        },
        "What AI Actually Is": {
            "total_ideas": 9,
            "completed_ideas": [], "completed_dates": [], "status": "not_started"
        },
        "The Agent Factory Thesis": {
            "total_arguments": 16,
            "completed_arguments": [], "completed_dates": [], "status": "not_started"
        },
        "The AI Operating Layer": {
            "total_concepts": 10,
            "completed_concepts": [], "completed_dates": [], "status": "not_started"
        },
        "Quick Start": {
            "total_pages": 1, "completed_pages": 0,
            "completed_topics": [], "status": "not_started"
        },
        "AI Prompting 2026": {
            "total_concepts": 13,
            "completed_concepts": [], "completed_dates": [], "status": "not_started"
        },
        "Markdown In, HTML Out": {
            "total_concepts": 14,
            "completed_concepts": [], "completed_dates": [], "status": "not_started"
        },
        "Code You Never Write": {
            "total_concepts": 13,
            "completed_concepts": [], "completed_dates": [], "status": "not_started"
        },
        "Skills & Connectors Crash Course": {
            "total_concepts": 6,
            "completed_concepts": [], "completed_dates": [], "status": "not_started"
        }
    }

# ── Data helpers ──────────────────────────────────────────────────────────────

def load_progress():
    try:
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
            # Ensure all required chapters exist (handles old files)
            defaults = get_default_chapters()
            if "chapters" not in data:
                data["chapters"] = defaults
            else:
                for ch, ch_def in defaults.items():
                    if ch not in data["chapters"]:
                        data["chapters"][ch] = ch_def
            data["total_chapters"] = len(ALL_CHAPTERS)
            return data
    except FileNotFoundError:
        default_data = {
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "total_chapters": len(ALL_CHAPTERS),
            "chapters": get_default_chapters(),
            "daily_log": [],
            "exam_date": None,
            "study_target": None
        }
        save_progress(default_data)
        return default_data

def save_progress(data):
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def ch(progress, name):
    return progress['chapters'][name]

# ── Chapter config for validation ─────────────────────────────────────────────

CHAPTER_CONFIG = {
    "The Agent Factory Orientation": {"max": 1, "field": "completed_topics"},
    "Foundations": {"max": 1, "field": "completed_topics"},
    "What AI Actually Is": {"max": 9, "field": "completed_ideas"},
    "The Agent Factory Thesis": {"max": 16, "field": "completed_arguments"},
    "The AI Operating Layer": {"max": 10, "field": "completed_concepts"},
    "Quick Start": {"max": 1, "field": "completed_topics"},
    "AI Prompting 2026": {"max": 13, "field": "completed_concepts"},
    "Markdown In, HTML Out": {"max": 14, "field": "completed_concepts"},
    "Code You Never Write": {"max": 13, "field": "completed_concepts"},
    "Skills & Connectors Crash Course": {"max": 6, "field": "completed_concepts"}
}

# Page-type chapters (single completion, not sequential)
PAGE_CHAPTERS = {"The Agent Factory Orientation", "Foundations", "Quick Start"}

# ── /progress ─────────────────────────────────────────────────────────────────

@app.route('/progress', methods=['GET'])
def get_progress():
    progress = load_progress()
    total_items = 0
    completed_items = 0

    # 1. Orientation (1 page)
    total_items += 1
    if ch(progress, "The Agent Factory Orientation")['status'] == 'completed':
        completed_items += 1

    # 2. Foundations (1 page)
    total_items += 1
    if ch(progress, "Foundations")['status'] == 'completed':
        completed_items += 1

    # 3. What AI Actually Is (9 ideas)
    total_items += 9
    whatai_completed = len(ch(progress, "What AI Actually Is")['completed_ideas'])
    completed_items += whatai_completed

    # 4. Thesis (16 arguments)
    total_items += 16
    thesis_completed = len(ch(progress, "The Agent Factory Thesis")['completed_arguments'])
    completed_items += thesis_completed

    # 5. AI Operating Layer (10 concepts)
    total_items += 10
    operating_completed = len(ch(progress, "The AI Operating Layer")['completed_concepts'])
    completed_items += operating_completed

    # 6. Quick Start (1 page)
    total_items += 1
    if ch(progress, "Quick Start")['status'] == 'completed':
        completed_items += 1

    # 7. AI Prompting (13 concepts)
    total_items += 13
    ai_completed = len(ch(progress, "AI Prompting 2026")['completed_concepts'])
    completed_items += ai_completed

    # 8. Markdown In, HTML Out (14 concepts)
    total_items += 14
    markdown_completed = len(ch(progress, "Markdown In, HTML Out")['completed_concepts'])
    completed_items += markdown_completed

    # 9. Code You Never Write (13 concepts)
    total_items += 13
    code_completed = len(ch(progress, "Code You Never Write")['completed_concepts'])
    completed_items += code_completed

    # 10. Skills & Connectors (6 concepts)
    total_items += 6
    skills_completed = len(ch(progress, "Skills & Connectors Crash Course")['completed_concepts'])
    completed_items += skills_completed

    percentage = int((completed_items / total_items) * 100) if total_items > 0 else 0
    recent_log = progress['daily_log'][-10:] if progress['daily_log'] else []

    return jsonify({
        'percentage': percentage,
        'orientation_status': ch(progress, "The Agent Factory Orientation")['status'],
        'foundations_completed': 1 if ch(progress, "Foundations")['status'] == 'completed' else 0,
        'whatai_completed': whatai_completed,
        'whatai_completed_ideas': [int(x) for x in ch(progress, "What AI Actually Is")['completed_ideas']],
        'thesis_completed': thesis_completed,
        'thesis_completed_arguments': [int(a) for a in ch(progress, "The Agent Factory Thesis")['completed_arguments']],
        'operating_completed': operating_completed,
        'operating_completed_concepts': [int(c) for c in ch(progress, "The AI Operating Layer")['completed_concepts']],
        'qs_status': ch(progress, "Quick Start")['status'],
        'ai_completed': ai_completed,
        'ai_completed_concepts': [int(c) for c in ch(progress, "AI Prompting 2026")['completed_concepts']],
        'markdown_completed': markdown_completed,
        'markdown_completed_concepts': [int(c) for c in ch(progress, "Markdown In, HTML Out")['completed_concepts']],
        'code_completed': code_completed,
        'code_completed_concepts': [int(c) for c in ch(progress, "Code You Never Write")['completed_concepts']],
        'skills_completed': skills_completed,
        'skills_completed_concepts': [int(c) for c in ch(progress, "Skills & Connectors Crash Course")['completed_concepts']],
        'recent_log': recent_log
    })

# ── /record_study ─────────────────────────────────────────────────────────────

@app.route('/record_study', methods=['POST'])
def record_study():
    try:
        data = request.json
        chapter = data.get('chapter')
        completed = str(data.get('completed'))
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

        if chapter not in CHAPTER_CONFIG:
            return jsonify({'success': False, 'message': f'Unknown chapter: {chapter}'}), 400

        progress = load_progress()
        cfg = CHAPTER_CONFIG[chapter]
        max_val = cfg['max']
        field = cfg['field']

        # Validate number
        if chapter in PAGE_CHAPTERS:
            if completed != '1':
                return jsonify({'success': False, 'message': f'{chapter} only has 1 page. Please enter 1.'}), 400
            if ch(progress, chapter)['status'] == 'completed':
                return jsonify({'success': False, 'message': f'{chapter} is already completed!'}), 400
        else:
            try:
                num = int(completed)
                if num < 1 or num > max_val:
                    return jsonify({'success': False, 'message': f'Invalid number! Please enter a number between 1 and {max_val}.'}), 400
            except ValueError:
                return jsonify({'success': False, 'message': f'Please enter a valid number (1-{max_val})'}), 400

            target = int(completed)
            current_set = set(ch(progress, chapter)[field])
            # Find which new numbers need to be added (from next uncompleted up to target)
            new_items = [str(i) for i in range(1, target + 1) if str(i) not in current_set]
            if not new_items:
                next_num = len(current_set) + 1
                return jsonify({'success': False, 'message': f'Already completed up to {target}! Try {next_num} next.'}), 400

        # ── For page chapters ──
        if chapter in PAGE_CHAPTERS:
            progress['daily_log'].append({
                'date': date, 'chapter': chapter, 'completed': completed, 'notes': ''
            })
            ch(progress, chapter)['completed_topics'] = [completed]
            ch(progress, chapter)['status'] = 'completed'
            next_msg = "\n\nCongratulations! You completed this chapter!"

        # ── For sequential chapters ──
        else:
            progress['daily_log'].append({
                'date': date, 'chapter': chapter, 'completed': f'1-{target}', 'notes': ''
            })
            ch(progress, chapter)[field].extend(new_items)
            ch(progress, chapter).setdefault('completed_dates', []).append(date)
            ch(progress, chapter)[field].sort(key=int)
            ch(progress, chapter)['status'] = 'in_progress'
            if len(ch(progress, chapter)[field]) >= max_val:
                ch(progress, chapter)['status'] = 'completed'

            current_count = len(ch(progress, chapter)[field])
            if current_count < max_val:
                next_msg = f"\n\nNext: Try {current_count + 1}/{max_val}"
            else:
                next_msg = f"\n\nCongratulations! You completed {chapter}!"

        progress['last_updated'] = date
        save_progress(progress)
        return jsonify({'success': True, 'message': f'Recorded: {chapter} - up to {completed}/{max_val}{next_msg}'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ── /delete_activity ──────────────────────────────────────────────────────────

@app.route('/delete_activity', methods=['POST'])
def delete_activity():
    try:
        data = request.json
        date = data.get('date')
        chapter = data.get('chapter')

        progress = load_progress()

        if chapter not in CHAPTER_CONFIG:
            return jsonify({'success': False, 'message': f'Unknown chapter: {chapter}'}), 400

        completed_value = None
        for log in progress['daily_log']:
            if log['date'] == date and log['chapter'] == chapter:
                completed_value = log['completed']
                break

        if completed_value:
            progress['daily_log'] = [
                log for log in progress['daily_log']
                if not (log['date'] == date and log['chapter'] == chapter)
            ]

            field = CHAPTER_CONFIG[chapter]['field']
            if chapter in PAGE_CHAPTERS:
                if completed_value in ch(progress, chapter).get('completed_topics', []):
                    ch(progress, chapter)['completed_topics'].remove(completed_value)
                    if not ch(progress, chapter).get('completed_topics'):
                        ch(progress, chapter)['status'] = 'not_started'
            else:
                # completed_value is now "1-N" format, reset the whole chapter
                ch(progress, chapter)[field] = []
                if 'completed_dates' in ch(progress, chapter):
                    ch(progress, chapter)['completed_dates'] = []
                ch(progress, chapter)['status'] = 'not_started'

        progress['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        save_progress(progress)
        return jsonify({'success': True, 'message': 'Activity deleted successfully!'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ── /delete_all_activities ────────────────────────────────────────────────────

@app.route('/delete_all_activities', methods=['POST'])
def delete_all_activities():
    try:
        progress = load_progress()
        progress['daily_log'] = []
        progress['chapters'] = get_default_chapters()
        progress['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        save_progress(progress)
        return jsonify({'success': True, 'message': 'All activities deleted successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

# ── /generate_progress ────────────────────────────────────────────────────────

@app.route('/generate_progress', methods=['POST'])
def generate_progress_report():
    try:
        progress = load_progress()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Calculate totals
        orientation_completed = 1 if ch(progress, "The Agent Factory Orientation")['status'] == 'completed' else 0
        foundations_completed = 1 if ch(progress, "Foundations")['status'] == 'completed' else 0
        whatai_completed = len(ch(progress, "What AI Actually Is")['completed_ideas'])
        thesis_completed = len(ch(progress, "The Agent Factory Thesis")['completed_arguments'])
        operating_completed = len(ch(progress, "The AI Operating Layer")['completed_concepts'])
        qs_completed = 1 if ch(progress, "Quick Start")['status'] == 'completed' else 0
        ai_completed = len(ch(progress, "AI Prompting 2026")['completed_concepts'])
        markdown_completed = len(ch(progress, "Markdown In, HTML Out")['completed_concepts'])
        code_completed = len(ch(progress, "Code You Never Write")['completed_concepts'])
        skills_completed = len(ch(progress, "Skills & Connectors Crash Course")['completed_concepts'])

        completed_items = (
            orientation_completed + foundations_completed + whatai_completed +
            thesis_completed + operating_completed + qs_completed +
            ai_completed + markdown_completed + code_completed + skills_completed
        )
        total_items = 1 + 1 + 9 + 16 + 10 + 1 + 13 + 14 + 13 + 6
        overall_percentage = int((completed_items / total_items) * 100) if total_items > 0 else 0

        # Write TXT report
        report_file = REPORTS_PATH / f'progress_report_{timestamp}.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STUDY PROGRESS REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"OVERALL COMPLETION: {overall_percentage}%\n")
            f.write(f"   Total Items Completed: {completed_items}/{total_items}\n\n")
            f.write("-" * 40 + "\n")
            f.write("DETAILED BREAKDOWN\n")
            f.write("-" * 40 + "\n\n")

            sections = [
                ("1. Orientation", orientation_completed, 1, ch(progress, "The Agent Factory Orientation")['completed_topics']),
                ("2. Foundations", foundations_completed, 1, ch(progress, "Foundations")['completed_topics']),
                ("3. What AI Actually Is", whatai_completed, 9, ch(progress, "What AI Actually Is")['completed_ideas']),
                ("4. The Agent Factory Thesis", thesis_completed, 16, ch(progress, "The Agent Factory Thesis")['completed_arguments']),
                ("5. The AI Operating Layer", operating_completed, 10, ch(progress, "The AI Operating Layer")['completed_concepts']),
                ("6. Quick Start", qs_completed, 1, ch(progress, "Quick Start")['completed_topics']),
                ("7. AI Prompting 2026", ai_completed, 13, ch(progress, "AI Prompting 2026")['completed_concepts']),
                ("8. Markdown In, HTML Out", markdown_completed, 14, ch(progress, "Markdown In, HTML Out")['completed_concepts']),
                ("9. Code You Never Write", code_completed, 13, ch(progress, "Code You Never Write")['completed_concepts']),
                ("10. Skills & Connectors", skills_completed, 6, ch(progress, "Skills & Connectors Crash Course")['completed_concepts'])
            ]

            for title, completed, total, items in sections:
                pct = int(completed / total * 100) if total > 0 else 0
                f.write(f"{title}: {completed}/{total} ({pct}%)\n")
                if completed > 0:
                    f.write(f"   Completed: {', '.join(items)}\n")
                    if completed < total:
                        next_val = int(max(items, key=int)) + 1 if items else 1
                        f.write(f"   Next: {next_val}\n")
                else:
                    f.write("   Not started yet\n")
                f.write("\n")

            f.write("-" * 40 + "\n")
            f.write("RECENT ACTIVITY LOG\n")
            f.write("-" * 40 + "\n\n")
            if progress['daily_log']:
                for log in progress['daily_log'][-20:]:
                    f.write(f"{log['date']}: {log['chapter']} - {log['completed']}\n")
            else:
                f.write("No activities recorded yet.\n")

            f.write("\n" + "-" * 40 + "\n")
            f.write("SUMMARY\n")
            f.write("-" * 40 + "\n\n")
            unique_dates = set(log['date'] for log in progress['daily_log'])
            f.write(f"Days studied: {len(unique_dates)}\n")
            f.write(f"Total activities: {len(progress['daily_log'])}\n")
            if unique_dates:
                f.write(f"Last activity: {max(unique_dates)}\n")
            f.write("\n" + "=" * 70 + "\n")
            f.write("Keep going! Every step brings you closer to mastery.\n")
            f.write("Mode 2: AI worker runs automatically. You build once. It works forever.\n")
            f.write("=" * 70 + "\n")

        # Write HTML report
        html_file = REPORTS_PATH / f'progress_report_{timestamp}.html'

        def badge(status, completed, total):
            if completed >= total:
                return 'completed', '✓ Complete'
            elif completed > 0:
                return 'in-progress', f'🔄 {completed}/{total}'
            return 'not-started', '⏳ Not Started'

        html_sections = ''
        for num, title, key, completed, total, items_field in [
            (1, "Orientation", "The Agent Factory Orientation", orientation_completed, 1, 'completed_topics'),
            (2, "Foundations (Everyone)", "Foundations", foundations_completed, 1, 'completed_topics'),
            (3, "What AI Actually Is", "What AI Actually Is", whatai_completed, 9, 'completed_ideas'),
            (4, "The Agent Factory Thesis", "The Agent Factory Thesis", thesis_completed, 16, 'completed_arguments'),
            (5, "The AI Operating Layer", "The AI Operating Layer", operating_completed, 10, 'completed_concepts'),
            (6, "Quick Start", "Quick Start", qs_completed, 1, 'completed_topics'),
            (7, "AI Prompting 2026", "AI Prompting 2026", ai_completed, 13, 'completed_concepts'),
            (8, "Markdown In, HTML Out", "Markdown In, HTML Out", markdown_completed, 14, 'completed_concepts'),
            (9, "Code You Never Write", "Code You Never Write", code_completed, 13, 'completed_concepts'),
            (10, "Skills & Connectors", "Skills & Connectors Crash Course", skills_completed, 6, 'completed_concepts')
        ]:
            b_cls, b_txt = badge(None, completed, total)
            items_list = ', '.join(ch(progress, key).get(items_field, [])) if completed > 0 else ''
            start_text = f'Start with {items_field.replace("completed_","").rstrip("s").title()} 1' if not items_list else ''
            html_sections += f"""
        <div class="section">
            <h3>{num}. {title}</h3>
            <span class="badge {b_cls}">{b_txt}</span>
            <p>{f'Completed: {items_list}' if items_list else start_text}</p>
        </div>"""

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Study Progress Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f8fafc; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 16px; }}
        h1 {{ color: #4f46e5; }}
        .progress {{ background: #e2e8f0; border-radius: 10px; height: 20px; overflow: hidden; }}
        .progress-fill {{ background: linear-gradient(90deg, #4f46e5, #8b5cf6); height: 100%; width: {overall_percentage}%; }}
        .section {{ margin: 20px 0; padding: 15px; background: #f8fafc; border-radius: 8px; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
        .completed {{ background: #d1fae5; color: #065f46; }}
        .in-progress {{ background: #fed7aa; color: #92400e; }}
        .not-started {{ background: #fee2e2; color: #991b1b; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Study Progress Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <h2>Overall Completion: {overall_percentage}%</h2>
        <div class="progress"><div class="progress-fill"></div></div>
        <p>Total: {completed_items}/{total_items} items completed</p>
        {html_sections}
        <div class="section">
            <h3>Recent Activity</h3>
            <ul>
                {''.join([f'<li>{log["date"]}: {log["chapter"]} - {log["completed"]}</li>' for log in progress['daily_log'][-10:]])}
            </ul>
        </div>
        <p style="text-align:center;color:#64748b;margin-top:30px;">Designed By : Azmat Ali</p>
    </div>
</body>
</html>""")

        return jsonify({
            'success': True,
            'file_path': str(report_file),
            'html_path': str(html_file),
            'message': 'Report generated successfully!'
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error generating report: {str(e)}'}), 500

# ── /health ───────────────────────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health_check():
    progress = load_progress()
    return jsonify({
        'status': 'healthy',
        'data_file': str(DATA_PATH),
        'reports_folder': str(REPORTS_PATH),
        'last_updated': progress.get('last_updated'),
        'total_activities': len(progress.get('daily_log', []))
    })

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print("Mode 2 Backend Server Starting...")
    print(f"Data file: {DATA_PATH}")
    print(f"Reports folder: {REPORTS_PATH}")
    print(f"\nBook Structure ({len(ALL_CHAPTERS)} topics):")
    for i, ch_name in enumerate(ALL_CHAPTERS, 1):
        cfg = CHAPTER_CONFIG[ch_name]
        unit = cfg['field'].replace('completed_', '').rstrip('s')
        print(f"   {i:2d}. {ch_name}: {cfg['max']} {unit}")
    print("\nServer running at: http://localhost:8000")
    print("Available endpoints:")
    print("   GET  /progress - Get current progress")
    print("   POST /record_study - Record a study session")
    print("   POST /delete_activity - Delete an activity")
    print("   POST /delete_all_activities - Delete all activities")
    print("   POST /generate_progress - Generate report (TXT + HTML)")
    print("   GET  /health - Health check")
    print("=" * 60)
    app.run(host='localhost', port=8000, debug=True)
