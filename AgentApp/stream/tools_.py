
from crewai_tools import PDFSearchTool
from crewai_tools  import tool
from crewai_tools import BaseTool
import json
import requests
from crewai_tools import BaseTool, YoutubeVideoSearchTool
from pydantic import PrivateAttr
from transformers import pipeline 
from PIL import Image  

from dotenv import load_dotenv

load_dotenv()


# the Internet an youtube Search Tools
class MyCustomTool(BaseTool):
    name: str = "Internet Search Tool"
    description: str = "This tool searches the internet for any {topic} and provides a summary."
    from pydantic import PrivateAttr
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
yt_tool = YoutubeVideoSearchTool()

##############image toolsssssssss
import os
from PIL import Image




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

#RAG TOOLS


from crewai_tools import PDFSearchTool

class MyPDFSearchTool(BaseTool):
    name: str = "PDF Search Tool"
    description: str = "Searches through the specified PDF file for answers."


    _pdf_search_tool: PDFSearchTool = PrivateAttr()

    def _initialize_tool(self):
        # Initialize the tool only when it's invoked
        
        self._pdf_search_tool = PDFSearchTool(
            pdf="RAG/newpdf.pdf",
            config=dict(
                config=dict(
                llm=dict(
                    provider="ollama",  # Ollama as the LLM provider
                    config=dict(
                        model="mistral:latest",  # Ollama's Mistral model identifier
                        temperature=0.2,  
                        # base_url='http://127.0.0.1:11434/v1',  
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
        )

    def _run(self, topic: str) -> str:
        # Initialize the tool every time it is invoked
        self._initialize_tool()

        # Directly call the tool with the topic
        response = self._pdf_search_tool.run(topic)
        return response
        

# The tool is only initialized when explicitly invoked
rag_tool = MyPDFSearchTool()


