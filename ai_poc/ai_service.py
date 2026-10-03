from dotenv import load_dotenv
from langchain.agents import create_agent
from langfuse.langchain import CallbackHandler
from langchain_groq import ChatGroq

from ai_poc.prompts.context_selector import build_context_selection_prompt
from ai_poc.tools.get_repository_files import get_multiple_files
from ai_poc.prompts.dependency_analysis import build_dependency_analysis_prompt
from common.models import ContextSelection, RepositoryKnowledge


load_dotenv()
langfuse_handler = CallbackHandler()


def get_model():
    return ChatGroq(
        model="openai/gpt-oss-120b",
    )


def select_context(
    question: str,
    repository: RepositoryKnowledge,
):
    model = get_model()

    prompt = build_context_selection_prompt(
        question,
        repository,
    )

    return model.invoke(prompt)


def answer(question: str, relationships: RepositoryKnowledge):

    model = get_model()

    agent = create_agent(
        model=model,
        tools=[get_multiple_files],
    )

    prompt = build_dependency_analysis_prompt(question, relationships)

    response = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        config={
            "callbacks": [langfuse_handler]
        }
    )

    return response["messages"][-1].content
