from crewai import Task
from textwrap import dedent

class SweTasks:
    def write_story(self, agent, idea):
        return Task(
            description=dedent(f"""\
                Write a children's story with the following idea: 
                ------------
                {idea}
                The story should be engaging and have a good moral lesson.\
                It should be suitable for children under 13 years old and have a good moral lesson.\
                The story should not be too short.
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
                - Personality traits
                - Clothing style

                Your final answer must be the full character description.
                It should be in JSON format with the character name as the key and the description as the value.
                """),
            agent=agent,
            expected_output="The full characters descriptions in JSON format.",
            context=[story_task]
        )

    def direct_movie(self, agent, story_task, descriptions_task):
        return Task(
            description=dedent(f"""\
                Create scenes for a short movie based on the following story, sectioning the\
                scenes to ensure the scenes capture the parts of the plot development properly. The story is as follows:
                ------------
                {story_task.output}
                -------------
                and the character descriptions:
                ------------
                {descriptions_task.output}
                ------------
                The scenes should be vivid and engaging, and should be suitable for a movie.\
                Include the following in your description:
                - Scene setting (location, time of day, weather)
                - Character actions and interactions
                - Dialogue (or narration if needed)
                - Character emotions and expressions and movements
                - Camera angles and movements

                Your final answer must be the full scene descriptions and scene numbers in JSON format.
                """),
            agent=agent,
            expected_output="The full scene descriptions in JSON format.",
            context=[story_task, descriptions_task]
        )

    def testing_task(self, agent, code):
        return Task(
            description=dedent(f"""\
                You are writing tests for the React component for the following code:
                Code to test:
                ------------
                {code}

                Include tests for the following:
                - Test the component renders correctly
                - Test the component renders the correct data
                - Test the component handles user input correctly
                - Test the component handles errors correctly
                
                Your final answer must be the full testing code, only the test code and nothing else.
                """),
            agent=agent,
            expected_output="The complete test code for the React component."
        )
