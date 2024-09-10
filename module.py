from crewai import crew
from crewai import  Crew
from langchain_openai import ChatOpenAI
import os



os.environ['OPENAI_API_BASE'] = 'http://127.0.0.1:11434/v1'
os.environ['OPENAI_MODEL_NAME'] = 'mistral:latest'
os.environ['OPENAI_API_KEY'] = 'NA'

llm  = ChatOpenAI(
    base_url = 'http://localhost:11434/v1',
    model='mistral:latest',
    api_key='NA',
)



from tasks_ import research,write,image_task,router_task
from agents_ import researcher, writer,image_agent,Router_Agent

crew_yt = Crew(
    agents=[researcher, writer],
    tasks=[research,write],
    verbose=True,
    planning=False, 
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
# Function to execute the crew tasks
def execute_crew(topic: str):
    crew_yt.kickoff(inputs={"topic": topic})

# # Test the system
# execute_crew("YouTube video about Python tutorials")  # This will trigger the YouTube Video Search Tool
# execute_crew("Market analysis of 2024 stocks in the USA")  # This will trigger the Internet Search Tool


rag_crew = Crew(
    agents=[Router_Agent],
    tasks=[router_task],
    verbose=True,
    full_output=True,

)
# path='artifacts\william.pdf'
# topic="who is williams wordworths wife"
# output=rag_crew.kickoff(inputs={"pdf_url":"artifacts/william.pdf","topic": topic})
# print(output)
# def execute_crew(topic: str,path:str):
#     rag_crew.kickoff(inputs={"topic": topic,"url":path})
# execute_crew()