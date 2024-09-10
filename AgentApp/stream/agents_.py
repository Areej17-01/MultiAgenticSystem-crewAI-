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


##########image agent 
# Define the image-based agent
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

############RAG agent


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
  

)


