# BM25 document retriever

Runnable educational demo/starter with synthetic examples.

Ranks a small JSON corpus with BM25 term-frequency scoring. Scores use lexical overlap; they are neither embeddings nor semantic similarity. IDs must be unique. Empty or out-of-vocabulary queries return no hits. This in-memory implementation is intended for small corpora.

## Run

Python 3.10+; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

No network requests, credentials, or paid services are used. Any model/provider integration would be a separate adapter; the current implementation performs only the operations described here.

Read `main.py` for the public functions and `test_main.py` for success/failure invariants. Fixture content is synthetic and safe to replace with local non-sensitive examples.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
