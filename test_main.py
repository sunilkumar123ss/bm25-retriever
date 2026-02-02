import unittest
# Load this project's module explicitly, including when invoked from repository root.
import importlib.util as _import_util
from pathlib import Path as _Path
import sys as _sys
_spec = _import_util.spec_from_file_location(
    "sunil_agents_" + _Path(__file__).parent.name, _Path(__file__).with_name("main.py"))
_main = _import_util.module_from_spec(_spec)
_sys.modules[_spec.name] = _main
_spec.loader.exec_module(_main)
BM25 = _main.BM25
tokenize = _main.tokenize

class RetrievalTests(unittest.TestCase):
    def test_relevant_first_and_oov_abstains(self):
        index = BM25([{"id":"a","text":"voice latency latency"},{"id":"b","text":"lexical retrieval"}])
        self.assertEqual(index.search("voice latency")[0]["id"], "a")
        self.assertEqual(index.search("unseen"), [])
        self.assertEqual(index.search(""), [])

