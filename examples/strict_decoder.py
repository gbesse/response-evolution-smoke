import json
import sys

data = json.load(sys.stdin)
if not isinstance(data, dict) or set(data) != {"items"}:
    raise SystemExit(2)
