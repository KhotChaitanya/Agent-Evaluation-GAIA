# Agent-Evaluation-GAIA: Tool-Augmented Reasoning System using smolagents

This repository contains a reasoning-first agent built as part of the HuggingFace course final evaluation. The agent leverages the `smolagents` framework with Gemini LiteLLM, enhanced by custom tools and a secure Gradio-based interface.

---

## Objective

- Implement a modular AI agent using `smolagents` and Gemini LLM.
- Use a custom reasoning system prompt with tool constraints.
- Integrate tools: reverse string, code execution, file download.
- Submit predictions to GAIA’s evaluation API using Hugging Face login.
- Build an interactive frontend using Gradio Blocks and OAuth.

---

## Core Components

### 1. Agent (`app.py`)
- Initializes the agent using Gemini-2.0 Flash model (via `LiteLLMModel`).
- Loads tools:  
  - DuckDuckGo search  
  - `reverse_string_tool`  
  - `execute_script_file`  
  - `download_from_link`  
- Uses a structured system prompt enforcing logical step-by-step tool use.
- Submits answers via authenticated Hugging Face API call.

### 2. Custom Tools (`gaia_tools.py`)
- `reverse_string_tool`: Flips input string.
- `execute_script_file`: Reads and runs a Python file using the agent's Python interpreter.
- `download_from_link`: Downloads external content into the runtime environment.

### 3. Interface (via Gradio)
- Login with Hugging Face (`gr.OAuthProfile`)
- One-click evaluation and submission
- Displays submission status and full evaluation table

---

## Requirements
- Python 3.10+
- Gemini API Key set as `GEMINI_API_KEY`
- (Optional) Hugging Face OAuth setup for `gr.LoginButton`

---

### Build & Execution
# Build:

![build](https://github.com/user-attachments/assets/c2adba94-f43c-449b-85a7-b0fe8dd865c4)

# Execution:

![output](https://github.com/user-attachments/assets/0dbb7ee2-51a0-41b9-b53a-6932436470cf)

---

### Install Dependencies
```bash
pip install -r requirements.txt
```
---

### Running the Agent
#### Set your Gemini API key
export GEMINI_API_KEY=your_api_key_here

#### Optionally set your Hugging Face space ID
export SPACE_ID=your-space-id

#### Launch the interface
python app.py

---

