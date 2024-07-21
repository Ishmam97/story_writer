import streamlit as st
import uuid
from main import CustomCrew
import torch
import os
import json
from images import generate_character_image

def fix_brackets_in_character_descriptions(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    
    # Fix the JSON format by adding missing brackets
    try:
        # Attempt to load the JSON data
        json_data = json.loads(data)
    except json.JSONDecodeError:
        # If there is a JSON decode error, try to fix the brackets
        # Add missing opening and closing brackets
        if not data.startswith('['):
            data = '[' + data
        if not data.endswith(']'):
            data = data + ']'
        
        # Attempt to load the fixed JSON data
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to fix the JSON format: {e}")
    
    # Write the fixed JSON data back to the file
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

st.title("Welcome to Story Writer!")

# User input for the idea
idea = st.text_area("Enter your story idea", "An adventure story in a mystical forest.")
image_gen_model = "cagliostrolab/animagine-xl-3.1"

# Run the agents
if st.button("Run"):
    #run_id = str(uuid.uuid4())
    run_id = 'a8581865-a5cf-46c8-b76e-e22cde68da51'
    st.write(f"Run ID: {run_id}")
    
    # crew = CustomCrew(idea)
    # crew.run(run_id)
    torch.cuda.empty_cache()
    st.success("Agents have completed their tasks.")

    # Construct the absolute path to the output directory
    base_dir = os.getcwd()
    output_folder = os.path.join(base_dir, 'outputs', run_id)

    story_file = os.path.join(output_folder, 'story.txt')
    character_descriptions_file = os.path.join(output_folder, 'character_descriptions.txt')
    scene_descriptions_file = os.path.join(output_folder, 'scene_descriptions.txt')

    # Fix character descriptions file
    if os.path.exists(character_descriptions_file):
        fix_brackets_in_character_descriptions(character_descriptions_file)

    # Display the story file
    st.subheader("Story")
    if os.path.exists(story_file):
        with open(story_file, 'r') as file:
            story = file.read()
            st.write(story)
    else:
        st.error(f"Story file not found: {story_file}")

    # Display the character descriptions
    st.subheader("Character Descriptions")
    if os.path.exists(character_descriptions_file):
        with open(character_descriptions_file, 'r') as file:
            character_descriptions = json.load(file)
            for character in character_descriptions:
                for name, details in character.items():
                    st.write(f"**Name**: {name}")
                    st.write(f"**Species**: {details['species']}")
                    st.write(f"**Description**: {details['description']}")
                    st.write("---")
    else:
        st.error(f"Character Descriptions file not found: {character_descriptions_file}")

    # Display the scene descriptions
    st.subheader("Scene Descriptions")
    if os.path.exists(scene_descriptions_file):
        with open(scene_descriptions_file, 'r') as file:
            scene_descriptions = json.load(file)
            for scene, details in scene_descriptions.items():
                st.write(f"**{scene}**")
                st.write(f"**Setting**: {details['Setting']}")
                st.write("**Characters**: " + ", ".join(details['Characters']))
                st.write("**Dialogue**:")
                for character, dialogue in details['Dialogue'].items():
                    st.write(f"  **{character}**: {dialogue}")
                st.write("**Sound**: " + details.get('Sound', ''))
                st.write("---")
    else:
        st.error(f"Scene Descriptions file not found: {scene_descriptions_file}")
