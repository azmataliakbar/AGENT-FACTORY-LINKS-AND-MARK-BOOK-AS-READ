import json
with open('data/progress.json', 'r') as f:
    data = json.load(f)

# Remove from How to Think chapter
if '1' in data['chapters']['How to Think in AI Era']['completed_disciplines']:
    data['chapters']['How to Think in AI Era']['completed_disciplines'].remove('1')
if '2026-05-25' in data['chapters']['How to Think in AI Era']['completed_dates']:
    data['chapters']['How to Think in AI Era']['completed_dates'].remove('2026-05-25')

# Update status if no completed disciplines left
if len(data['chapters']['How to Think in AI Era']['completed_disciplines']) == 0:
    data['chapters']['How to Think in AI Era']['status'] = 'not_started'

# Remove from daily_log
data['daily_log'] = [log for log in data['daily_log'] 
                     if not (log['date'] == '2026-05-25' and 
                             log['chapter'] == 'How to Think in AI Era')]

# Update last_updated
data['last_updated'] = '2026-05-25'

# Save back to file
with open('data/progress.json', 'w') as f:
    json.dump(data, f, indent=2)

print('✓ Entry deleted successfully!')
