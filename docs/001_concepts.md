## Part 1: Foundational Concepts

### How LLMs Work Under the Hood

```mermaid
graph LR
    A[Raw Text] --> B[Break into tokens]
    B --> E[Weights /<br/>statistics]
    E --> F[Next token]
    F --> G{More<br/>tokens?}
    G -->|Yes| F
    G -->|No| H[Done]
```

#### Key Building Blocks

**🧩 Tokens**

- The "words" that LLMs understand
- ~4 characters = 1 token
- Example: "Hello world!" = 3 tokens

**🧠 Weights**

- The "knowledge" stored in the model
- GPT-4 has ~1.7 trillion parameters
- Think of them as tiny pieces of learned information

**🎯 Prompt Engineering**

- The art of asking LLMs the right questions
- Better prompts = better answers

Deep Dive into LLMs by Andrej Karpathy: https://www.youtube.com/watch?v=7xTGNNLPyMI

**What LLMs Excel At:**

- ✅ Text generation and completion
- ✅ Pattern recognition

**What LLMs Struggle With:**

- ❌ Factual accuracy (hallucinations)
- ❌ Mathematical precision
- ❌ Consistent reasoning

### Embeddings and Semantic Search

```mermaid
graph LR
    A["Text: 'The cat sat on the mat'"] --> B[Embedding Model]
    B --> C["[0.2, -0.1, 0.8, ...]"]

    D["Text: 'A feline rested on the rug'"] --> B
    B --> E["[0.19, -0.09, 0.79, ...]"]

    C --> F[Cosine Similarity]
    E --> F
    F --> G["High Similarity Score<br/>= Similar Meaning!"]
```

<details>
<summary>
Q: Why Embeddings Matter?
</summary>

A: Semantic Search

</details>

### RAG (Retrieval-Augmented Generation) Pipeline

```mermaid
flowchart LR
    A['How do I deploy to production?'] --> B[Convert to embedding]
    B --> C[Vector search]
    C --> F[LLM generates answer]

    H[Knowledge base] --> I[Split into chunks]
    I --> J[Create embeddings]
    J --> K[Store in vector DB]
    K --> C
```

#### Why RAG is Powerful

**Without RAG:**

- ❌ LLM: "I don't have information about your specific deployment process"
- ❌ Outdated information from training data
- ❌ Generic answers

**With RAG:**

- ✅ LLM: "Based on your deployment guide, here are the exact steps..."
- ✅ Up-to-date information from your docs
- ✅ Company-specific answers
