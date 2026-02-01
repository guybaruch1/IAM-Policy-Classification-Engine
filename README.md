# IAM Policy Classification Engine 🔐🤖

A research-oriented system for **automatic security classification of AWS IAM policies** using Large Language Models (LLMs).  
The project evaluates how well modern LLMs can reason about IAM permissions, least-privilege principles, and conditional access controls.

---

## ✨ Key Features

- ✅ Accepts **AWS IAM policies in JSON format**
- ✅ Classifies policies as **Strong** or **Weak**
- ✅ Produces **concise, security-focused reasoning**
- ✅ Supports **multiple LLM providers** (Hugging Face & OpenAI)
- ✅ Enforces **structured JSON output** via schema validation
- ✅ Includes an **evaluation pipeline** with accuracy metrics
- ✅ Designed for **analysis and research**, not production enforcement

---

## 🧠 Motivation

IAM misconfigurations are a leading cause of cloud security incidents.  
This project explores whether Large Language Models can reliably analyze IAM policies and distinguish secure configurations from risky ones - including **borderline cases** that require semantic reasoning rather than simple pattern matching.

---

## 🗂 Project Structure

```
IAM-Policy-Classification-Engine/
│
├── main.py                     # Entry point - runs policy classification
├── evaluate.py                 # Evaluation script over labeled datasets
│
├── classifier.py               # Core classification logic
├── llm_client.py               # Generic LLM client interface
├── prompt.py                   # Prompt templates and construction
├── schemas.py                  # Output JSON schemas
├── schema_self_check.py        # Self-check logic for the scheme
│
├── providers.py                # Provider abstraction
├── openai_provider.py          # OpenAI-specific implementation
├── huggingface_provider.py     # Hugging Face-specific implementation
│
├── logging_utils.py            # Centralized logging utilities
│
├── policies/                   # Example IAM policies (JSON)
│   ├── strong_policy.json
│   ├── weak_policy.json
│
├── outputs/                    # Generated outputs and evaluation results
│   └── evaluation_results.json
│
├── .env.example                # Environment variable template
├── .gitignore
│
├── requirements.txt            # Python dependencies
└── README.md

```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/guybaruch1/IAM-Policy-Classification-Engine.git
cd IAM-Policy-Classification-Engine
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file based on `.env.example`:

```env
HF_API_TOKEN=your_huggingface_token
HF_MODEL=meta-llama/Meta-Llama-3-8B-Instruct

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
```

---

## 🚀 Usage

### 🔹 Classify a Single IAM Policy

```bash
python main.py policies/weak_policy.json
```

### 🔹 Evaluate Multiple Policies

```bash
python evaluate.py
```

Results are saved to:
```
outputs/evaluation_results.json
```

---

## 🧪 Evaluation Summary

- Dataset size: 12 IAM policies
- Includes strong, weak, and borderline cases
- Accuracy comparison across LLMs
- Structured JSON outputs validated via schema

---

## ⚠️ Limitations

- Research-oriented (not production-ready)
- Dependent on LLM reasoning quality
- IAM policies can be semantically ambiguous

---

## 📌 Future Work

- Larger datasets
- Confusion matrices
- Additional LLM providers
- Hybrid rule-based + LLM analysis

---

## 📄 License

Academic & research use only.
