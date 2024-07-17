import json
from openai import OpenAI
import requests
import base64
import os
from langchain_community.llms import Ollama
import time
import pickle
import torch
from diffusers import DiffusionPipeline

def read_file(filepath):
    with open(filepath, "r") as file:
        scenes = json.loads(file.read())
        return scenes

def print_scenes(scenes):
    for scene, description in scenes.items():
        print(f"Scene: {scene}")
        print(f"Setting: {description['Setting']}")
        print(f"Characters: {', '.join(description['Characters'])}")
        print(f"Dialogue:")
        for character, line in description['Dialogue'].items():
            print(f"    {character}: {line}")
        print("\n")

def generate_image_dalle(prompt):
    
    client = OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    print(image_url)

    # save image
    with open(f'{time.time()}_image.jpg', 'wb') as f:
        f.write(requests.get(image_url).content)
    
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

def generate_illustrations(filepath: str) -> list[str]:
    # file is a txt file [\n"scene1"\n"scene2"...] or it can be ["frame1","frame2"] parse the text file properly
    try:
        with open(filepath, "r") as file:
            scenes = json.load(file)
            frames = [scene["Setting"] for scene in scenes.values()]
            return frames
    except:
        pass
    with open(filepath, "r") as file:
        content = file.read()
        # remove the new line characters and the brackets
        content = content.replace("\n", "").replace("[", "").replace("]", "")
        # split the content by the quotation marks
        frames = content.split('"')[1::2]

    #if a frame in frames contains the word "frame", "Frame", "Scene 123", ":" replace with blank
    frames = [frame.replace("Frame", "").replace("frame", "").replace("Scene", "").replace(":", "") for frame in frames]
    # remove numbers
    frames = ["".join([i for i in frame if not i.isdigit()]).strip() for frame in frames]
    return frames

def query_illustrator_llama(scene: str, character_desc: str) -> str:
    llm = Ollama(model="llama3")
    prompt = f'''Generate a detailed and vivid description of the scene and charaters in the scene with 50 words or less:
    {scene}
    Characters: {character_desc}
    To generate an excellent image description, follow these guidelines:
    - Be highly specific and descriptive: Instead of "a cat", describe "a fluffy orange tabby cat sitting on a velvet cushion in a sunlit Victorian parlor" for every detail.
    - Use artistic terms to set the style: Incorporate words like "digital art", "cartoon", "artwork".
    - Mention the characters in the scene and the background/ambiance.
    - Include textures and colors: Add descriptions of textures (e.g., "smooth marble floor", "rough wooden table") and colors (e.g., "emerald green", "crimson red") to enrich the imagery.
    - Aim for clarity and conciseness: The final description should be highly descriptive yet clear, not exceeding 50 words.
    The final answer should only be the scene description and character description in 50 words or less.
    '''
    response = llm.invoke(prompt)
    return response

def generate_scene_prompts(scene_filepath, character_description):
    # to string the character descriptions
    character_description = json.dumps(character_description)   
    frames = generate_illustrations(scene_filepath)
    
    image_prompts = []
    for frame in frames:
        resp = query_illustrator_llama(frame, character_description)
        image_prompts.append(resp)

    return image_prompts

def generate_image_diffusion(model_name, prompts, negative_prompt, output_dir):
    pipe = DiffusionPipeline.from_pretrained(
    model_name, 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    )

    pipe.to('cuda')
    # to_string negative_prompt
    negative_prompt = json.dumps(negative_prompt)
    
    for idx, prompt in enumerate(prompts):
        print(f"Generating image fore: {prompt}")
        image = pipe(
            prompt,
            negative_prompt=negative_prompt,
            width=1024,
            height=1024,
            guidance_scale=7,
            num_inference_steps=10,
        ).images[0]

        image.save(f"{output_dir}/{idx}.png")

def generate_character_image(model_name, character_name, character_description, output_dir):
    pipe = DiffusionPipeline.from_pretrained(
    model_name, 
    torch_dtype=torch.float16, 
    use_safetensors=True, 
    )

    pipe.to('cuda')
    # to_string negative_prompt
    negative_prompt = ['nsfw, lowres, (bad), missing limbs, extra limbs']
    image = pipe(
        character_description,
        negative_prompt=negative_prompt,
        width=1024,
        height=1024,
        guidance_scale=7,
        num_inference_steps=10,
    ).images[0]
    
    # save and return output path
    image.save(f"{output_dir}/{character_name}.png")
    return f"{output_dir}/{character_name}.png"

def main():
    run_id = "a8581865-a5cf-46c8-b76e-e22cde68da51"
    output_dir = f'outputs/{run_id}/img'
    os.makedirs(output_dir, exist_ok=True)

    scene_filepath = f'outputs/{run_id}/scene_descriptions.txt'
    character_description = read_file(f'outputs/{run_id}/character_descriptions.txt')
    
    image_prompts = generate_scene_prompts(scene_filepath, character_description)

    with open(f'outputs/{run_id}/image_prompts.pkl', "wb") as f:
        pickle.dump(image_prompts, f)
    
    # with open("outputs/20240706_034332_6289cccf/image_prompts.pkl", "rb") as f:
    #     image_prompts = pickle.load(f)

    negative_prompts =['nsfw, lowres, (bad), missing limbs, extra limbs']
    prompt = ["1girl, souryuu asuka langley, neon genesis evangelion, solo, upper body, v, smile, looking at viewer, outdoors, night", "2boy, Luffy, Zoro, One Piece, duo, figh, v, smile, looking at viewer, outdoors, night"]
    generate_image_diffusion('cagliostrolab/animagine-xl-3.1', image_prompts, negative_prompts, output_dir)    
    

if __name__ == "__main__":
    main()
