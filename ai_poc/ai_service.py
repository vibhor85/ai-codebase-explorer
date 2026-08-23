from dotenv import load_dotenv
from langchain.agents import create_agent
from langfuse.langchain import CallbackHandler
from langchain_groq import ChatGroq
from ai_poc.tools.get_repository_files import get_multiple_files
from ai_poc.prompts.dependency_analysis import build_dependency_analysis_prompt


load_dotenv()
langfuse_handler = CallbackHandler()


def answer(question: str, relationships: list[dict[str, str]]):

    # model = init_chat_model(
    #     "gemini-3.6-flash",
    #     model_provider="google_genai",
    # )
    model = ChatGroq(
        model="openai/gpt-oss-120b",
    )

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
