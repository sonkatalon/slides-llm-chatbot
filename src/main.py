import os, time, argparse
from typing import Dict, Any, List

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

KB_DIR = os.getenv("KB_DIR", "kb")

SYSTEM_PROMPT = r"""You are a careful assistant answering ONLY with information grounded in the provided context.
If the answer is not present in the context, reply concisely with: "I don't know."
When relevant, keep answers brief and actionable.
r"""

QA_TEMPLATE = r"""{system}

Context:
{context}

Question: {question}

Answer:
r"""

def build_retriever() -> Any:
    loader = DirectoryLoader(KB_DIR, glob="**/*.md", loader_cls=TextLoader)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vs = FAISS.from_documents(chunks, embeddings)

    retriever = vs.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 1, "score_threshold": 0.2},
    )
    return retriever

def build_chain(retriever) -> Any:
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.2)
    prompt = PromptTemplate.from_template(QA_TEMPLATE).partial(system=SYSTEM_PROMPT)
    chain = RetrievalQA.from_chain_type(
        llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )
    return chain

def answer(question: str) -> Dict[str, Any]:
    t0 = time.perf_counter()
    retriever = build_retriever()
    t1 = time.perf_counter()
    chain = build_chain(retriever)
    out = chain.invoke({"query": question})
    t2 = time.perf_counter()

    sources = []
    for d in out.get("source_documents", []):
        src = d.metadata.get("source", "")
        # normalize source path to be relative under kb/
        idx = src.find("kb/")
        sources.append(src[idx+3:] if idx >= 0 else src)

    return {
        "answer": out.get("result", ""),
        "sources": sources,
        "timings": {
            "index_ms": round((t1 - t0) * 1000, 1),
            "llm_ms": round((t2 - t1) * 1000, 1),
            "total_ms": round((t2 - t0) * 1000, 1),
        },
    }

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", "--question", dest="question", required=True, help="Question to ask")
    args = parser.parse_args()
    res = answer(args.question)
    print("--- Answer ---")
    print(res["answer"])
    print("\n--- Sources ---")
    for s in res["sources"]:
        print("-", s)
    print("\n--- Timings (ms) ---")
    for k, v in res["timings"].items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    cli()
