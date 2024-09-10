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
researcher = Agent(
    role='Internet Search Specialist',
    goal='Provide information to the user about their query.',
    backstory=(
        "An expert in internet searches about {topic}. Your task is to provide "
        "the user with accurate results based on their query. You are skilled at searching "
        "for {topic} online and compiling comprehensive findings."
        "use youtube tool only when video or youtube is mentioned in {topic}"
    ),
    tools=[int_tool, yt_tool],  # Add both Internet Search and YouTube Video Search tools
    verbose=True
)
writer = Agent(
    role='Content Writer',
    goal='Create engaging and informative blog posts based on the research.',
    backstory=(
        "A skilled writer who transforms research into compelling, informative content. "
        "You create blog posts based on the provided research, ensuring the content is "
        "accessible, engaging, and avoids complex jargon."
        "use example or sample if possible"
    ),
    tools=[],  
    verbose=True
)

from agents_ import *
from tools_ import *

research = Task(
    description=(
        "1. Search the internet for the {topic} and provide a summary .\n"
        "2. Extract relevant information from the search results or videos.\n"
        "3. Use youtube tool only when video is mentioned in {topic} "
        "3. Identify key points and arguments related to {topic}.\n"
        "4. Organize and summarize findings in a clear and concise manner."
    ),
    expected_output='A concise summary of the search results or YouTube videos.',
    agent=researcher,
)

write = Task(
    description="""Create a blog post based on the research findings.""",
    expected_output='A 2-paragraph blog post formatted in markdown with engaging, informative, and accessible content and links .Add a sample and example if possible',
    agent=writer,
    output_file='blog-posts/new_post.md',  
)

crew_yt = Crew(
    agents=[researcher, writer],
    tasks=[research,write],
    verbose=True,
    planning=False, 
)
crew_yt.kickoff(inputs={"topic": 'what is recent usa stock market'})