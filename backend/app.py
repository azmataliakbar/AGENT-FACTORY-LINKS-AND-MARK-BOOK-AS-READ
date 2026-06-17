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

def load_progress():
    """Load progress data from JSON file"""
    try:
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default progress data if file doesn't exist
        default_data = {
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "total_chapters": 7,
            "chapters": {
                "The Agent Factory Orientation": {
                    "total_pages": 1,
                    "completed_pages": 0,
                    "completed_topics": [],
                    "status": "not_started"
                },
                "The Agent Factory Thesis": {
                    "total_arguments": 16,
                    "completed_arguments": [],
                    "completed_dates": [],
                    "status": "not_started"
                },
                "The AI Operating Layer": {
                    "total_concepts": 10,
                    "completed_concepts": [],
                    "completed_dates": [],
                    "status": "not_started"
                },
                "Quick Start": {
                    "total_pages": 1,
                    "completed_pages": 0,
                    "completed_topics": [],
                    "status": "not_started"
                },
                "AI Prompting 2026": {
                    "total_concepts": 13,
                    "completed_concepts": [],
                    "completed_dates": [],
                    "status": "not_started"
                },
                "Markdown In, HTML Out": {
                    "total_concepts": 14,
                    "completed_concepts": [],
                    "completed_dates": [],
                    "status": "not_started"
                },
                "Skills & Connectors Crash Course": {
                    "total_concepts": 6,
                    "completed_concepts": [],
                    "completed_dates": [],
                    "status": "not_started"
                }
            },
            "daily_log": [],
            "exam_date": None,
            "study_target": None
        }
        save_progress(default_data)
        return default_data

def save_progress(data):
    """Save progress data to JSON file"""
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/progress', methods=['GET'])
def get_progress():
    """Get current progress data for frontend display"""
    progress = load_progress()
    
    # Calculate completion percentage correctly
    total_items = 0
    completed_items = 0
    
    # Orientation (1 page)
    total_items += 1
    if progress['chapters']['The Agent Factory Orientation']['status'] == 'completed':
        completed_items += 1
    
    # The Agent Factory Thesis (16 arguments)
    total_items += 16
    thesis_completed_arguments = progress['chapters']['The Agent Factory Thesis']['completed_arguments']
    thesis_completed = len(thesis_completed_arguments)
    completed_items += thesis_completed
    
    # AI Operating Layer (10 concepts)
    total_items += 10
    operating_completed_concepts = progress['chapters']['The AI Operating Layer']['completed_concepts']
    operating_completed = len(operating_completed_concepts)
    completed_items += operating_completed
    
    # Quick Start (1 page)
    total_items += 1
    if progress['chapters']['Quick Start']['status'] == 'completed':
        completed_items += 1
    
    # AI Prompting (13 concepts)
    total_items += 13
    ai_completed_concepts = progress['chapters']['AI Prompting 2026']['completed_concepts']
    ai_completed = len(ai_completed_concepts)
    completed_items += ai_completed
    
    # Markdown In, HTML Out (14 concepts)
    total_items += 14
    markdown_completed_concepts = progress['chapters']['Markdown In, HTML Out']['completed_concepts']
    markdown_completed = len(markdown_completed_concepts)
    completed_items += markdown_completed
    
    # Skills & Connectors (6 concepts)
    total_items += 6
    skills_completed_concepts = progress['chapters']['Skills & Connectors Crash Course']['completed_concepts']
    skills_completed = len(skills_completed_concepts)
    completed_items += skills_completed
    
    # Calculate percentage (rounded)
    percentage = int((completed_items / total_items) * 100) if total_items > 0 else 0
    
    # Get recent activity (last 10 entries)
    recent_log = progress['daily_log'][-10:] if progress['daily_log'] else []
    
    response = {
        'percentage': percentage,
        'thesis_completed': thesis_completed,
        'thesis_completed_arguments': [int(a) for a in thesis_completed_arguments],
        'operating_completed': operating_completed,
        'operating_completed_concepts': [int(c) for c in operating_completed_concepts],
        'qs_status': progress['chapters']['Quick Start']['status'],
        'orientation_status': progress['chapters']['The Agent Factory Orientation']['status'],
        'ai_completed': ai_completed,
        'ai_completed_concepts': [int(c) for c in ai_completed_concepts],
        'markdown_completed': markdown_completed,
        'markdown_completed_concepts': [int(c) for c in markdown_completed_concepts],
        'skills_completed': skills_completed,
        'skills_completed_concepts': [int(c) for c in skills_completed_concepts],
        'recent_log': recent_log
    }
    
    return jsonify(response)

