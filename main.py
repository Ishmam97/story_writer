from crewai import Crew
from agents import CustomAgents
from tasks import SweTasks
from textwrap import dedent
import os
import uuid
from datetime import datetime

class CustomCrew:
    def __init__(self, idea):
        self.idea = idea

    def save_output(self, folder, filename, content):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, filename), 'w') as file:
            file.write(content)

    def run(self):
        # Generate a unique subfolder for this crew run
        run_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        output_folder = os.path.join("outputs", run_id)

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

        results = crew.kickoff()

        # Save each task's output
        self.save_output(output_folder, "story.txt", results[story_writer_task])
        self.save_output(output_folder, "character_descriptions.json", results[character_detailer_task])
        self.save_output(output_folder, "scene_descriptions.json", results[director_task])

        return results

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
