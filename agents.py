import os
from dotenv import load_dotenv

from prompts.explainer import EXPLAINER_BACKSTORY
from prompts.quiz_master import QUIZ_MASTER_BACKSTORY
from prompts.evaluator import EVALUATOR_BACKSTORY

load_dotenv()

# Same Groq/litellm caching bug fix from your last project
import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crewai import Agent, LLM
from prompts.coordinator import COORDINATOR_BACKSTORY

groq_llm = LLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

coordinator_agent = Agent(
    role="Session Coordinator",
    goal="Understand the student's request and route it clearly, or flag when it's unclear.",
    backstory=COORDINATOR_BACKSTORY,
    llm=groq_llm,
    verbose=True,
    max_iter=3,
)

explainer_agent = Agent(
    role="Concept Explainer",
    goal="Teach the given topic clearly, matched to the student's level.",
    backstory=EXPLAINER_BACKSTORY,
    llm=groq_llm,
    verbose=True,
    max_iter=3,
)

quiz_master_agent = Agent(
    role="Quiz Master",
    goal="Write focused practice questions based on what the Explainer just taught.",
    backstory=QUIZ_MASTER_BACKSTORY,
    llm=groq_llm,
    verbose=True,
    max_iter=3,
)

evaluator_agent = Agent(
    role="Answer Evaluator",
    goal="Fairly grade the student's quiz answers and give constructive feedback.",
    backstory=EVALUATOR_BACKSTORY,
    llm=groq_llm,
    verbose=True,
    max_iter=3,
)