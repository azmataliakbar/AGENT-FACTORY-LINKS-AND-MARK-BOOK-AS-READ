with open('backend/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

patches = []

# Find the line numbers of key anchors
for i, line in enumerate(lines):
    stripped = line.strip()

    # Step 1: Default data - add thesis chapter (after "How to Think" entry closing brace)
    if stripped.startswith('"status": "not_started"'):
        # Check if this is the last chapter entry (before daily_log)
        next_line = lines[i+1].strip() if i+1 < len(lines) else ''
        if next_line == '},' and 'daily_log' in lines[i+2]:
            # Mark this position for insertion
            patches.append(('default_chapter', i))

    # Step 4: Validation - add thesis elif (after Quick Start elif, before "# Add to daily_log")
    if stripped == "# Add to daily_log":
        patches.append(('validation', i))

    # Step 5: Update - add thesis elif 
    if stripped == "# Sort numerically for better display":
        patches.append(('update_sort', i))
    
    # Step 6: Sort
    if stripped == "progress['chapters']['How to Think in AI Era']['completed_disciplines'].sort(key=int)":
        patches.append(('sort_line', i))

for name, line_num in patches:
    print(f"{name}: line {line_num+1}")

# Apply patches in reverse order
thesis_default = '''                "The Agent Factory Thesis": {
                    "total_arguments": 16,
                    "completed_arguments": [],
                    "completed_dates": [],
                    "status": "not_started"
                },
'''

thesis_validation = '''        elif chapter == 'The Agent Factory Thesis':
            try:
                num = int(completed)
                if num < 1 or num > 16:
                    return jsonify({
                        'success': False, 
                        'message': f'\\u274c Invalid argument number! Please enter a number between 1 and 16.'
                    }), 400
            except ValueError:
                return jsonify({'success': False, 'message': '\\u274c Please enter a valid number (1-16)'}), 400
            
            # Check for duplicates
            if completed in progress['chapters'][chapter]['completed_arguments']:
                next_num = len(progress['chapters'][chapter]['completed_arguments']) + 1
                return jsonify({
                    'success': False, 
                    'message': f'\\u26a0\\ufe0f Argument {completed} already completed! Try argument {next_num} next.'
                }), 400
        
'''

thesis_update = '''        elif chapter == 'The Agent Factory Thesis':
            if completed not in progress['chapters'][chapter]['completed_arguments']:
                progress['chapters'][chapter]['completed_arguments'].append(completed)
                progress['chapters'][chapter]['completed_dates'].append(date)
                progress['chapters'][chapter]['status'] = 'in_progress'
                if len(progress['chapters'][chapter]['completed_arguments']) >= 16:
                    progress['chapters'][chapter]['status'] = 'completed'
        
'''

thesis_sort = '''        progress['chapters']['The Agent Factory Thesis']['completed_arguments'].sort(key=int)
'''

# Apply in reverse order so line numbers stay correct
for name, line_num in sorted(patches, key=lambda x: -x[1]):
    if name == 'default_chapter':
        # Insert after the closing brace + comma of the last chapter entry
        lines.insert(line_num + 1, thesis_default)
        print(f"Inserted thesis chapter after line {line_num+1}")
    elif name == 'validation':
        # Insert before "# Add to daily_log"
        lines.insert(line_num, thesis_validation)
        print(f"Inserted thesis validation before line {line_num+1}")
    elif name == 'update_sort':
        # Insert before "# Sort numerically for better display" (after the AI Prompting elif)
        lines.insert(line_num, thesis_update)
        print(f"Inserted thesis update before line {line_num+1}")
    elif name == 'sort_line':
        # Insert after the how_to_think sort line
        lines.insert(line_num + 1, thesis_sort)
        print(f"Inserted thesis sort after line {line_num+1}")

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

import py_compile
py_compile.compile('backend/app.py', doraise=True)
print("All patches applied, syntax OK!")
