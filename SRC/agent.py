import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4",
    temperature=0.7
)


class WaterIntakeAgent:

    def __init__(self):
        self.history = []

    def analyze_intake(self, intake_ml):

        prompt = f"""
        You are a hydration assistant.
        The user consumed {intake_ml} ml of water today.

        Provide a general hydration status and suggest whether
        they may need to drink more water.
        """

        response = llm.invoke(
            [HumanMessage(content=prompt)]
        )

        return response.content


if __name__ == "__main__":

    agent = WaterIntakeAgent()

    intake = 1500

    analysis = agent.analyze_intake(intake)

    print(f"Hydration Analysis: {analysis}")