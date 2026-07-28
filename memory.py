from dataclasses import dataclass, field

@dataclass
class SessionMemory:
    student_name: str = "Student"
    topic: str = ""
    student_level: str = "beginner"
    notes: str = ""
    explanation: str = ""
    quiz_questions: str = ""
    student_answers: str = ""
    feedback: str = ""
    weak_areas: str = ""
    history: list = field(default_factory=list)

    def log(self, agent_name: str, output: str):
        self.history.append({"agent": agent_name, "output": output})

    def as_dict(self):
        return {
            "student_name": self.student_name,
            "topic": self.topic,
            "student_level": self.student_level,
            "notes": self.notes,
            "explanation": self.explanation,
            "quiz_questions": self.quiz_questions,
            "student_answers": self.student_answers,
            "feedback": self.feedback,
            "weak_areas": self.weak_areas,
        }

    