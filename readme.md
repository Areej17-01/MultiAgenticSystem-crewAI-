

# Multi-Agentic Tool Suite for Task Automation

## Overview

This project implements a **multi-agentic system** designed to perform automated tasks efficiently across various domains. Each agent operates independently, focusing on tasks like internet search, image classification, and retrieval-augmented generation (RAG) based queries. The project is structured with separate files for each agent, ensuring modularity and ease of execution.

## Key Features

- **Modular Design**: The system is composed of separate files, each containing runnable code for individual agents. This ensures that each agent works independently and executes its tasks correctly.
- **Multi-Agent Task Automation**: Agents are designed to handle tasks such as YouTube and internet searches, image classification, and RAG-based queries.
- **Fine-Grained Task Management**: The system supports asynchronous execution and task delegation among agents.

## Task Flow

The system is built to perform three primary tasks:

1. **YouTube and Internet Search with Blog Post Generation**
   - Agents perform searches on YouTube and the internet, retrieve content, and generate blog posts based on the results.
   
2. **Image Classification with Query Search**
   - Images are classified using pre-trained models, and relevant information is retrieved based on the classification results.

3. **RAG-Based Query with Search and Comparison (incomplete)**
   - Agents perform retrieval-augmented generation (RAG) to answer user queries, search for data on the internet, and compare results from multiple sources.

## File Structure

- `agents_.py`: Contains logic for the agents responsible for the tasks outlined above.
- `app.py`: The main entry point that orchestrates agent execution from the Streamlit app.
- `module.py`: Manages interactions between agents and the core functionality.
- `task.py` & `tasks_.py`: Define the specific tasks to be executed by agents.
- `tools_.py`: Contains tools that agents use for web scraping, API calls, and data processing.

Each file is runnable and works independently, ensuring that individual agents can be tested and executed separately.

## Installation

### 1. Download Ollama
Install **Ollama** as part of the system setup for local model execution:
- **MacOS**: Install via Homebrew:
  ```bash
  brew install ollama
  ```
- **Windows**: Install via the Ollama installer, available from the [official website](https://ollama.com).
- **Linux**: Follow the official website instructions for Linux distributions.

Once installed, download the necessary models:
```bash
ollama pull mistral or mistral-instruct
```
Adjust the modelfile:
follow this link to create modelfile: https://github.com/ollama/ollama/blob/main/docs/modelfile.md 

### 2. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Ensure that environment variables are configured correctly in a `.env` file.

### 5. Run the Application
directory \AgentApp\stream
```bash
streamlit run app.py
```

## Known Issues

### 1. **PDF Agent Issues**
The **PDF Agent** is currently unstable due to integration problems with the Mistral library. This agent may not function as expected when handling PDF-related tasks, and improvements are in progress.

### 2. **Internet Search Tool Problems**
Models like Mistral sometimes fail to invoke the internet search tool when called from the **Streamlit** app framework (GPT works fine). However, this tool works perfectly in the separate file provided in the `'separate file for agent'` folder, where it is executed directly.

## Dependencies

This project relies on several Python libraries, which are specified in the `requirements.txt` file. Key dependencies include:

- **AresAPI**: For internet search.
- **Langchain**: To initialize the Ollama model.
- **Streamlit**: For the UI (though currently experiencing issues).
- **Ollama**: For using the `mistral:latest` model.
- **CrewAI**: For agents and APIs.
- **Hugging Face**: For image classification.

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## How It Works

1. **Agents**: Each agent is responsible for performing a specific task. They can run independently or in coordination, with clear communication and task execution protocols.
   
2. **Task Management**: Tasks are defined in `task.py` and `tasks_.py`, and are executed by agents when invoked.

3. **Tool Execution**: The tools are defined in `tools_.py` and can be used by agents to perform various actions like API calls, image classification, and data retrieval.

4. **Streamlit Integration**: A user interface is built using **Streamlit**.
## Future Development

- **PDF Agent Fixes**: Resolve the Mistral integration issues with the base PDF tool to stabilize PDF-related tasks.
- **Streamlit Debugging**: Fix execution bugs within the Streamlit execution with mistral.
- **New Agents**: Develop additional agents to expand the functionality of the system.

---

