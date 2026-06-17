import json
import os
from datetime import datetime

PROGRESS_FILE = "../data/progress.json"

def load_progress():
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def record_study():
    print("\n📚 Record Your Study Progress")
    print("=" * 40)
    
    print("\nWhich chapter?")
    print("1. The Agent Factory Thesis")
    print("2. Quick Start")
    print("3. AI Prompting 2026")
    print("4. How to Think in AI Era")
    
    choice = input("\nEnter number (1-4): ")
    
    chapters = ["The Agent Factory Thesis", "Quick Start", "AI Prompting 2026", "How to Think in AI Era"]
    chapter = chapters[int(choice)-1]
    
    print(f"\n📖 {chapter}")
    
    if chapter == "The Agent Factory Thesis":
        print("\nArguments: 1. Core Thesis, 2. Vocabulary, 3. Paradigm Shift, 4. Economic Actors, 5. 10-80-10 Rule, 6. Two-Layer Model, 7. Two Modes, 8-14. Seven Invariants, 15. Reference Stack, 16. Workforce Opportunity")
        argument = input("Which argument number(s)? (e.g., '1,2,3'): ")
        
    elif chapter == "Quick Start":
        topic = input("What topic did you complete? (e.g., 'Mode 1 vs Mode 2'): ")
        pages = input("How many pages? (or press Enter): ")
        
    elif chapter == "AI Prompting 2026":
        print("\nConcepts: 1. Context, 2. Retrieval Modes, 3. Thinking Mode, 4. Sycophancy, 5. Brainstorm-Iterate, 6. Multimodal, 7. Data Analysis, 8-13. Others")
        concept = input("Which concept number(s)? (e.g., '1,2,3'): ")
        
    else:  # How to Think
        print("\nDisciplines: 1. Prediction Lock, 2. Reasoning Receipt, 3. Error Taxonomy, 4. Cascade Maps, 5. Named Thresholds, 6. Working WITH AI")
        discipline = input("Which discipline number(s)? (e.g., '1,2'): ")
    
    notes = input("Any notes? (optional): ")
    
    # Save to progress
    progress = load_progress()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    entry = {
        "date": today,
        "chapter": chapter,
        "completed": topic if chapter == "Quick Start" else concept if chapter == "AI Prompting 2026" else discipline,
        "notes": notes
    }
    
    progress["daily_log"].append(entry)
    progress["last_updated"] = today
    
    # Update chapter status
    if chapter == "Quick Start":
        progress["chapters"]["Quick Start"]["completed_topics"].append(topic)
        progress["chapters"]["Quick Start"]["status"] = "in_progress"
    elif chapter == "AI Prompting 2026":
        progress["chapters"]["AI Prompting 2026"]["completed_concepts"].extend(concept.split(','))
        progress["chapters"]["AI Prompting 2026"]["completed_dates"].append(today)
        if len(progress["chapters"]["AI Prompting 2026"]["completed_concepts"]) >= 13:
            progress["chapters"]["AI Prompting 2026"]["status"] = "completed"
        else:
            progress["chapters"]["AI Prompting 2026"]["status"] = "in_progress"
    else:
        progress["chapters"]["How to Think in AI Era"]["completed_disciplines"].extend(discipline.split(','))
        progress["chapters"]["How to Think in AI Era"]["completed_dates"].append(today)
        if len(progress["chapters"]["How to Think in AI Era"]["completed_disciplines"]) >= 6:
            progress["chapters"]["How to Think in AI Era"]["status"] = "completed"
        else:
            progress["chapters"]["How to Think in AI Era"]["status"] = "in_progress"
    
    save_progress(progress)
    
    print(f"\n✅ Recorded! Progress saved for {today}")
    print(f"📊 Total days studied: {len(progress['daily_log'])}")

if __name__ == "__main__":
    record_study()