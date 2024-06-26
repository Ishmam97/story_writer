from crewai import Agent
from langchain_community.llms import OpenAI  # Ensure this is the correct import
from langchain_openai import ChatOpenAI  # Ensure this is the correct import
from textwrap import dedent

class CustomAgents:
    def __init__(self):
        # Ensure LLAMA3 is available and properly configured
        self.LLAMA3 = ChatOpenAI(
            model="llama3",
            base_url="http://localhost:11434/v1",
            api_key="NA"  # Make sure this is correct
        )

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
            # Add tools if necessary, e.g., tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.LLAMA3,
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
            # Add tools if necessary, e.g., tools=[tool_1, tool_2],
            verbose=True,
            llm=self.LLAMA3,
            allow_delegation=False,
        )

    def director(self):
        return Agent(
            role='illustrator',
            backstory=dedent("""
                An illustrator with who comes up with vivid descriptions for scenes.
            """),
            goal=dedent("""
                Create vivid illustration descriptions for directing a motion picture film.
            """),
            # Add tools if necessary, e.g., tools=[tool_1, tool_2],
            verbose=True,
            llm=self.LLAMA3,
            allow_delegation=False,
        )

    def editor(self):
        return Agent(
            role='editor',
            backstory=dedent("""
                An editor with a sharp eye for detail and ensuring completeness of content.
            """),
            goal=dedent("""
                Ensure the script covers the entire story, filling in any missing parts if necessary.
            """),
            verbose=True,
            llm=self.LLAMA3,
            allow_delegation=False,
        )