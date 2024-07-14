from crewai import Task
from textwrap import dedent

class SweTasks:
    def write_story(self, agent, idea):
        return Task(
            description=dedent(f"""\
                Write a children's story (1000-2000 words) with the following idea: 
                ------------
                {idea}
                The final answer must be the full story and no other text before or after.
                It should be suitable for children under 13 years old and have a good moral lesson.\
                The story should not be too short and have engaging and meaningful dialogue.\

                """),
            agent=agent,
            expected_output="Only the story written with engaging content and a good moral lesson and no other text before or after."
        )

    def describe_characters_task(self, agent, story_task):
        return Task(
            description=dedent(f"""\
                Describe the characters in the following story:
                ------------
                {story_task.output}
                The characters can be described with rich details to make them more engaging and relatable.\
                You have the freedom to create fantasy or realistic characters.
                Describe each character in 2-3 sentences.
                Include the following in your description answering:
                - species
                - detailed physical description and clothing description.

                The output format should be:
                [{{
                    "character_name": {{
                        "species": "species",
                        "description": "detailed description"
                    }}
                }}]

                Your final answer must be the full character description in JSON with no other text before or after.
                """),
            agent=agent,
            expected_output="The full characters descriptions as a JSON no other text after.",
            context=[story_task]
        )

    def direct_movie(self, agent, story_task, descriptions_task):
        return Task(
            description=dedent(f"""\
                Create a well detailed scene description with discriptive scene settings and interesting dialogue.
                Only mention the species or description of the character and not the name. such as "orange cat" instead of "Garfield" for ALL ILLUSTRATIONS and CHARACTERS.
                Story:
                ------------
                {story_task.output}
                ------------
                The dialogue should fit the story and the scenes should cover the full story. Include Narrator dialogues if no character is speaking or music/sound effects.
                The final answer should be in JSON format in the following format and contents:
                {{
                    "Scene 1":{{
                        "Setting": "Description of the scene",
                        "Characters": ["Character 1", "Character 2"],
                        "Dialogue": {{
                            "Character 1": "Dialogue of character 1",
                            "Character 2": "Dialogue of character 2",
                            "Narrator": "Narrator dialogue",
                            "Sound": "Sound effect or music"
                        }}
                    }}
                }}
                """),
            agent=agent,
            expected_output="The full scene descriptions in an array of strings and no other text after.",
            context=[story_task, descriptions_task]
        )
    
    def edit_movie(self, agent, script_task, charcter_description_task):
        return Task(
            description=dedent(f"""\
                From the character descriptions and the script, create descriptions for 6 frames with one sentence descriptions for a motion picture.
                ------------
                Character Descriptions:
                {charcter_description_task.output}
                --------------
                Script:
                {script_task.output}
                ------------

                output should be an array of strings with atleast 15 frame description.
                The output should be an array only with frame descriptions, no other text before or after.
                
                """),
            agent=agent,
            expected_output="The complete script with all sections covered.",
            context=[script_task, charcter_description_task]
        )
    
    def image_prompter(self, agent, illustration_task, character_description_task):
        return Task(
            description=dedent(f"""\
                               
                Generate image prompts for each scene description and you can refer to character descriptions.:
                
                Scene descriptions:
                ------------
                {illustration_task.output}
                ------------


                Be specific and descriptive: Instead of "a cat", try "a fluffy orange tabby cat sitting on a velvet cushion in a sunlit Victorian parlor" for EVERY PROMPT.
                Use artistic terms: Incorporate words like "digital art", "oil painting", "photorealistic", or "watercolor" to influence the style.
                Specify lighting and mood: Words like "soft morning light", "neon-lit", or "moody twilight" can dramatically affect the atmosphere.
                The final answer should be prompts for images in the form of an array of strings.
                """),
            agent=agent,
            context=[illustration_task, character_description_task],
            expected_output="The image generated from the prompt."
        )
