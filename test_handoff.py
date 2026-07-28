from crewai import Task, Crew, Process

from agents import coordinator_agent, explainer_agent, quiz_master_agent, evaluator_agent
from memory import SessionMemory
from prompts.coordinator import COORDINATOR_TASK_TEMPLATE
from prompts.explainer import EXPLAINER_TASK_TEMPLATE
from prompts.evaluator import EVALUATOR_TASK_TEMPLATE
from parsing import parse_coordinator_output, parse_quiz_output, format_student_answers
from prompts.quiz_master import QUIZ_MASTER_TASK_TEMPLATE


session = SessionMemory(
    student_name="Rafi",
    topic="Explain binary search trees to me, I'm a CS student who knows basic data structures"
)

# --- Step 1: Coordinator runs ---
coordinator_task = Task(
    description=COORDINATOR_TASK_TEMPLATE.format(**session.as_dict()),
    expected_output="TOPIC/LEVEL/NOTES block or CLARIFICATION_NEEDED",
    agent=coordinator_agent,
)
coord_crew = Crew(agents=[coordinator_agent], tasks=[coordinator_task], process=Process.sequential, verbose=True)
coord_result = coord_crew.kickoff()

# --- The handoff: parse Coordinator's text output, write it into memory ---
parsed = parse_coordinator_output(coord_result.raw)

if not parsed["clear"]:
    print("Coordinator needs clarification:", parsed["question"])
    exit()

session.topic = parsed["topic"]
session.student_level = parsed["level"]
session.notes = parsed["notes"]

print("\n--- Memory after Coordinator handoff ---")
print(session.as_dict())

# --- Step 2: Explainer runs, using the topic/level/notes handed off from the Coordinator ---
explainer_task = Task(
    description=EXPLAINER_TASK_TEMPLATE.format(**session.as_dict()),
    expected_output="A clear explanation of the topic at the student's level",
    agent=explainer_agent,
)
explain_crew = Crew(agents=[explainer_agent], tasks=[explainer_task], process=Process.sequential, verbose=True)
explain_result = explain_crew.kickoff()

session.explanation = explain_result.raw

print("\n=== FINAL EXPLANATION ===")
print(session.explanation)

# --- Step 3: Quiz Master runs, using the Explainer's output ---
quiz_task = Task(
    description=QUIZ_MASTER_TASK_TEMPLATE.format(**session.as_dict()),
    expected_output="Exactly 3 Q/ANSWER pairs in the specified format",
    agent=quiz_master_agent,
)
quiz_crew = Crew(agents=[quiz_master_agent], tasks=[quiz_task], process=Process.sequential, verbose=True)
quiz_result = quiz_crew.kickoff()

session.quiz_questions = quiz_result.raw
questions = parse_quiz_output(session.quiz_questions)

print("\n=== QUIZ QUESTIONS (student view - no answers) ===")
for i, q in enumerate(questions, 1):
    print(f"{i}. {q['question']}")

# --- Simulate the student answering (one right, one wrong, one partial) ---
simulated_answers = [
    "O(log n)",
    "It would go to the right of 30",  # deliberately wrong, to test grading
    "Fast search and insertion",
]
session.student_answers = format_student_answers(questions, simulated_answers)

# --- Step 4: Evaluator runs ---
evaluator_task = Task(
    description=EVALUATOR_TASK_TEMPLATE.format(**session.as_dict()),
    expected_output="Per-question grading, overall summary, and weak areas",
    agent=evaluator_agent,
)
eval_crew = Crew(agents=[evaluator_agent], tasks=[evaluator_task], process=Process.sequential, verbose=True)
eval_result = eval_crew.kickoff()

session.feedback = eval_result.raw
print("\n=== EVALUATOR FEEDBACK ===")
print(session.feedback)