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
                 
                Include the following in your description answering in JSON format:
                - appearance: Physical appearance
                - attire: Clothing style
                - species: Creature type
                - extras: Any other details that make the character unique

                Your final answer must be the full character description in JSON format no other text before or after.
                """),
            agent=agent,
            expected_output="The full characters descriptions as a string no other text after.",
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
    
    def edit_movie(self, agent, story_task, script_task):
        return Task(
            description=dedent(f"""\
                
                ------------
                Story:
                {story_task.output}
                ------------
                Script:
                {script_task.output}
                ------------
                
                """),
            agent=agent,
            expected_output="The complete script with all sections covered.",
            context=[story_task, script_task]
        )
