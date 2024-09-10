import json
import requests
from crewai_tools import BaseTool, YoutubeVideoSearchTool
from crewai import Agent, Task, Crew
from pydantic import BaseModel, PrivateAttr
from transformers import pipeline 
from PIL import Image  
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_BASE'] = 'http://127.0.0.1:11434/v1'
os.environ['OPENAI_MODEL_NAME'] = 'mistral:latest'
os.environ['OPENAI_API_KEY'] = 'NA'

from langchain_openai import ChatOpenAI
llm  = ChatOpenAI(
    base_url = 'http://localhost:11434/v1',
    model='mistral:latest',
    api_key='NA',)


class MyCustomTool(BaseTool):
    name: str = "Internet Search Tool"
    description: str = "This tool searches the 3 -4 times on internet for any user query and provides a summary."

    def _run(self, topic: str)  -> str:
        url = "https://api-ares.traversaal.ai/live/predict"
        payload = { "query": [topic] }
        headers = {
            "x-api-key":  os.getenv('ARES_API_KEY'),  # Replace with your actual ARES API key
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return json.dumps(data, indent=2)  # Adjust formatting as needed
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"

# Define tools
int_tool = MyCustomTool()


from tools_ import int_tool,yt_tool,image_caption_tool,rag_tool
from crewai import Agent, Task, Crew


class ImageCaptionTool(BaseTool):
    name: str = "Image Caption Tool"
    description: str = "This tool generates text descriptions of an image."

    # Use PrivateAttr to declare attributes that should not be part of Pydantic's validation
    _pipe: pipeline = PrivateAttr()

    def __init__(self):
        super().__init__()
        "microsoft/dit-base-finetuned-coco"
        #Salesforce/blip-image-captioning-base
        self._pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

    def _run(self, image_url: str) -> str:
        image_folder = 'image'  
        image_files = os.listdir(image_folder)
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
        images = [file for file in image_files if file.lower().endswith(tuple(image_extensions))]
        if len(images) == 1:
            image_path = os.path.join(image_folder, images[0])
            # image = Image.open(image_path)
        image = Image.open(image_path)

       
        result = self._pipe(image)

       
        caption = result[0]['generated_text']

        return caption
image_caption_tool = ImageCaptionTool()


image_agent = Agent(
    role='Image Processing Specialist',
    goal='Perform image caption generation from provided image.',
    backstory=(
        "An expert in analyzing images and generating text descriptions associate it with user provided {topic} "
        "categories. Capable of both image-to-text"
        "after done categorizing use int_tool to search images with the same captions"
    ),
    tools=[image_caption_tool,int_tool],
    verbose=True
)


image_task = Task(
    description="search for images on internet with image caption.",
    expected_output='when result apears Get few accessible links from there alike caption and mention image captions, Provide it once done',
    agent=image_agent,
    tools=[image_caption_tool,int_tool],
)
crew_img = Crew(
    agents=[ image_agent],
    tasks=[image_task,image_task],
    verbose=True,
    planning=False,  
)
image_url='artifacts/buterfly.png'

def execute_crew(topic: str,image_url:str):
    crew_img.kickoff(inputs={"topic": topic,"image_url": image_url})

# response=execute_crew('define this image and provide images like these make sure of color ',image_url)
# print(response)