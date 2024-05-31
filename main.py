from crewai import Crew
from agents import CustomAgents
from tasks import SweTasks
from textwrap import dedent

class CustomCrew:
    def __init__(self, idea):
        self.idea = idea

    def run(self):
        agents = CustomAgents()
        tasks = SweTasks()

        # Instantiate custom agents
        story_writer = agents.story_writer()
        character_detailer = agents.character_detailer()
        director = agents.director()

        # Create tasks
        story_writer_task = tasks.write_story(story_writer, self.idea)
        character_detailer_task = tasks.describe_characters_task(character_detailer, story_writer_task)
        director_task = tasks.direct_movie(director, story_writer_task, character_detailer_task)

        # Define and run the crew
        crew = Crew(
            name="SWE Crew",
            agents=[story_writer, character_detailer, director],
            tasks=[story_writer_task, character_detailer_task, director_task],
        )

        result = crew.kickoff()
        return result

# Main function to run the custom crew
if __name__ == "__main__":
    print("## Welcome to SWE Crew")
    print("-------------------------------")
    feature = input(dedent("""Enter Story Idea: """))
    
    custom_crew = CustomCrew(feature)
    result = custom_crew.run()
    print("\n\n########################")
    print("## Here is your custom crew run result:")
    print("########################\n")
    print(result)
