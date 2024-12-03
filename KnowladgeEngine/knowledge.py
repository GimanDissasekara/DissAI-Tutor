from experta import KnowledgeEngine, Rule, Fact, DefFacts, MATCH

knowledge_data = [
    {"Topic": "Addition", 
     "If you struggle, I suggest": "Number Line", 
     "If you Master then you can do": "Perform complex arithmetic operations, solve algebraic equations, and analyze data.", 
     "Category": "Numbers"},
    {"Topic": "Negative number addition", 
     "If you struggle, I suggest": "Addition, Number Line", 
     "If you Master then you can do": "Solve equations involving negative numbers, analyze financial data, and understand physics concepts.", 
     "Category": "Numbers"},
    {"Topic": "Subtraction", 
     "If you struggle, I suggest": "Addition, Number Line", 
     "If you Master then you can do": "Understand debt calculations, solve equations, and measure differences effectively.", 
     "Category": "Numbers"},
    {"Topic": "Fractions", 
     "If you struggle, I suggest": "Multiplication, Division, Number Line", 
     "If you Master then you can do": "Perform advanced calculations, understand proportions, and interpret statistical data.", 
     "Category": "Numbers"},
    {"Topic": "Multiplication", 
     "If you struggle, I suggest": "Addition, Number Line", 
     "If you Master then you can do": "Work with exponents, solve area and volume problems, and understand scaling.", 
     "Category": "Numbers"},
    {"Topic": "Division", 
     "If you struggle, I suggest": "Subtraction, Multiplication, Number Line", 
     "If you Master then you can do": "Solve division problems, understand ratios, and perform unit conversions.", 
     "Category": "Numbers"},
    {"Topic": "Simple Equations", 
     "If you struggle, I suggest": "Addition, Subtraction, Multiplication, Division", 
     "If you Master then you can do": "Solve unknown variable problems, build logic for programming, and model basic systems.", 
     "Category": "Algebra"},
    {"Topic": "Simultaneous Equations", 
     "If you struggle, I suggest": "Simple Equations", 
     "If you Master then you can do": "Analyze multi-variable systems and apply concepts in economics and engineering.", 
     "Category": "Algebra"},
    {"Topic": "Quadratic Equations", 
     "If you struggle, I suggest": "Simple Equations, Simultaneous Equations", 
     "If you Master then you can do": "Understand parabolas, calculate projectile motion, and optimize engineering designs.", 
     "Category": "Algebra"},
    {"Topic": "Perimeter", 
     "If you struggle, I suggest": "Number Line", 
     "If you Master then you can do": "Calculate boundaries of shapes, solve real-world measurement problems, and design layouts.", 
     "Category": "Geometry"},
    {"Topic": "Area", 
     "If you struggle, I suggest": "Multiplication, Perimeter", 
     "If you Master then you can do": "Solve surface problems, understand spatial geometry, and design structures.", 
     "Category": "Geometry"},
    {"Topic": "Volume", 
     "If you struggle, I suggest": "Area", 
     "If you Master then you can do": "Solve problems in 3D space, design containers, and work with fluid dynamics.", 
     "Category": "Geometry"},
    {"Topic": "Probability", 
     "If you struggle, I suggest": "Fractions, Multiplication, Division", 
     "If you Master then you can do": "Analyze events, solve risk management problems, and interpret statistical models.", 
     "Category": "Statistics"},
    {"Topic": "Statistics", 
     "If you struggle, I suggest": "Fractions, Probability", 
     "If you Master then you can do": "Understand data trends, analyze experiments, and perform market analysis.", 
     "Category": "Statistics"},
    {"Topic": "Linear Graphs", 
     "If you struggle, I suggest": "Simple Equations", 
     "If you Master then you can do": "Analyze trends, model real-world problems, and solve linear optimization tasks.", 
     "Category": "Algebra"},
    {"Topic": "Quadratic Graphs", 
     "If you struggle, I suggest": "Quadratic Equations, Linear Graphs", 
     "If you Master then you can do": "Understand curves, predict motion paths, and explore advanced mathematical models.", 
     "Category": "Algebra"},
    {"Topic": "Trigonometry", 
     "If you struggle, I suggest": "Simple Equations, Geometry", 
     "If you Master then you can do": "Analyze waves, understand rotation and angles, and model periodic phenomena.", 
     "Category": "Trigonometry"},
    {"Topic": "Calculus", 
     "If you struggle, I suggest": "Simple Equations, Trigonometry", 
     "If you Master then you can do": "Model changes, optimize processes, and explore advanced scientific theories.", 
     "Category": "Calculus"}
]

class TutorExpertSystem(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(action="start")

    # Rule for recommending prerequisites based on struggles
    @Rule(Fact(action="start_tutoring"), Fact(struggling=MATCH.topic))
    def recommend_prerequisite(self, topic):
        for knowledge in knowledge_data:
            if knowledge["Topic"] == topic:
                print(f"To master {topic}, focus on these first: {knowledge['If you struggle, I suggest']}.")
                return  # Exit the loop after finding the topic

        print(f"Topic {topic} is not found in the knowledge base.")

    # Rule for recommending the next topic based on mastered topics
    @Rule(Fact(action="start_tutoring"), Fact(mastered=MATCH.mastered))
    def recommend_next_topic(self, mastered):
        mastered_topics = mastered.split(", ")  # Convert mastered topics into a list
        for knowledge in knowledge_data:
            # Skip topics that are already mastered
            if knowledge["Topic"] in mastered_topics:
                continue

            # Check if prerequisites for the topic are all mastered
            prerequisites = knowledge["If you struggle, I suggest"]
            if prerequisites == "-" or all(prereq in mastered_topics for prereq in prerequisites.split(", ")):
                print(f"Great job mastering {', '.join(mastered_topics)}! Next, try learning {knowledge['Topic']}.")
                break  # Exit the loop after recommending a topic
        else:
            print("You've mastered all the topics in the knowledge base!")

# Sample Knowledge Base (already defined)

# Sample Student Data
students = [
    {"name": "John", "struggling": "Fractions", "mastered": "Addition, Multiplication"},
    {"name": "Mary", "struggling": "Quadratic Equations", "mastered": "Simple Equations, Simultaneous Equations"},
    {"name": "Alice", "struggling": "Perimeter", "mastered": "Number Line"},
]

# Instantiate and run the expert system for each student
engine = TutorExpertSystem()

for student in students:
    print(f"\nRecommendations for {student['name']}:")
    engine.reset()  # Reset the engine for each student
    engine.declare(Fact(action="start_tutoring"))
    engine.declare(Fact(struggling=student["struggling"]))
    engine.declare(Fact(mastered=student["mastered"]))
    engine.run()