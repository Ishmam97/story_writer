
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
        # editor = agents.editor()

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

        print("\n\n########################")
        print("## Here is your character_detailer_task result:")
        print(character_detailer_task.output.exported_output)

        # Save each task's output
        self.save_output(output_folder, "story.txt", story_writer_task.output.exported_output)
        self.save_output(output_folder, "character_descriptions.json", character_detailer_task.output.exported_output)
        self.save_output(output_folder, "scene_descriptions.txt", director_task.output.exported_output)


        return results


def read_array_from_file(file_path):
    # remove everything after closing bracket "]" and return as eval array
    with open(file_path, "r") as f:
        content = f.read()
        content = content.split("]")[0] + "]"
        return eval(content)

def payload_generator(scene):
    payload = {
        "text_prompts": [
            {
                "text": scene,
                "weight": 1
            }
        ],
        "seed": 12,
        "sampler": "K_EULER_ANCESTRAL",
        "steps": 4
    }

    return payload


def generate_images_from_scene_descriptions(run_id, scene_descriptions):
    # Generate images from a list of scene descriptions
    invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/sdxl-turbo"

    # Ensure the API key is set
    api_key = os.getenv("SDXL_API_KEY")
    if not api_key:
        raise ValueError("SDXL_API_KEY environment variable is not set")

    headers = {
        "Authorization": f'Bearer {api_key}',
        "Accept": "application/json",
    }

    for idx, scene in enumerate(scene_descriptions):
        payload = payload_generator(scene)
        response = requests.post(invoke_url, headers=headers, json=payload)

        # Check if the response status code indicates success
        if response.status_code == 401:
            raise Exception("Unauthorized: Check your API key and ensure it is correct")

        response.raise_for_status()
        response_body = response.json()
        
        # Decode the base64 image and save it as idx.jpeg
        image_data = base64.b64decode(response_body['artifacts'][0]['base64'])
        os.makedirs(f"outputs/{run_id}/img", exist_ok=True)
        with open(f"outputs/{run_id}/img/{idx}.jpeg", "wb") as f:
            f.write(image_data)
        
        print(f"Image saved for index: {idx}")

# Main function to run the custom crew
if __name__ == "__main__":
    print("## Welcome to SWE Crew")
    print("-------------------------------")
    feature = input(dedent("""Enter Story Idea: """))
    
    # Assuming CustomCrew is defined elsewhere
    custom_crew = CustomCrew(feature)
    run_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    result = custom_crew.run(run_id)
    
    print("\n\n########################")
    print("## Here is your custom crew run result:")
    print("########################\n")
    print(result)
    # Read scene_descriptions.txt file from outputs/{run_id}/scene_descriptions.txt
    # scene_descriptions = read_array_from_file(f"outputs/{run_id}/scene_descriptions.txt")

#     # Generate images from scene descriptions
#     generate_images_from_scene_descriptions(run_id, scene_descriptions)

#     print("Transcribing Audio...")
# # sleep for 5 seconds to simulate audio transcription
#     time.sleep(5)
#     print("Audio Transcription Complete!")
    
#     print("Video Compilation...")
#     time.sleep(5)
#     print("Video Compilation Complete!")