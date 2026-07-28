from crewai import Task, Crew, Process

from agents import coordinator_agent, explainer_agent, quiz_master_agent, evaluator_agent
from memory import SessionMemory
from prompts.coordinator import COORDINATOR_TASK_TEMPLATE
from prompts.explainer import EXPLAINER_TASK_TEMPLATE
from prompts.quiz_master import QUIZ_MASTER_TASK_TEMPLATE
from prompts.evaluator import EVALUATOR_TASK_TEMPLATE
from parsing import parse_coordinator_output, parse_quiz_output, format_student_answers

print("=" * 50)
print("  Welcome to Leo - your Multi-Agent AI Tutor")
print("=" * 50)

student_name = input("\nWhat's your name? ").strip() or "Student"
topic_request = input(f"Hi {student_name}! What would you like to learn today? ").strip()

session = SessionMemory(student_name=student_name, topic=topic_request)


# --- Coordinator: keep asking until the request is clear ---
while True:
    print(f"\n🧭 Coordinator is reviewing your request...")

    coordinator_task = Task(
        description=COORDINATOR_TASK_TEMPLATE.format(**session.as_dict()),
        expected_output="TOPIC/LEVEL/NOTES block or CLARIFICATION_NEEDED",
        agent=coordinator_agent,
    )
    coord_crew = Crew(agents=[coordinator_agent], tasks=[coordinator_task], process=Process.sequential, verbose=False)
    coord_result = coord_crew.kickoff()

    parsed = parse_coordinator_output(coord_result.raw)

    if parsed["clear"]:
        session.topic = parsed["topic"]
        session.student_level = parsed["level"]
        session.notes = parsed["notes"]
        print(f"✅ Got it — teaching you: {session.topic} ({session.student_level} level)")
        break
    else:
        print(f"\n🧭 Coordinator: {parsed['question']}")
        session.topic = input("Your answer: ").strip()


# --- Explainer ---
print(f"\n📖 Explainer is preparing your lesson on {session.topic}...")

explainer_task = Task(
    description=EXPLAINER_TASK_TEMPLATE.format(**session.as_dict()),
    expected_output="A clear explanation of the topic at the student's level",
    agent=explainer_agent,
)
explain_crew = Crew(agents=[explainer_agent], tasks=[explainer_task], process=Process.sequential, verbose=False)
explain_result = explain_crew.kickoff()

session.explanation = explain_result.raw

print("\n" + "=" * 50)
print("LESSON")
print("=" * 50)
print(session.explanation)

# --- Quiz Master ---
print(f"\n📝 Quiz Master is writing practice questions...")

quiz_task = Task(
    description=QUIZ_MASTER_TASK_TEMPLATE.format(**session.as_dict()),
    expected_output="Exactly 3 Q/ANSWER pairs in the specified format",
    agent=quiz_master_agent,
)
quiz_crew = Crew(agents=[quiz_master_agent], tasks=[quiz_task], process=Process.sequential, verbose=False)
quiz_result = quiz_crew.kickoff()

session.quiz_questions = quiz_result.raw
questions = parse_quiz_output(session.quiz_questions)

print("\n" + "=" * 50)
print("QUIZ TIME")
print("=" * 50)

student_answers = []
for i, q in enumerate(questions, 1):
    print(f"\nQ{i}: {q['question']}")
    answer = input("Your answer: ").strip()
    student_answers.append(answer)

session.student_answers = format_student_answers(questions, student_answers)

# --- Evaluator ---
print(f"\n🔍 Evaluator is grading your answers...")

evaluator_task = Task(
    description=EVALUATOR_TASK_TEMPLATE.format(**session.as_dict()),
    expected_output="Per-question grading, overall summary, and weak areas",
    agent=evaluator_agent,
)
eval_crew = Crew(agents=[evaluator_agent], tasks=[evaluator_task], process=Process.sequential, verbose=False)
eval_result = eval_crew.kickoff()

session.feedback = eval_result.raw

print("\n" + "=" * 50)
print("FEEDBACK")
print("=" * 50)
print(session.feedback)

print("\n" + "=" * 50)
print(f"Session complete! Great work, {session.student_name}.")
print("=" * 50)