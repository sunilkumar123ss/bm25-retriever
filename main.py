"""Small, inspectable BM25 baseline; no neural model or network."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re


def tokenize(text):
    return re.findall(r"\w+", text.casefold(), flags=re.UNICODE)

