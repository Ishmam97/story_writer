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

                The final answer must be the full story and no other text before or after.
                """),
            agent=agent,
            expected_output="Story written with engaging content and a good moral lesson and no other text before or after."
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
                Your final answer must be the full character description in a paragraph, each character separated by a new line, no other text after.
                """),
            agent=agent,
            expected_output="The full characters descriptions as a string no other text after.",
            context=[story_task]
        )

    def direct_movie(self, agent, story_task, descriptions_task):
        return Task(
            description=dedent(f"""\
                Create descriptions for illustrating the following story into scenes\
                Only mention the species or description of the character and not the name. such as "orange cat" instead of "Garfield" for ALL ILLUSTRATIONS and CHARACTERS.
                Story:
                ------------
                {story_task.output}
                ------------
                The final answer should be an array strings containing only a short description of each illustration. The story should be broken down into meaningful chunks for the illustration.
                The description should contain the description of the scenery and character.
                Your answer should be in the following format:
                ["a one sentence description of scene 1", "scene 2 description" ...]
                there should be no extra text or note before or after the array.
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