@app.route('/record_study', methods=['POST'])
def record_study():
    """Record a study session with validation"""
    try:
        data = request.json
        chapter = data.get('chapter')
        completed = str(data.get('completed'))
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        progress = load_progress()
        
        # VALIDATION: Check if the number is within range and valid
        if chapter == 'The Agent Factory Thesis':
            try:
                num = int(completed)
                if num < 1 or num > 16:
                    return jsonify({
                        'success': False, 
                        'message': f'Invalid argument number! Please enter a number between 1 and 16.'
                    }), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Please enter a valid number (1-16)'}), 400
            
            if completed in progress['chapters'][chapter]['completed_arguments']:
                next_num = len(progress['chapters'][chapter]['completed_arguments']) + 1
                return jsonify({
                    'success': False, 
                    'message': f'Argument {completed} already completed! Try argument {next_num} next.'
                }), 400
        
        elif chapter == 'The AI Operating Layer':
            try:
                num = int(completed)
                if num < 1 or num > 10:
                    return jsonify({
                        'success': False, 
                        'message': f'Invalid concept number! Please enter a number between 1 and 10.'
                    }), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Please enter a valid number (1-10)'}), 400
            
            if completed in progress['chapters'][chapter]['completed_concepts']:
                next_num = len(progress['chapters'][chapter]['completed_concepts']) + 1
                return jsonify({
                    'success': False, 
                    'message': f'Concept {completed} already completed! Try concept {next_num} next.'
                }), 400
        
        elif chapter == 'Quick Start':
            if completed != '1':
                return jsonify({
                    'success': False, 
                    'message': f'Quick Start only has 1 page. Please enter 1.'
                }), 400
            
            if progress['chapters'][chapter]['status'] == 'completed':
                return jsonify({
                    'success': False, 
                    'message': f'Quick Start is already completed!'
                }), 400
        
        elif chapter == 'The Agent Factory Orientation':
            if completed != '1':
                return jsonify({
                    'success': False, 
                    'message': f'Orientation only has 1 page. Please enter 1.'
                }), 400
            
            if progress['chapters'][chapter]['status'] == 'completed':
                return jsonify({
                    'success': False, 
                    'message': f'Orientation is already completed!'
                }), 400
        
        elif chapter == 'AI Prompting 2026':
            try:
                num = int(completed)
                if num < 1 or num > 13:
                    return jsonify({
                        'success': False, 
                        'message': f'Invalid concept number! Please enter a number between 1 and 13.'
                    }), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Please enter a valid number (1-13)'}), 400
            
            if completed in progress['chapters'][chapter]['completed_concepts']:
                next_num = len(progress['chapters'][chapter]['completed_concepts']) + 1
                return jsonify({
                    'success': False, 
                    'message': f'Concept {completed} already completed! Try concept {next_num} next.'
                }), 400
        
        elif chapter == 'Markdown In, HTML Out':
            try:
                num = int(completed)
                if num < 1 or num > 14:
                    return jsonify({
                        'success': False, 
                        'message': f'Invalid concept number! Please enter a number between 1 and 14.'
                    }), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Please enter a valid number (1-14)'}), 400
            
            if completed in progress['chapters'][chapter]['completed_concepts']:
                next_num = len(progress['chapters'][chapter]['completed_concepts']) + 1
                return jsonify({
                    'success': False, 
                    'message': f'Concept {completed} already completed! Try concept {next_num} next.'
                }), 400
        
        elif chapter == 'Skills & Connectors Crash Course':
            try:
                num = int(completed)
                if num < 1 or num > 6:
                    return jsonify({
                        'success': False, 
                        'message': f'Invalid concept number! Please enter a number between 1 and 6.'
                    }), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Please enter a valid number (1-6)'}), 400
            
            if completed in progress['chapters'][chapter]['completed_concepts']:
                next_num = len(progress['chapters'][chapter]['completed_concepts']) + 1
                return jsonify({
                    'success': False, 
                    'message': f'Concept {completed} already completed! Try concept {next_num} next.'
                }), 400
        
        else:
            return jsonify({'success': False, 'message': f'Unknown chapter: {chapter}'}), 400
        
        # Add to daily_log
        progress['daily_log'].append({
            'date': date,
            'chapter': chapter,
            'completed': completed,
            'notes': ''
        })
        
        # Update chapter progress
        if chapter == 'The Agent Factory Thesis':
            if completed not in progress['chapters'][chapter]['completed_arguments']:
                progress['chapters'][chapter]['completed_arguments'].append(completed)
                progress['chapters'][chapter]['completed_dates'].append(date)
                progress['chapters'][chapter]['status'] = 'in_progress'
                if len(progress['chapters'][chapter]['completed_arguments']) >= 16:
                    progress['chapters'][chapter]['status'] = 'completed'
                    
        elif chapter == 'The AI Operating Layer':
            if completed not in progress['chapters'][chapter]['completed_concepts']:
                progress['chapters'][chapter]['completed_concepts'].append(completed)
                progress['chapters'][chapter]['completed_dates'].append(date)
                progress['chapters'][chapter]['status'] = 'in_progress'
                if len(progress['chapters'][chapter]['completed_concepts']) >= 10:
                    progress['chapters'][chapter]['status'] = 'completed'
                    
        elif chapter == 'Quick Start':
            if progress['chapters'][chapter]['status'] != 'completed':
                progress['chapters'][chapter]['completed_topics'].append(completed)
                progress['chapters'][chapter]['status'] = 'completed'
                
        elif chapter == 'The Agent Factory Orientation':
            if progress['chapters'][chapter]['status'] != 'completed':
                progress['chapters'][chapter]['completed_topics'].append(completed)
                progress['chapters'][chapter]['status'] = 'completed'
                
        elif chapter == 'AI Prompting 2026':
            if completed not in progress['chapters'][chapter]['completed_concepts']:
                progress['chapters'][chapter]['completed_concepts'].append(completed)
                progress['chapters'][chapter]['completed_dates'].append(date)
                progress['chapters'][chapter]['status'] = 'in_progress'
                if len(progress['chapters'][chapter]['completed_concepts']) >= 13:
                    progress['chapters'][chapter]['status'] = 'completed'
                    
        elif chapter == 'Markdown In, HTML Out':
            if completed not in progress['chapters'][chapter]['completed_concepts']:
                progress['chapters'][chapter]['completed_concepts'].append(completed)
                progress['chapters'][chapter]['completed_dates'].append(date)
                progress['chapters'][chapter]['status'] = 'in_progress'
                if len(progress['chapters'][chapter]['completed_concepts']) >= 14:
                    progress['chapters'][chapter]['status'] = 'completed'
                    
        elif chapter == 'Skills & Connectors Crash Course':
            if completed not in progress['chapters'][chapter]['completed_concepts']:
                progress['chapters'][chapter]['completed_concepts'].append(completed)
                progress['chapters'][chapter]['completed_dates'].append(date)
                progress['chapters'][chapter]['status'] = 'in_progress'
                if len(progress['chapters'][chapter]['completed_concepts']) >= 6:
                    progress['chapters'][chapter]['status'] = 'completed'
        
        # Sort numerically for better display
        for ch in ['The AI Operating Layer', 'AI Prompting 2026', 'Markdown In, HTML Out', 'Skills & Connectors Crash Course']:
            if 'completed_concepts' in progress['chapters'][ch]:
                progress['chapters'][ch]['completed_concepts'].sort(key=int)
        progress['chapters']['The Agent Factory Thesis']['completed_arguments'].sort(key=int)
        
        progress['last_updated'] = date
        save_progress(progress)
        
        # Calculate next suggestion
        if chapter == 'The Agent Factory Thesis':
            current_count = len(progress['chapters'][chapter]['completed_arguments'])
            total = 16
            if current_count < total:
                next_msg = f"\n\nNext: Try argument {current_count + 1}/16"
            else:
                next_msg = "\n\nCongratulations! You completed The Agent Factory Thesis!"
        elif chapter == 'The AI Operating Layer':
            current_count = len(progress['chapters'][chapter]['completed_concepts'])
            total = 10
            if current_count < total:
                next_msg = f"\n\nNext: Try concept {current_count + 1}/10"
            else:
                next_msg = "\n\nCongratulations! You completed The AI Operating Layer!"
        elif chapter == 'AI Prompting 2026':
            current_count = len(progress['chapters'][chapter]['completed_concepts'])
            total = 13
            if current_count < total:
                next_msg = f"\n\nNext: Try concept {current_count + 1}/13"
            else:
                next_msg = "\n\nCongratulations! You completed AI Prompting 2026!"
        elif chapter == 'Markdown In, HTML Out':
            current_count = len(progress['chapters'][chapter]['completed_concepts'])
            total = 14
            if current_count < total:
                next_msg = f"\n\nNext: Try concept {current_count + 1}/14"
            else:
                next_msg = "\n\nCongratulations! You completed Markdown In, HTML Out!"
        elif chapter == 'Skills & Connectors Crash Course':
            current_count = len(progress['chapters'][chapter]['completed_concepts'])
            total = 6
            if current_count < total:
                next_msg = f"\n\nNext: Try concept {current_count + 1}/6"
            else:
                next_msg = "\n\nCongratulations! You completed Skills & Connectors!"
        else:  # Quick Start or Orientation
            next_msg = "\n\nCongratulations! You completed this chapter!"
        
        return jsonify({
            'success': True, 
            'message': f'Recorded: {chapter} - {completed}/{1 if chapter in ("Quick Start", "The Agent Factory Orientation") else "total"}{next_msg}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/delete_activity', methods=['POST'])
def delete_activity():
    """Delete a study activity"""
    try:
        data = request.json
        date = data.get('date')
        chapter = data.get('chapter')
        
        progress = load_progress()
        
        # Find the completed value for this activity
        completed_value = None
        log_to_delete = None
        for log in progress['daily_log']:
            if log['date'] == date and log['chapter'] == chapter:
                completed_value = log['completed']
                log_to_delete = log
                break
        
        if completed_value and log_to_delete:
            # Remove from daily_log
            progress['daily_log'] = [
                log for log in progress['daily_log'] 
                if not (log['date'] == date and log['chapter'] == chapter)
            ]
            
            # Remove from chapter progress
            if chapter == 'The Agent Factory Thesis':
                if completed_value in progress['chapters'][chapter]['completed_arguments']:
                    idx = progress['chapters'][chapter]['completed_arguments'].index(completed_value)
                    progress['chapters'][chapter]['completed_arguments'].pop(idx)
                    progress['chapters'][chapter]['completed_dates'].pop(idx)
                    
                    if len(progress['chapters'][chapter]['completed_arguments']) == 0:
                        progress['chapters'][chapter]['status'] = 'not_started'
                    else:
                        progress['chapters'][chapter]['status'] = 'in_progress'
                        
            elif chapter in ('Quick Start', 'The Agent Factory Orientation'):
                progress['chapters'][chapter]['completed_topics'] = []
                progress['chapters'][chapter]['status'] = 'not_started'
                
            elif chapter in ('The AI Operating Layer', 'AI Prompting 2026', 'Markdown In, HTML Out', 'Skills & Connectors Crash Course'):
                if completed_value in progress['chapters'][chapter]['completed_concepts']:
                    idx = progress['chapters'][chapter]['completed_concepts'].index(completed_value)
                    progress['chapters'][chapter]['completed_concepts'].pop(idx)
                    progress['chapters'][chapter]['completed_dates'].pop(idx)
                    
                    if len(progress['chapters'][chapter]['completed_concepts']) == 0:
                        progress['chapters'][chapter]['status'] = 'not_started'
                    else:
                        progress['chapters'][chapter]['status'] = 'in_progress'
        
        progress['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        save_progress(progress)
        
        return jsonify({'success': True, 'message': 'Activity deleted successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/delete_all_activities', methods=['POST'])
def delete_all_activities():
    """Delete all study activities"""
    try:
        progress = load_progress()
        
        # Clear daily log
        progress['daily_log'] = []
        
        # Reset all chapter progress
        progress['chapters']['The Agent Factory Orientation']['completed_topics'] = []
        progress['chapters']['The Agent Factory Orientation']['status'] = 'not_started'
        
        progress['chapters']['The Agent Factory Thesis']['completed_arguments'] = []
        progress['chapters']['The Agent Factory Thesis']['completed_dates'] = []
        progress['chapters']['The Agent Factory Thesis']['status'] = 'not_started'
        
        progress['chapters']['The AI Operating Layer']['completed_concepts'] = []
        progress['chapters']['The AI Operating Layer']['completed_dates'] = []
        progress['chapters']['The AI Operating Layer']['status'] = 'not_started'
        
        progress['chapters']['Quick Start']['completed_topics'] = []
        progress['chapters']['Quick Start']['status'] = 'not_started'
        
        progress['chapters']['AI Prompting 2026']['completed_concepts'] = []
        progress['chapters']['AI Prompting 2026']['completed_dates'] = []
        progress['chapters']['AI Prompting 2026']['status'] = 'not_started'
        
        progress['chapters']['Markdown In, HTML Out']['completed_concepts'] = []
        progress['chapters']['Markdown In, HTML Out']['completed_dates'] = []
        progress['chapters']['Markdown In, HTML Out']['status'] = 'not_started'
        
        progress['chapters']['Skills & Connectors Crash Course']['completed_concepts'] = []
        progress['chapters']['Skills & Connectors Crash Course']['completed_dates'] = []
        progress['chapters']['Skills & Connectors Crash Course']['status'] = 'not_started'
        
        progress['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        save_progress(progress)
        
        return jsonify({'success': True, 'message': 'All activities deleted successfully!'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/generate_progress', methods=['POST'])
def generate_progress_report():
    """Generate a progress report (TXT format)"""
    try:
        progress = load_progress()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = REPORTS_PATH / f'progress_report_{timestamp}.txt'
        
        # Calculate statistics
        total_items = 0
        completed_items = 0
        
        # Orientation
        orientation_completed = 1 if progress['chapters']['The Agent Factory Orientation']['status'] == 'completed' else 0
        completed_items += orientation_completed
        total_items += 1
        
        # Thesis
        thesis_completed = len(progress['chapters']['The Agent Factory Thesis']['completed_arguments'])
        completed_items += thesis_completed
        total_items += 16
        
        # AI Operating Layer
        operating_completed = len(progress['chapters']['The AI Operating Layer']['completed_concepts'])
        completed_items += operating_completed
        total_items += 10
        
        # Quick Start
        qs_completed = 1 if progress['chapters']['Quick Start']['status'] == 'completed' else 0
        completed_items += qs_completed
        total_items += 1
        
        # AI Prompting
        ai_completed = len(progress['chapters']['AI Prompting 2026']['completed_concepts'])
        completed_items += ai_completed
        total_items += 13
        
        # Markdown In, HTML Out
        markdown_completed = len(progress['chapters']['Markdown In, HTML Out']['completed_concepts'])
        completed_items += markdown_completed
        total_items += 14
        
        # Skills & Connectors
        skills_completed = len(progress['chapters']['Skills & Connectors Crash Course']['completed_concepts'])
        completed_items += skills_completed
        total_items += 6
        
        overall_percentage = int((completed_items / total_items) * 100) if total_items > 0 else 0
        
        # Write report
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
            
            # Orientation
            f.write(f"Orientation: {orientation_completed}/1 ({int(orientation_completed/1*100)}%)\n")
            f.write(f"   {'Page 1 completed' if orientation_completed else 'Not started yet'}\n\n")
            
            # Thesis
            f.write(f"The Agent Factory Thesis: {thesis_completed}/16 ({int(thesis_completed/16*100) if thesis_completed > 0 else 0}%)\n")
            if thesis_completed > 0:
                arguments = progress['chapters']['The Agent Factory Thesis']['completed_arguments']
                f.write(f"   Completed arguments: {', '.join(arguments)}\n")
                if thesis_completed < 16:
                    next_arg = int(max(arguments, key=int)) + 1 if arguments else 1
                    f.write(f"   Next: Argument {next_arg}\n")
            else:
                f.write("   Not started yet\n   Start with Argument 1\n")
            f.write("\n")
            
            # AI Operating Layer
            f.write(f"AI Operating Layer: {operating_completed}/10 ({int(operating_completed/10*100)}%)\n")
            if operating_completed > 0:
                concepts = progress['chapters']['The AI Operating Layer']['completed_concepts']
                f.write(f"   Completed concepts: {', '.join(concepts)}\n")
                if operating_completed < 10:
                    next_c = int(max(concepts, key=int)) + 1 if concepts else 1
                    f.write(f"   Next: Concept {next_c}\n")
            else:
                f.write("   Not started yet\n   Start with Concept 1\n")
            f.write("\n")
            
            # Quick Start
            f.write(f"Quick Start: {qs_completed}/1 ({int(qs_completed/1*100)}%)\n")
            f.write(f"   {'Page 1 completed' if qs_completed else 'Not started yet'}\n\n")
            
            # AI Prompting
            f.write(f"AI Prompting 2026: {ai_completed}/13 ({int(ai_completed/13*100)}%)\n")
            if ai_completed > 0:
                concepts = progress['chapters']['AI Prompting 2026']['completed_concepts']
                f.write(f"   Completed concepts: {', '.join(concepts)}\n")
                if ai_completed < 13:
                    next_concept = int(max(concepts, key=int)) + 1 if concepts else 1
                    f.write(f"   Next: Concept {next_concept}\n")
            else:
                f.write("   Not started yet\n   Start with Concept 1\n")
            f.write("\n")
            
            # Markdown
            f.write(f"Markdown In, HTML Out: {markdown_completed}/14 ({int(markdown_completed/14*100)}%)\n")
            if markdown_completed > 0:
                concepts = progress['chapters']['Markdown In, HTML Out']['completed_concepts']
                f.write(f"   Completed concepts: {', '.join(concepts)}\n")
                if markdown_completed < 14:
                    next_c = int(max(concepts, key=int)) + 1 if concepts else 1
                    f.write(f"   Next: Concept {next_c}\n")
            else:
                f.write("   Not started yet\n   Start with Concept 1\n")
            f.write("\n")
            
            # Skills
            f.write(f"Skills & Connectors: {skills_completed}/6 ({int(skills_completed/6*100)}%)\n")
            if skills_completed > 0:
                concepts = progress['chapters']['Skills & Connectors Crash Course']['completed_concepts']
                f.write(f"   Completed concepts: {', '.join(concepts)}\n")
                if skills_completed < 6:
                    next_c = int(max(concepts, key=int)) + 1 if concepts else 1
                    f.write(f"   Next: Concept {next_c}\n")
            else:
                f.write("   Not started yet\n   Start with Concept 1\n")
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
                latest_date = max(unique_dates)
                f.write(f"Last activity: {latest_date}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("Keep going! Every step brings you closer to mastery.\n")
            f.write("Mode 2: AI worker runs automatically. You build once. It works forever.\n")
            f.write("=" * 70 + "\n")
        
        # HTML report
        html_file = REPORTS_PATH / f'progress_report_{timestamp}.html'
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
        <div class="progress">
            <div class="progress-fill"></div>
        </div>
        <p>Total: {completed_items}/{total_items} items completed</p>
        
        <div class="section">
            <h3>1. Orientation</h3>
            <span class="badge {'completed' if orientation_completed else 'not-started'}">{'Complete' if orientation_completed else 'Not Started'}</span>
            <p>{'Page 1 completed' if orientation_completed else 'Complete Page 1'}</p>
        </div>
        
        <div class="section">
            <h3>2. The Agent Factory Thesis</h3>
            <span class="badge {'completed' if thesis_completed==16 else 'in-progress' if thesis_completed>0 else 'not-started'}">
                {'Complete' if thesis_completed==16 else f'{thesis_completed}/16' if thesis_completed>0 else 'Not Started'}
            </span>
            <p>{f'Completed arguments: {", ".join(progress["chapters"]["The Agent Factory Thesis"]["completed_arguments"])}' if thesis_completed>0 else 'Start with Argument 1'}</p>
        </div>
        
        <div class="section">
            <h3>3. The AI Operating Layer</h3>
            <span class="badge {'completed' if operating_completed==10 else 'in-progress' if operating_completed>0 else 'not-started'}">
                {'Complete' if operating_completed==10 else f'{operating_completed}/10' if operating_completed>0 else 'Not Started'}
            </span>
            <p>{f'Completed concepts: {", ".join(progress["chapters"]["The AI Operating Layer"]["completed_concepts"])}' if operating_completed>0 else 'Start with Concept 1'}</p>
        </div>
        
        <div class="section">
            <h3>4. Quick Start</h3>
            <span class="badge {'completed' if qs_completed else 'not-started'}">{'Complete' if qs_completed else 'Not Started'}</span>
            <p>{'Page 1 completed' if qs_completed else 'Complete Page 1'}</p>
        </div>
        
        <div class="section">
            <h3>5. AI Prompting 2026</h3>
            <span class="badge {'completed' if ai_completed==13 else 'in-progress' if ai_completed>0 else 'not-started'}">
                {'Complete' if ai_completed==13 else f'{ai_completed}/13' if ai_completed>0 else 'Not Started'}
            </span>
            <p>{f'Completed concepts: {", ".join(progress["chapters"]["AI Prompting 2026"]["completed_concepts"])}' if ai_completed>0 else 'Start with Concept 1'}</p>
        </div>
        
        <div class="section">
            <h3>6. Markdown In, HTML Out</h3>
            <span class="badge {'completed' if markdown_completed==14 else 'in-progress' if markdown_completed>0 else 'not-started'}">
                {'Complete' if markdown_completed==14 else f'{markdown_completed}/14' if markdown_completed>0 else 'Not Started'}
            </span>
            <p>{f'Completed concepts: {", ".join(progress["chapters"]["Markdown In, HTML Out"]["completed_concepts"])}' if markdown_completed>0 else 'Start with Concept 1'}</p>
        </div>
        
        <div class="section">
            <h3>7. Skills & Connectors Crash Course</h3>
            <span class="badge {'completed' if skills_completed==6 else 'in-progress' if skills_completed>0 else 'not-started'}">
                {'Complete' if skills_completed==6 else f'{skills_completed}/6' if skills_completed>0 else 'Not Started'}
            </span>
            <p>{f'Completed concepts: {", ".join(progress["chapters"]["Skills & Connectors Crash Course"]["completed_concepts"])}' if skills_completed>0 else 'Start with Concept 1'}</p>
        </div>
        
        <div class="section">
            <h3>Recent Activity</h3>
            <ul>
                {''.join([f'<li>{log["date"]}: {log["chapter"]} - {log["completed"]}</li>' for log in progress['daily_log'][-10:]])}
            </ul>
        </div>
    </div>
</body>
</html>""")
        
        return jsonify({
            'success': True, 
            'file_path': str(report_file),
            'html_path': str(html_file),
            'message': f'Report generated successfully!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error generating report: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    progress = load_progress()
    return jsonify({
        'status': 'healthy',
        'data_file': str(DATA_PATH),
        'reports_folder': str(REPORTS_PATH),
        'last_updated': progress.get('last_updated'),
        'total_activities': len(progress.get('daily_log', []))
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Mode 2 Backend Server Starting...")
    print(f"Data file: {DATA_PATH}")
    print(f"Reports folder: {REPORTS_PATH}")
    print("\nBook Structure (7 topics):")
    print("   1. The Agent Factory Orientation: 1 page")
    print("   2. The Agent Factory Thesis: 16 arguments")
    print("   3. The AI Operating Layer: 10 concepts")
    print("   4. Quick Start: 1 page")
    print("   5. AI Prompting 2026: 13 concepts")
    print("   6. Markdown In, HTML Out: 14 concepts")
    print("   7. Skills & Connectors Crash Course: 6 concepts")
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
