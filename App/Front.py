import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, 
                             QLineEdit, QTextEdit, QWidget, QLabel, QMessageBox, QCompleter)
import pandas as pd
from fuzzywuzzy import process  # For fuzzy matching
import Back 

class LearningApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DissAi - Personalized Mathematics Learning System")
        self.setGeometry(100, 100, 600, 700)  

        # Load topics from the Excel file
        file_path = 'Data.xlsx'
        try:
            sheet_data = pd.read_excel(file_path)
            self.topics = sheet_data['Topic'].dropna().unique().tolist()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load topics: {str(e)}")
            self.topics = []

        self.layout = QVBoxLayout()

        # Struggling Subject Input
        self.struggling_label = QLabel("Your Struggling Subject:", self)
        self.struggling_field = QLineEdit(self)
        self.struggling_field.setPlaceholderText("Type struggling subject...")
        self.struggling_completer = QCompleter(self.topics, self)
        self.struggling_completer.setCaseSensitivity(False)
        self.struggling_field.setCompleter(self.struggling_completer)

        # Mastered Subject Input
        self.mastered_label = QLabel("Your Mastered Subject:", self)
        self.mastered_field = QLineEdit(self)
        self.mastered_field.setPlaceholderText("Type mastered subject...")
        self.mastered_completer = QCompleter(self.topics, self)
        self.mastered_completer.setCaseSensitivity(False)
        self.mastered_field.setCompleter(self.mastered_completer)

        # Marks Input
        self.marks_label = QLabel("Enter your marks (0-100):", self)
        self.marks_field = QLineEdit(self)
        self.marks_field.setPlaceholderText("Type your marks (0-100)...")

        # Submit Button
        self.submit_btn = QPushButton("Get Learning Recommendations", self)
        self.submit_btn.clicked.connect(self.get_suggestions)

        # Output area
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            font-family: Arial, sans-serif; 
            font-size: 14px; 
            color: #333; 
            background-color: #f9f9f9;
            padding: 10px;
        """)

        # Add widgets to layout
        self.layout.addWidget(self.struggling_label)
        self.layout.addWidget(self.struggling_field)
        self.layout.addWidget(self.mastered_label)
        self.layout.addWidget(self.mastered_field)
        self.layout.addWidget(self.marks_label)
        self.layout.addWidget(self.marks_field)
        self.layout.addWidget(self.submit_btn)
        self.layout.addWidget(self.output_area)

        # Set the layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def fuzzy_match(self, input_text):
        """
        Matches the user input with the closest valid topic using fuzzy matching.
        """
        best_match, score = process.extractOne(input_text, self.topics)
        if score >= 75:  # Threshold for considering a match
            return best_match
        return None

    def get_suggestions(self):
        # Get input values
        struggling = self.struggling_field.text().strip()
        mastered = self.mastered_field.text().strip()
        marks_text = self.marks_field.text().strip()

        # Fuzzy match the struggling and mastered subjects
        corrected_struggling = self.fuzzy_match(struggling)
        corrected_mastered = self.fuzzy_match(mastered)

        if not corrected_struggling:
            QMessageBox.warning(self, "Invalid Input", f"'{struggling}' is not a recognized subject.")
            return
        if not corrected_mastered:
            QMessageBox.warning(self, "Invalid Input", f"'{mastered}' is not a recognized subject.")
            return

        # Validate marks
        try:
            marks = int(marks_text)
            if marks < 0 or marks > 100:
                raise ValueError("Marks must be between 0 and 100")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid mark between 0 and 100.")
            return

        # Get recommendations
        recommendations, explanations, alternative_solutions = Back.get_recommendations(corrected_struggling, corrected_mastered, marks)

        # Format output
        output_text = """
        <div style='font-family: Arial, sans-serif; color: #333;'>
        <h2 style='color: #2c3e50;'>📚 Personalized Learning Recommendations</h2>
        
        <h3 style='color: #34495e;'>🎯 Suggestions:</h3>
        <ul>
        {}
        </ul>
        
        <h3 style='color: #34495e;'>💡 Explanations:</h3>
        <p>{}</p>
        
        <h3 style='color: #34495e;'>🔍 Alternative Solutions:</h3>
        <ul>
        {}
        </ul>
        </div>
        """.format(
            ''.join(f"<li>{rec}</li>" for rec in recommendations),
            explanations,
            ''.join(f"<li>{sol}</li>" for sol in alternative_solutions)
        )

        # Display recommendations
        self.output_area.setHtml(output_text)

def main():
    app = QApplication(sys.argv)
    window = LearningApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
