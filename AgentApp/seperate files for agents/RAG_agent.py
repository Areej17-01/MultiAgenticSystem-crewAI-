
from langchain_openai import ChatOpenAI
import os
from crewai_tools import PDFSearchTool

from crewai_tools  import tool
from crewai import Crew
from crewai import Task
from crewai import Agent

ares_key='ares_0f5fe3f0fbeb3ad774accc9c5cde9403e7123817af48a0416317006d8cb9569d'

import os
from langchain_openai import ChatOpenAI

from crewai_tools import PDFSearchTool
from crewai_tools  import tool
from crewai import Crew
from crewai import Task
from crewai import Agent
from langchain_openai import ChatOpenAI

# Set environment variables
import os
os.environ['OPENAI_API_BASE'] = 'http://127.0.0.1:11434/v1'#'http://192.168.18.1:11434/v1:11434/v1'
os.environ['OPENAI_MODEL_NAME'] = 'mistral:latest'
os.environ['OPENAI_API_KEY'] = 'NA'



from langchain_openai import ChatOpenAI
llm=ChatOpenAI(
    model='mistral:latest',
    base_url='http://127.0.0.1:11434/v1',
    openai_api_key='NA'
)


# r=llm.invoke('hi')
# print(r)
import ollama

url='Volunteering.pdf'



rag_tool = PDFSearchTool(
    pdf='stream/artifacts',
    config=dict(
        llm=dict(
            provider="ollama",  # Ollama as the LLM provider
            config=dict(
                model="mistral:latest",  # Ollama's Mistral model identifier
                temperature=0.2,  # Set the temperature to control randomness
                # base_url='http://127.0.0.1:11434/v1',  # Ollama's base URL
            ),
        ),
        embedder=dict(
            provider="huggingface",  # Hugging Face for embedding
            config=dict(
                model="sentence-transformers/all-MiniLM-L6-v2",  # Embedding model
            ),
        ),
    )
)



import json,requests
from crewai_tools import BaseTool
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

class MyCustomTool(BaseTool):
    name: str = "Internet Search Tool"
    description: str = "This tool searches the internet for any user query and provides a summary."

    def _run(self, topic: str)  -> str:

        url = "https://api-ares.traversaal.ai/live/predict"
        payload = { "query": [topic] }
        headers = {
            "x-api-key": 'ares_dca47048934bce4fb9c5d2c5bb1dd92ec6c5deee92c6452f1b5ce30e1b0a6ac4',  # Replace with your actual ARES API key
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return json.dumps(data, indent=2)  # Adjust formatting as needed
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"

# Define the tool
int_tool = MyCustomTool()

""


Router_Agent = Agent(
    role='Router',
    goal='Provide answers to users from the vector database and internet ',
    backstory=(
        "You are an expert in answering  questions."
        "you use vector database to search {topic} in it and when you found out answer in context you provide it"
        "If the answer is not found in the vector database, you use the internet to answer the {topic} and you provide it "
        "both tools can be used together"

    ),
    verbose=True,
    allow_delegation=False,
    tools=[rag_tool, int_tool],  # Ensure both tools are properly defined
    llm=llm,

)



router_task = Task(
    description=("You answer user with both vector database and internet as needed."
    "if in any case there are two different answers provide diffreneces b/w them"
    ),
    expected_output=("you provide answer from vector database and internet ,you answer it in proper format mentioning from which source answer is from."),
    agent=Router_Agent,

)
rag_crew = Crew(
    agents=[Router_Agent],
    tasks=[router_task],
    verbose=True,
    full_output=True,

)
inputs ={"topic":"when was william born?"}

result = rag_crew.kickoff(inputs=inputs)
print(result)
