import yaml, statistics
from pathlib import Path
from sentence_transformers import SentenceTransformer
from main import answer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def sim(a,b):
    ea, eb = embedder.encode([a,b], normalize_embeddings=True)
    return float((ea*eb).sum())

def run():
    gold = yaml.safe_load(Path("goldens/qa.yaml").read_text())
    sims, hallucs, latencies = [], [], []
    for item in gold:
        res = answer(item["question"])
        lat = res["timings"]["total_ms"]
        latencies.append(lat)

        ans = (res["answer"] or "").strip()

        # Negative tests expect "I don't know"
        if item.get("allow_no_answer"):
            hallucs.append(0 if "i don't know" in ans.lower() else 1)
            continue

        # Semantic accuracy
        sims.append(sim(ans, item["expected"]))

        # Grounding by expected sources
        expected_sources = set(item.get("expected_sources", []))
        got = set(res.get("sources", []))
        grounded = any(any(exp in g for g in got) for exp in expected_sources) if expected_sources else True
        hallucs.append(0 if grounded else 1)

    sims_avg = round(sum(sims)/max(1,len(sims)),3)
    hallu_rate = round(sum(hallucs)/len(hallucs),3)
    p50 = round(statistics.median(latencies),1)
    p95 = round(sorted(latencies)[int(0.95*len(latencies))-1],1) if len(latencies) >= 2 else p50

    print({
        "acc_semantic_avg": sims_avg,
        "hallucination_rate": hallu_rate,
        "latency_p50_ms": p50,
        "latency_p95_ms": p95
    })

if __name__ == "__main__":
    run()
