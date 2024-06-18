# Description

The idea is to build a crew of video production with ability to direct videos, write scripts and character descriptions.
We generate a story using a text prompt. CrewAI Agents generated the story, character description and scene descriptions (illustrations). This is used to prompt stable diffusion to generate images while the story is used to generate audio. Finally the images and videos are put together manually to generate a video.

![Architecture](https://github.com/Ishmam97/story_writer/blob/master/NVIDIA_CONTEST.jpg?raw=true)

figure above shows the current architecture. We plan to experiment and refine this further.

## Install dependencies

1. ```
   poetry install --no-root
   ```
2. ```
   poetry shell
   ```
