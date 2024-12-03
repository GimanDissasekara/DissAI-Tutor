from fastapi import FastAPI
from knowledge import prerequisites, suggest_next_topic
from pydantic import BaseModel
from typing import List

app = FastAPI()

class CompletedTopics(BaseModel):
    topics: List[str]

@app.get("/")
def home():
    return {"message": "Welcome to DissAI Tutor!"}

@app.get("/prerequisites/{topic}")
def get_prerequisites(topic: str):
    if topic in prerequisites:
        return {"topic": topic, "prerequisites": prerequisites[topic]}
    else:
        return {"error": "Topic not found"}

@app.post("/suggest/")
def suggest_next(completed: CompletedTopics):
    suggested = suggest_next_topic(completed.topics)
    if suggested:
        return {"next_topic": suggested}
    else:
        return {"message": "No suggestions available. You might have completed all topics!"}

def main():
    print("Welcome to DissAI Tutor!")
    while True:
        print("\n1. Learn Prerequisites")
        print("2. Get Next Suggested Topic")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            topic = input("Enter the topic you want to learn: ").strip()
            if topic in prerequisites:
                print(f"The prerequisites for {topic} are: {', '.join(prerequisites[topic]) or 'None'}")
            else:
                print("Topic not found in the system.")
        
        elif choice == "2":
            completed = input("Enter the topics you have completed (comma-separated): ").strip().split(',')
            completed = [t.strip() for t in completed]
            suggested_topic = suggest_next_topic(completed)
            if suggested_topic:
                print(f"The next suggested topic for you is: {suggested_topic}")
            else:
                print("No suggestions available. You might have completed all topics!")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
