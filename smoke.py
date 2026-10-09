#!/usr/bin/env python3
"""Run an older JSON decoder against baseline and additive response fixtures."""

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

WORDS = {
    "en": {"compatible": "Older client accepts the added response field", "regression": "Older client rejects the added response field", "inconclusive": "Baseline decoder did not pass", "invalid": "Invalid fixture or command"},
    "fr": {"compatible": "L’ancien client accepte le champ ajouté", "regression": "L’ancien client refuse le champ ajouté", "inconclusive": "Le décodeur échoue déjà sur la base", "invalid": "Fixture ou commande invalide"},
    "es": {"compatible": "El cliente antiguo acepta el campo añadido", "regression": "El cliente antiguo rechaza el campo añadido", "inconclusive": "El decodificador falla en la base", "invalid": "Fixture o comando no válido"},
}


def inspect(fixture, field, value, command, timeout=15):
    if not isinstance(fixture, dict) or not isinstance(field, str) or not field or field in fixture:
        raise ValueError("root JSON object and new field required")
    if not command:
        raise ValueError("decoder command required")
    def run(data):
        result = subprocess.run(command, input=json.dumps(data), text=True, capture_output=True,
                                timeout=timeout, check=False)
        return result.returncode
    baseline = run(fixture)
    added = run({**fixture, field: value})
    status = "inconclusive" if baseline != 0 else "regression" if added != 0 else "compatible"
    return {"status": status, "baseline_exit": baseline, "added_exit": added, "field": field}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("demo", "check"))
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--field", default="total")
    parser.add_argument("--value", default="1", help="JSON value to add")
    parser.add_argument("--decoder-cmd", help="trusted local command, parsed without a shell")
    parser.add_argument("--lang", choices=WORDS, default="en")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            fixture = {"items": []}
            command = [sys.executable, str(Path(__file__).parent / "examples" / "strict_decoder.py")]
        else:
            if not args.fixture or not args.decoder_cmd:
                parser.error("check requires --fixture and --decoder-cmd")
            fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
            command = shlex.split(args.decoder_cmd)
        report = inspect(fixture, args.field, json.loads(args.value), command)
    except (OSError, ValueError, TypeError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        print(f"{WORDS[args.lang]['invalid']}: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False) if args.json else WORDS[args.lang][report["status"]])
    return 0 if args.command == "demo" or report["status"] == "compatible" else 2


if __name__ == "__main__":
    raise SystemExit(main())
