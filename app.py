import os
import gradio as gr
import requests
import pandas as pd

from smolagents import LiteLLMModel, CodeAgent, DuckDuckGoSearchTool
from gaia_tools import reverse_string_tool, execute_script_file, download_from_link

# Custom system prompt for reasoning behavior
ASSISTANT_PROMPT = """You are a smart AI assistant. When a question is provided, break it down logically and use tools if required.
Your final response should contain only the clean answer — no extra text or phrases like "FINAL ANSWER:".
Keep answers short and precise (number, word, or a comma-separated list).
Follow these strict guidelines:
1. Do NOT use unlisted tools.
2. Use ONE tool per step only.
3. If a Python file is involved, use execute_script_file.
4. If question text looks reversed, use reverse_string_tool first.
5. For puzzles or logical riddles, try solving directly.
6. Use download_from_link if you need to fetch any external file.
7. Assume every question is solvable — don’t give up.
"""

API_ENDPOINT = "https://agents-course-unit4-scoring.hf.space"

# Agent class wrapper
class SmartAgent:
    def __init__(self):
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY is not set in environment.")

        self.model = LiteLLMModel(
            model_id="gemini/gemini-2.0-flash-lite",
            api_key=gemini_key,
            system_prompt=ASSISTANT_PROMPT,
        )

        self.executor = CodeAgent(
            tools=[
                DuckDuckGoSearchTool(),
                reverse_string_tool,
                execute_script_file,
                download_from_link,
            ],
            model=self.model,
            add_base_tools=True,
        )

    def __call__(self, query: str) -> str:
        return self.executor.run(query)

# Evaluation and submission process
def evaluate_and_send(profile: gr.OAuthProfile | None):
    space_id = os.getenv("SPACE_ID")

    if not profile:
        return "Please log in to Hugging Face first.", None

    user_handle = profile.username
    print(f"Running for: {user_handle}")

    fetch_url = f"{API_ENDPOINT}/questions"
    submit_url = f"{API_ENDPOINT}/submit"

    try:
        agent_instance = SmartAgent()
    except Exception as error:
        return f"Failed to initialize agent: {error}", None

    try:
        question_data = requests.get(fetch_url, timeout=15).json()
    except Exception as error:
        return f"Failed to fetch questions: {error}", None

    output_log = []
    answer_list = []

    for entry in question_data:
        q_id = entry.get("task_id")
        prompt = entry.get("question")
        if not q_id or not prompt:
            continue
        try:
            prediction = agent_instance(prompt)
            answer_list.append({"task_id": q_id, "submitted_answer": prediction})
            output_log.append({"Task ID": q_id, "Question": prompt, "Submitted Answer": prediction})
        except Exception as error:
            output_log.append({
                "Task ID": q_id,
                "Question": prompt,
                "Submitted Answer": f"ERROR: {error}"
            })

    if not answer_list:
        return "No answers were generated.", pd.DataFrame(output_log)

    submission_payload = {
        "username": user_handle.strip(),
        "agent_code": f"https://huggingface.co/spaces/{space_id}/tree/main",
        "answers": answer_list,
    }

    try:
        response = requests.post(submit_url, json=submission_payload, timeout=60)
        result = response.json()
        status_message = (
            f"✅ Submitted!\n"
            f"User: {result.get('username')}\n"
            f"Score: {result.get('score', 'N/A')}% "
            f"({result.get('correct_count', '?')}/{result.get('total_attempted', '?')})\n"
            f"Message: {result.get('message', 'No message returned.')}"
        )
        return status_message, pd.DataFrame(output_log)
    except Exception as error:
        return f"Submission failed: {error}", pd.DataFrame(output_log)

# Gradio Interface
with gr.Blocks() as interface:
    gr.Markdown("# 🤖 GAIA Final Agent Evaluation")
    gr.Markdown("""
    1. Set your Gemini API key (as secret).
    2. Log into Hugging Face.
    3. Click below to evaluate and submit your agent!
    """)

    gr.LoginButton()
    submit_button = gr.Button("🔍 Run Agent & Submit Answers")
    status_box = gr.Textbox(label="Submission Output", lines=6, interactive=False)
    results_display = gr.DataFrame(label="Evaluation Details")

    submit_button.click(fn=evaluate_and_send, outputs=[status_box, results_display])

if __name__ == "__main__":
    print("🚀 Launching app...")
    interface.launch(debug=True, share=False)
