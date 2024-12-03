from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt
from experta import KnowledgeEngine, Rule, Fact, MATCH

# Knowledge Base
knowledge_data = [
    {
      "Topic": "Addition",
      "If you struggle, I suggest": "Number Line",
      "If you Master then you can do": "Perform complex arithmetic operations, solve algebraic equations, and analyze data.",
      "Category": "Numbers",
      "Mark": 1
    },
    {
      "Topic": "Negative number addition",
      "If you struggle, I suggest": "Addition, Number Line",
      "If you Master then you can do": "Solve equations involving negative numbers, analyze financial data, and understand physics concepts.",
      "Category": "Numbers",
      "Mark": 1
    },
    {
      "Topic": "Subtraction",
      "If you struggle, I suggest": "Addition, Number Line",
      "If you Master then you can do": "Understand debt calculations, solve equations, and measure differences effectively.",
      "Category": "Numbers",
      "Mark": 1
    },
    {
      "Topic": "Fractions",
      "If you struggle, I suggest": "Multiplication, Division, Number Line",
      "If you Master then you can do": "Perform advanced calculations, understand proportions, and interpret statistical data.",
      "Category": "Numbers",
      "Mark": 2
    },
    {
      "Topic": "Multiplication",
      "If you struggle, I suggest": "Addition, Number Line",
      "If you Master then you can do": "Work with exponents, solve area and volume problems, and understand scaling.",
      "Category": "Numbers",
      "Mark": 2
    },
    {
      "Topic": "Division",
      "If you struggle, I suggest": "Subtraction, Multiplication, Number Line",
      "If you Master then you can do": "Solve division problems, understand ratios, and perform unit conversions.",
      "Category": "Numbers",
      "Mark": 2
    },
    {
      "Topic": "Simple Equations",
      "If you struggle, I suggest": "Addition, Subtraction, Multiplication, Division",
      "If you Master then you can do": "Solve unknown variable problems, build logic for programming, and model basic systems.",
      "Category": "Algebra",
      "Mark": 2
    },
    {
      "Topic": "Simultaneous Equations",
      "If you struggle, I suggest": "Simple Equations",
      "If you Master then you can do": "Analyze multi-variable systems and apply concepts in economics and engineering.",
      "Category": "Algebra",
      "Mark": 3
    },
    {
      "Topic": "Quadratic Equations",
      "If you struggle, I suggest": "Simple Equations, Simultaneous Equations",
      "If you Master then you can do": "Understand parabolas, calculate projectile motion, and optimize engineering designs.",
      "Category": "Algebra",
      "Mark": 3
    },
    {
      "Topic": "Perimeter",
      "If you struggle, I suggest": "Number Line",
      "If you Master then you can do": "Calculate boundaries of shapes, solve real-world measurement problems, and design layouts.",
      "Category": "Geometry",
      "Mark": 2
    },
    {
      "Topic": "Area",
      "If you struggle, I suggest": "Multiplication, Perimeter",
      "If you Master then you can do": "Solve surface problems, understand spatial geometry, and design structures.",
      "Category": "Geometry",
      "Mark": 3
    },
    {
      "Topic": "Volume",
      "If you struggle, I suggest": "Area",
      "If you Master then you can do": "Solve problems in 3D space, design containers, and work with fluid dynamics.",
      "Category": "Geometry",
      "Mark": 3
    },
    {
      "Topic": "Probability",
      "If you struggle, I suggest": "Fractions, Multiplication, Division",
      "If you Master then you can do": "Analyze events, solve risk management problems, and interpret statistical models.",
      "Category": "Statistics",
      "Mark": 4
    },
    {
      "Topic": "Statistics",
      "If you struggle, I suggest": "Fractions, Probability",
      "If you Master then you can do": "Understand data trends, analyze experiments, and perform market analysis.",
      "Category": "Statistics",
      "Mark": 4
    },
    {
      "Topic": "Linear Graphs",
      "If you struggle, I suggest": "Simple Equations",
      "If you Master then you can do": "Analyze trends, model real-world problems, and solve linear optimization tasks.",
      "Category": "Algebra",
      "Mark": 3
    },
    {
      "Topic": "Quadratic Graphs",
      "If you struggle, I suggest": "Quadratic Equations, Linear Graphs",
      "If you Master then you can do": "Understand curves, predict motion paths, and explore advanced mathematical models.",
      "Category": "Algebra",
      "Mark": 3
    },
    {
      "Topic": "Trigonometry",
      "If you struggle, I suggest": "Simple Equations, Geometry",
      "If you Master then you can do": "Analyze waves, understand rotation and angles, and model periodic phenomena.",
      "Category": "Trigonometry",
      "Mark": 4
    },
    {
      "Topic": "Calculus",
      "If you struggle, I suggest": "Simple Equations, Trigonometry",
      "If you Master then you can do": "Model changes, optimize processes, and explore advanced scientific theories.",
      "Category": "Calculus",
      "Mark": 4
    },
    {
      "Topic": "Sets",
      "If you struggle, I suggest": "Fractions, Addition",
      "If you Master then you can do": "Understand data grouping, solve logic problems, and analyze collections.",
      "Category": "Algebra",
      "Mark": 2
    },
    {
      "Topic": "Number Patterns",
      "If you struggle, I suggest": "Simple Equations, Fractions",
      "If you Master then you can do": "Solve sequence problems, model financial growth, and predict outcomes.",
      "Category": "Numbers",
      "Mark": 3
    },
    {
      "Topic": "Functions",
      "If you struggle, I suggest": "Quadratic Equations, Trigonometry",
      "If you Master then you can do": "Analyze input-output relationships, model processes, and predict trends.",
      "Category": "Algebra",
      "Mark": 4
    },
    {
      "Topic": "Logarithms",
      "If you struggle, I suggest": "Multiplication, Exponents",
      "If you Master then you can do": "Solve exponential decay problems, analyze scales, and model growth.",
      "Category": "Algebra",
      "Mark": 4
    }
]

