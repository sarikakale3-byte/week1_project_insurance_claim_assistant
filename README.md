 SK Insurance Claims Assistant Chatbot

 This project implements an AI-powered Insurance Claims Processing & Settlement Assistant using Large Language Models (LLMs).

 ### Project Structure

├── app.py                  # Core logic (LLM call + JSON extraction + validation)
├── llm_engine_langchain.py # OpenAI API interaction
├── strealit.py            # Chatbot UI (Streamlit)
├── evaluation.py           # Evaluation script (runs test cases)
├── models/
│   └── schema.py           # Pydantic schema
├── utils/
│   ├── guardrails.py       # Safety checks (PII, injection, off-topic)
│   ├── prompt_builder.py   # System Prompt + few-shot logic
│   └── data_loader.py      # Product data loader
|   |__ memory.py           # Redis memory
|   |__ tools.py            # Tools which are bind to llm
├── data/
│   └── data.json           # Insurance product catalog
└── README.md

### Setup Instructions

## Clone GIT repository
git clone <your-repo-url>
cd <project-folder>
## Create Virtual ENvironment
python3 -m venv venv
source venv/bin/activate
## Install Dependencies
pip install -r requirements.txt
## Configure Environment
Create a .env file at root level abnd add below:
OPENAI_API_KEY=<your_api_key_here>
## Update memory.py with Redis url and password
## Run Chatbot
streamlit run stremlit.py
