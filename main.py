"""Small, inspectable BM25 baseline; no neural model or network."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re


def tokenize(text):
    return re.findall(r"\w+", text.casefold(), flags=re.UNICODE)


class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        if not math.isfinite(k1) or k1 <= 0 or not 0 <= b <= 1:
            raise ValueError("k1 must be positive and b must be in [0, 1]")
        self.documents = []
        seen = set()
        for doc in documents:
            if not isinstance(doc, dict) or not isinstance(doc.get("id"), str) or not doc["id"]:
                raise ValueError("each document needs a nonempty string id")
            if doc["id"] in seen or not isinstance(doc.get("text"), str):
                raise ValueError("document IDs must be unique and text must be a string")
            seen.add(doc["id"])
            self.documents.append(dict(doc))
        self.k1, self.b = k1, b
        self.counts = [Counter(tokenize(d["text"])) for d in self.documents]
        self.lengths = [sum(c.values()) for c in self.counts]
        self.average_length = sum(self.lengths) / len(self.lengths) if self.lengths else 0
        self.df = Counter(term for counts in self.counts for term in counts)

    def search(self, query, limit=5):
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("limit must be a positive integer")
        if not self.average_length:
            return []
        terms = set(tokenize(query))
        results = []
        n = len(self.documents)
        for doc, counts, length in zip(self.documents, self.counts, self.lengths):
            score = 0.0
            for term in terms:
                tf = counts[term]
                if not tf:
                    continue
                idf = math.log1p((n - self.df[term] + 0.5) / (self.df[term] + 0.5))
                norm = self.k1 * (1 - self.b + self.b * length / self.average_length)
                score += idf * tf * (self.k1 + 1) / (tf + norm)
            if score > 0:
                results.append({"id": doc["id"], "score": round(score, 8), "text": doc["text"]})
        return sorted(results, key=lambda x: (-x["score"], x["id"]))[:limit]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="voice latency")
    parser.add_argument("--corpus", type=Path, default=Path(__file__).with_name("corpus.json"))
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()
    try:
        results = BM25(json.loads(args.corpus.read_text())).search(args.query, args.limit)
    except (ValueError, OSError, TypeError) as exc:
        parser.error(str(exc))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
