import streamlit as st
import uuid
from main import CustomCrew
import os
import json
st.title("Welcome to Story Writer!")

# User input for the idea
idea = st.text_area("Enter your story idea", "An adventure story in a mystical forest.")


# Run the agents
if st.button("Run"):
    run_id = str(uuid.uuid4())
    st.write(f"Run ID: {run_id}")
    
    crew = CustomCrew(idea)
    crew.run(run_id)

    # run_id = "20240714_010401_784dc77f"
    st.success("Agents have completed their tasks.")

    # Construct the absolute path to the output directory
    base_dir = os.getcwd()
    output_folder = os.path.join(base_dir, 'outputs', run_id)

    story_file = os.path.join(output_folder, 'story.txt')
    character_descriptions_file = os.path.join(output_folder, 'character_descriptions.txt')
    scene_descriptions_file = os.path.join(output_folder, 'scene_descriptions.txt')

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