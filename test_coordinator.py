from crewai import Task, Crew, Process

from agents import coordinator_agent
from memory import SessionMemory
from prompts.coordinator import COORDINATOR_TASK_TEMPLATE

session = SessionMemory(student_name="Rafi", topic="Explain binary search trees to me, I'm a CS student who knows basic data structures")

coordinator_task = Task(
    description=COORDINATOR_TASK_TEMPLATE.format(**session.as_dict()),
    expected_output="Either 'CLARIFICATION_NEEDED: ...' or a TOPIC/LEVEL/NOTES block",
    agent=coordinator_agent,
)

crew = Crew(
    agents=[coordinator_agent],
    tasks=[coordinator_task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n--- RAW OUTPUT ---")
    print(result.raw)