import os
from experta import *
import pandas as pd
import random

# Function to load the Excel file with error handling
def load_excel_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file not found at {file_path}")
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Error loading Excel file: {e}")

# Load subject relationships from Excel
file_path = 'Data.xlsx'
try:
    sheet_data = load_excel_file(file_path)
except (FileNotFoundError, ValueError) as e:
    print(f"<p style='color: red;'>{e}</p>")
    exit()

# Parse the subject relationships
subject_relationships = {}
for _, row in sheet_data.iterrows():
    topic = row['Topic']
    prerequisites = row['If you struggle, I suggest'].split(', ') if pd.notna(row['If you struggle, I suggest']) else []
    advanced_topics = row['If you Master then you can do'].split(', ') if pd.notna(row['If you Master then you can do']) else []
    
    group = row.get('Group', 'Unknown')

    subject_relationships[topic] = {
        'Group': group,
        'Prerequisites': prerequisites,
        'Advanced Topics': advanced_topics,
        'Category': row['Category']
    }

def get_recommendations(struggling_topic, mastered_topic, marks):
    # Input validation
    if not struggling_topic or not mastered_topic:
        return (
            ["Please select both struggling and mastered subjects"],
            "Missing input",
            ["Ensure you've selected subjects for both fields"]
        )

    # Prevent same subject selection
    if struggling_topic == mastered_topic:
        return (
            ["Error: Cannot select the same subject for struggling and mastered"],
            "Input Validation Error",
            ["Please choose different subjects for struggling and mastered"]
        )

    # Uncertainty and confidence calculation
    uncertainty_factors = []
    confidence_score = 0

    # Marks-based analysis
    difficulty_levels = {
        (0, 35): {"level": "Low", "recommendations": "Basic Improvement"},
        (35, 50): {"level": "Below Average", "recommendations": "Fundamental Strengthening"},
        (50, 70): {"level": "Average", "recommendations": "Targeted Practice"},
        (70, 90): {"level": "Good", "recommendations": "Advanced Concepts"},
        (90, 100): {"level": "Excellent", "recommendations": "Mastery and Exploration"}
    }

    # Determine difficulty level and recommendations
    current_level = None
    for (low, high), level_info in difficulty_levels.items():
        if low <= marks < high:
            current_level = level_info
            break

    # Suggestions generation
    suggestions = []
    explanations = []
    alternative_solutions = []

    # Check prerequisites for struggling topic
    if struggling_topic in subject_relationships:
        prerequisites = subject_relationships[struggling_topic]['Prerequisites']
        if prerequisites:
            suggestions.append(f"For {struggling_topic}, focus on prerequisites: {', '.join(prerequisites)}")
            explanations.append(f"You are struggling with {struggling_topic}. Mastering the prerequisites will help you improve.")
            uncertainty_factors.append(f"Prerequisite gap in {struggling_topic}")

    # Advanced topics for mastered subject
    if mastered_topic in subject_relationships:
        advanced_topics = subject_relationships[mastered_topic]['Advanced Topics']
        if advanced_topics:
            suggestions.append(f"Since you've mastered {mastered_topic}, explore: {', '.join(advanced_topics)}")
            explanations.append(f"You've shown mastery in {mastered_topic}. These topics will help you further enhance your skills.")
            confidence_score += 20

    # Difficulty level recommendations
    if current_level:
        suggestions.append(f"{current_level['recommendations']} strategy recommended")
        explanations.append(f"Based on your marks ({marks}), you are at a {current_level['level']} performance level.")

        # Generate uncertainty and confidence insights
        if marks < 50:
            uncertainty_factors.append("High learning uncertainty")
            alternative_solutions.append("Consider additional tutoring or guided learning")
        elif 50 <= marks < 70:
            uncertainty_factors.append("Moderate learning variability")
            alternative_solutions.append("Focus on targeted practice and concept clarification")
        else:
            confidence_score += 30
            alternative_solutions.append("Continue challenging yourself with advanced problems")

    # Randomized learning tip
    learning_tips = [
        "Break complex topics into smaller, manageable chunks",
        "Use visualization techniques to understand abstract concepts",
        "Practice regularly to build muscle memory for problem-solving",
        "Seek help when you're stuck - don't hesitate to ask questions"
    ]
    suggestions.append(f"Learning Tip: {random.choice(learning_tips)}")

    # Confidence and uncertainty summary
    if uncertainty_factors:
        explanations.append(f"Potential Learning Challenges: {', '.join(uncertainty_factors)}")

    return suggestions, "\n".join(explanations), alternative_solutions