# Expert System
class TutorExpertSystem(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendation = ""

    def categorize_marks(self, marks):
        """Categorizes marks based on the provided ranges."""
        marks = int(marks)  # Ensure marks are treated as integers
        if 1 <= marks <= 35:
            return 1
        elif 35 < marks <= 50:
            return 2
        elif 50 < marks <= 70:
            return 3
        elif 70 < marks <= 100:
            return 4
        else:
            return None  # Invalid marks

    @Rule(Fact(action="start_tutoring"), Fact(struggling=MATCH.topic))
    def recommend_prerequisite(self, topic):
        # Recommend topics based on difficulty level
        for knowledge in knowledge_data:
            if knowledge["Topic"] == topic:
                self.recommendation = f"To master {topic}, focus on these first: {knowledge['If you struggle, I suggest']}."
                return
        self.recommendation = f"Topic {topic} is not found in the knowledge base."

    @Rule(Fact(action="start_tutoring"), Fact(mastered=MATCH.mastered), Fact(marks=MATCH.marks))
    def recommend_based_on_marks(self, mastered, marks):
        # Categorize the marks
        mark_category = self.categorize_marks(marks)
        
        # If marks are below 35, focus on lower difficulty topics (category 1)
        if mark_category == 1:
            self.recommendation = f"Your marks are {marks}. You need to focus on topics from category 1 like basic addition, subtraction, etc."
            return

        # If marks are between 35-50, focus on category 2 topics
        elif mark_category == 2:
            self.recommendation = f"Your marks are {marks}. You should focus on topics like Fractions, Multiplication, Division, etc. (Category 2 topics)."
            return

        # If marks are between 50-70, focus on category 3 topics
        elif mark_category == 3:
            self.recommendation = f"Your marks are {marks}. It's time to dive into advanced topics like Quadratic Equations, Linear Graphs, etc."
            return
        
        # If marks are between 70-100, focus on category 4 topics
        elif mark_category == 4:
            self.recommendation = f"Your marks are {marks}. You're doing well! It's time to explore more advanced topics like Trigonometry, Calculus, etc."
            return

        self.recommendation = "Marks are outside the valid range (1-100)."

    @Rule(Fact(action="start_tutoring"), Fact(mastered=MATCH.mastered))
    def suggest_next_topics(self, mastered):
        mastered_list = mastered.split(", ")
        all_suggestions = []
        for knowledge in knowledge_data:
            if knowledge["Topic"] not in mastered_list:
                all_suggestions.append(knowledge["Topic"])

        if all_suggestions:
            self.recommendation += "\nNext topics to study: " + ", ".join(all_suggestions[:2])  # Suggest two next topics
        else:
            self.recommendation += "\nNo more topics to study. You've mastered all the topics!"

# GUI Application Update
class TutorExpertSystemApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tutor Expert System")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Widgets
        self.label_struggling = QLabel("Enter the topic you're struggling with:")
        self.input_struggling = QLineEdit()

        self.label_mastered = QLabel("Enter topics you've mastered (comma-separated):")
        self.input_mastered = QLineEdit()

        self.label_marks = QLabel("Enter your marks (1-100):")
        self.input_marks = QLineEdit()

        self.button_run = QPushButton("Get Recommendations")
        self.button_run.clicked.connect(self.get_recommendations)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # Add widgets to layout
        layout.addWidget(self.label_struggling)
        layout.addWidget(self.input_struggling)
        layout.addWidget(self.label_mastered)
        layout.addWidget(self.input_mastered)
        layout.addWidget(self.label_marks)
        layout.addWidget(self.input_marks)
        layout.addWidget(self.button_run)
        layout.addWidget(self.output)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_recommendations(self):
        struggling_topic = self.input_struggling.text().strip()
        mastered_topics = self.input_mastered.text().strip().split(',')
        marks = self.input_marks.text().strip()

        if not struggling_topic and not mastered_topics and not marks:
            self.output.setText("Please fill in at least one field.")
            return

        # Run the expert system
        engine = TutorExpertSystem()
        engine.reset()
        engine.declare(Fact(action="start_tutoring"))

        # Filter out already mastered topics
        completed_topics = [topic.strip() for topic in mastered_topics]  # clean up extra spaces
        remaining_topics = []

        # Filter subjects based on the entered marks
        mark_category = engine.categorize_marks(marks)
        for knowledge in knowledge_data:
            if mark_category and knowledge["Mark"] == mark_category:
                # If the topic is not already mastered, add it to remaining topics
                if knowledge["Topic"] not in completed_topics:
                    remaining_topics.append(knowledge)

        if not remaining_topics:
            self.output.setText("You have already mastered all topics.")
            return

        # Format the list of remaining topics
        remaining_topics_text = ""
        for topic in remaining_topics:
            remaining_topics_text += f"Topic: {topic['Topic']}\n"
            remaining_topics_text += f"  Suggestion: {topic['If you struggle, I suggest']}\n"
            remaining_topics_text += f"  Mastery Outcome: {topic['If you Master then you can do']}\n\n"

        # Display the result
        self.output.setText(f"Topics you need to focus on:\n\n{remaining_topics_text}")

if __name__ == "__main__":
    app = QApplication([])
    window = TutorExpertSystemApp()
    window.show()
    app.exec_()
