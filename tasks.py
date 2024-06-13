from crewai import Task
from textwrap import dedent

class SweTasks:
    def write_story(self, agent, idea):
        return Task(
            description=dedent(f"""\
                Write a children's story with the following idea: 
                ------------
                {idea}
                It should be suitable for children under 13 years old and have a good moral lesson.\
                The story should not be too short and have engaging and meaningful dialogue.\

                The final answer must be the full story and nothing else.
                """),
            agent=agent,
            expected_output="Story written with engaging content and a good moral lesson."
        )

    def describe_characters_task(self, agent, story_task):
        return Task(
            description=dedent(f"""\
                Describe the characters in the following story:
                ------------
                {story_task.output}
                The characters can be described with rich details to make them more engaging and relatable.\
                You have the freedom to create fantasy or realistic characters.
                 
                Include the following in your description:
                - Physical appearance
                - Clothing style
                - Creature type
                Your final answer must be the full character description. In Json format and return only the Json object and only the JSON and no other text after.
                """),
            agent=agent,
            expected_output="The full characters descriptions in JSON format and only the JSON and no other text after.",
            context=[story_task]
        )

    def direct_movie(self, agent, story_task, descriptions_task):
        return Task(
            description=dedent(f"""\
                Create scenes for turning the story into a movie, do not deviate from the story and ensure all characters and the entire story is covered.\
                Story:
                ------------
                {story_task.output}
                ------------
                The final answer should be an array of JSON objects containing,
                - Scene description
                - Character or narrator dialogue in the scene
                Your answer should be in the following format:
                [{{
                    
                    "Scene_description": "Description of the envioronment, setting and summary of the scene, and characters in the scene",
                    "character_name": "dialogue of the character in the scene or narration from narrator if no character is speaking",
                }}]
                """),
            agent=agent,
            expected_output="The full scene descriptions in JSON format. only the JSON and no other text after.",
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
