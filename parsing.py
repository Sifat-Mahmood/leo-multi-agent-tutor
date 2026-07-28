def parse_coordinator_output(raw_output: str) -> dict:
    if raw_output.strip().startswith("CLARIFICATION_NEEDED"):
        return {"clear": False, "question": raw_output.split(":", 1)[1].strip()}

    result = {"clear": True, "topic": "", "level": "", "notes": ""}
    for line in raw_output.strip().splitlines():
        if line.startswith("TOPIC:"):
            result["topic"] = line.replace("TOPIC:", "").strip()
        elif line.startswith("LEVEL:"):
            result["level"] = line.replace("LEVEL:", "").strip()
        elif line.startswith("NOTES:"):
            result["notes"] = line.replace("NOTES:", "").strip()
    return result

import re

def parse_quiz_output(raw_output: str) -> list:
    questions = {}
    for line in raw_output.strip().splitlines():
        q_match = re.match(r"Q(\d+):\s*(.+)", line)
        a_match = re.match(r"ANSWER(\d+):\s*(.+)", line)
        if q_match:
            num = int(q_match.group(1))
            questions.setdefault(num, {})["question"] = q_match.group(2).strip()
        elif a_match:
            num = int(a_match.group(1))
            questions.setdefault(num, {})["answer"] = a_match.group(2).strip()

    return [questions[num] for num in sorted(questions.keys())]

def format_student_answers(questions: list, student_answers: list) -> str:
    lines = []
    for i, (q, ans) in enumerate(zip(questions, student_answers), 1):
        lines.append(f"Q{i}: {q['question']}\nStudent answered: {ans}")
    return "\n\n".join(lines)