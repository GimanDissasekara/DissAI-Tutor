from pyknow import *

class StudentKnowledge(Fact):
    """Facts about a student's knowledge."""
    pass

class TutoringExpertSystem(KnowledgeEngine):
    @Rule(StudentKnowledge(topic="fractions", struggling=True))
    def suggest_fractions_help(self):
        print("Student is struggling with fractions. Suggest reviewing basic division first.")

    @Rule(StudentKnowledge(topic="calculus", struggling=True))
    def suggest_calculus_help(self):
        print("Student is struggling with calculus. Recommend algebra refresher and practice.")

engine = TutoringExpertSystem()
engine.reset()

# Add facts
engine.declare(StudentKnowledge(topic="fractions", struggling=True))
engine.declare(StudentKnowledge(topic="calculus", struggling=True))

# Run the system
engine.run()
