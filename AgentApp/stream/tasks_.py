####tasks for internet and youtube search
from crewai import Agent, Task, Crew
from agents_ import researcher,image_agent
from agents_ import *
from tools_ import *

research = Task(
    description=(
        "1. Search the internet for the {topic} and provide a summary.\n"
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
    expected_output='A 2-paragraph blog post formatted in markdown with engaging, informative, and accessible content.Add a sample and example if possible',
    agent=writer,
    output_file='blog-posts/new_post.md',  
)

##########task for image model

# Define the task for image-to-text or classification
# image_task = Task(
#     description="Perform an image caption or classification based on the provided image.",
#     expected_output='A generated caption or predicted class for the image with description, explain the image caption.',
#     agent=image_agent,
# )
# imageSearch_task = Task(
#     description=("Perform an image caption or classification based on the provided image and search for images on internet with caption."
#                  "when result apears Get few accessible links from there alike caption and mention captions"),
#     expected_output='image links to the images from internet with same almost same name.',
#     agent=image_agent,
#      tools=[image_caption_tool,int_tool]
# )
# # Add the image agent to the crew along with researcher and writer agents
image_task = Task(
    description="search for images on internet with image caption.",
    expected_output='when result apears Get few accessible links from there alike caption and mention image captions, Provide it once done',
    agent=image_agent,
    tools=[image_caption_tool,int_tool],
)
#for RAG model
from agents_ import Router_Agent

router_task = Task(
    description=("You answer user with both vector database of pdf and internet as needed."
    "if in any case there are two different answers provide diffreneces b/w them"
    ),
    expected_output=("you provide answer from vector database and internet ,you answer it in proper format mentioning from which source answer is from."),
    agent=Router_Agent,

)