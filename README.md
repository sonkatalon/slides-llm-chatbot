# LLM Chatbots

Demo a Retrieval-Augmented Generation (RAG) chatbot using LangChain, OpenAI, and FAISS vector store.

## Overview

This project implements a question-answering chatbot that:

- Loads documents from a knowledge base
- Uses vector similarity search to retrieve relevant context
- Generates grounded answers using OpenAI's GPT models
- Includes comprehensive evaluation metrics

## Features

- **RAG Implementation**: Retrieval-Augmented Generation with FAISS vector store
- **Document Processing**: Automatic chunking and embedding of markdown documents
- **Grounded Responses**: Answers are based only on provided context
- **Source Attribution**: Tracks and returns source documents for transparency
- **Performance Metrics**: Timing analysis for indexing and LLM calls
- **Evaluation Framework**: Automated testing with semantic similarity and hallucination detection

## Project Structure

```
├── src/
│   ├── main.py          # Core RAG implementation
│   └── run_eval.py      # Evaluation framework
├── kb/                  # Knowledge base documents
│   ├── policies/        # Company policies
│   └── product/         # Product documentation
├── goldens/
│   └── qa.yaml          # Test questions and expected answers
├── requirements.txt     # Python dependencies
├── test.sh             # Test script
└── improvements.md     # Suggested enhancements
```

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- UV package manager

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd llm-chatbot
```

2. Install dependencies:

```bash
uv sync
```

3. Set your OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

### Ask Questions

```bash
uv run src/main.py --q "What is our refund policy timeline?"
```

Output

```
--- Answer ---
Customers have 30 days from purchase to request a refund, and refunds are issued within 5–10 business days after verification.

--- Sources ---
- policies/refunds.md

--- Timings (ms) ---
index_ms: 2584.2
llm_ms: 1856.9
total_ms: 4441.0
```

Ask another question

```bash
uv run src/main.py --q 'How fast should we response to a security event?'
```

Output

```
--- Answer ---
Target initial response within 48 hours.

--- Sources ---
- policies/security.md

--- Timings (ms) ---
index_ms: 1309.9
llm_ms: 1244.5
total_ms: 2554.5
```

### Run Evaluation

```bash
uv run src/run_eval.py
```

Output

```
{
  'acc_semantic_avg': 0.862,
  'hallucination_rate': 0.0,
  'latency_p50_ms': 2480.1,
  'latency_p95_ms': 2635.3
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: `gpt-4o-mini`)
- `KB_DIR`: Knowledge base directory (default: `kb`)

### Retrieval Parameters

Current configuration in `src/main.py`:

- **Chunk size**: 800 characters
- **Chunk overlap**: 120 characters
- **Retrieved documents**: 1 (k=1)
- **Similarity threshold**: 0.2

## Evaluation Metrics

The evaluation framework measures:

- **Semantic Accuracy**: Cosine similarity between generated and expected answers
- **Hallucination Rate**: Percentage of responses not grounded in expected sources
- **Latency**: P50 and P95 response times
- **Source Grounding**: Verification that answers cite correct source documents

## Knowledge Base

The `kb/` directory contains sample documents:

- `policies/refunds.md`: Refund policy information
- `policies/security.md`: Security and data protection policies
- `product/faq.md`: Product FAQ including RAG explanations
