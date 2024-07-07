from crewai import Agent
from textwrap import dedent
from langchain.chat_models import ChatOpenAI

class CustomAgents():
    LLAMA3 = ChatOpenAI(
        model="llama3",
        base_url="http://localhost:11434/v1",
        api_key="NA"  # Make sure this is correct
    )

    mistral = ChatOpenAI(
        model="mistral-openorca",
        base_url="http://localhost:11434/v1",
        api_key="NA"  # Make sure this is correct
    )

    gpt35 = ChatOpenAI(
        temperature = 0.9,
        model_name = "gpt-3.5-turbo-0125",
    )
    mainModel = LLAMA3

    def story_writer(self):
        return Agent(
            role="story_writer",
            backstory=dedent("""
                You are a popular children's story writer known for writing interesting children's stories that have good moral lessons.
            """),
            goal=dedent("""
                Ensure the story is well written and is friendly for children under 13. The story should have a good moral lesson and not be too short.
                You can add a little fantasy to the story and use example plot points from popular stories.
            """),
            llm = self.mainModel,
            # Add tools if necessary, e.g., tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,

        )

    def character_detailer(self):
        return Agent(
            role='character_detailer',
            backstory=dedent("""
                A detail-oriented writer who excels in character development.
            """),
            goal=dedent("""
                Describe the characters in the story with rich details.
            """),
            llm = self.mainModel,
            # Add tools if necessary, e.g., tools=[tool_1, tool_2],
            verbose=True,
            allow_delegation=False,
        )

    def director(self):
        return Agent(
            role='Director',
            backstory=dedent("""
                A seasoned director with experience in describing vivid scenes and riveting dialogue
            """),
            goal=dedent("""
                Create engaging scenes and dialogue to direct a short movie from the story.
            """),
            llm = self.gpt35,
           # Add tools if necessary, e.g., tools=[tool_1, tool_2],
            verbose=True,
            allow_delegation=False,
        )

    def illustrator(self):
        return Agent(
            role='editor',
            backstory=dedent("""
                An editor with a sharp eye for detail and ensuring completeness of content.
            """),
            goal=dedent("""
                Ensure the script covers the entire story, filling in any missing parts if necessary.
            """),
            llm = self.gpt35,
            verbose=True,
            allow_delegation=True,
        )