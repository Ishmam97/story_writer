
from crewai import Crew
from agents import CustomAgents
from tasks import SweTasks
from textwrap import dedent
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CustomCrew:
    def __init__(self, idea):
        self.idea = idea

    def save_output(self, folder, filename, content):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, filename), 'w') as file:
            file.write(content)

    def run(self, run_id):
        # Generate a unique subfolder for this crew run
        
        output_folder = os.path.join("outputs", run_id)

        agents = CustomAgents()
        tasks = SweTasks()

        # Instantiate custom agents
        story_writer = agents.story_writer()
        character_detailer = agents.character_detailer()
        director = agents.director()
        illustrator = agents.illustrator()
        # image_prompter = agents.image_propmpter()

        # Create tasks
        story_writer_task = tasks.write_story(story_writer, self.idea)
        character_detailer_task = tasks.describe_characters_task(character_detailer, story_writer_task)
        director_task = tasks.direct_movie(director, story_writer_task, character_detailer_task)
        illustrator_task = tasks.edit_movie(illustrator, director_task, character_detailer_task)
        # image_prompter_task = tasks.image_prompter(image_prompter, illustration_task=illustrator_task, character_description_task=character_detailer_task)
        # Define and run the crew
        crew = Crew(
            name="SWE Crew",
            agents=[story_writer, character_detailer, director, illustrator],
            tasks=[story_writer_task, character_detailer_task, director_task, illustrator_task],
        )

        results = crew.kickoff()

        print("\n\n########################")
        print("## Here is your character_detailer_task result:")
        print(illustrator_task.output)

        # Save each task's output
        self.save_output(output_folder, "story.txt", story_writer_task.output.exported_output)
        self.save_output(output_folder, "character_descriptions.json", character_detailer_task.output.exported_output)
        self.save_output(output_folder, "scene_descriptions.txt", director_task.output.exported_output)
        self.save_output(output_folder, "illustrations.txt", illustrator_task.output.exported_output)
        # self.save_output(output_folder, "image_prompts.txt", image_prompter_task.output.exported_output)

        return results


# Main function to run the custom crew
if __name__ == "__main__":
    print("## Welcome to SWE Crew")
    print("-------------------------------")
    feature = input(dedent("""Enter Story Idea: """))
    
    # Assuming CustomCrew is defined elsewhere
    custom_crew = CustomCrew(feature)
    run_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    result = custom_crew.run(run_id)
    
    
    print(result)