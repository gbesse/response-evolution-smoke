# Response Evolution Smoke

[Français](README.fr.md) · English · [Español](README.es.md)

**Will yesterday’s generated client still read tomorrow’s API response?** This small CI check feeds an older decoder both a known-good JSON response and the same response with one additive field. It reports `regression` only when the baseline passes and the additive response fails.

## Related projects

- [Hindsight #5454](https://github.com/vectorize-io/hindsight/issues/5454) reports an older generated Go client rejecting a newly added `total` field because it calls `DisallowUnknownFields()`.
- [oasdiff](https://github.com/oasdiff/oasdiff) compares API schemas; this tool instead executes your actual old decoder against response examples. No integration or affiliation is claimed.

## Ten-second demo

```sh
python3 smoke.py demo --lang en
python3 smoke.py check --fixture examples/list-response.json --field total --value 1 --decoder-cmd 'go run examples/old_go_client.go' --lang en
```

The bundled Python and Go decoders intentionally reject unknown fields, so the demo reports a regression. To check your own generated client, pass a trusted local decoder command that reads one JSON response on stdin and exits 0 when it can decode it. The command is executed locally without a shell. Exit codes for `check`: 0 compatible, 2 regression or inconclusive, 1 invalid input. The tool adds a field only at the JSON root; it does not parse OpenAPI or prove all future changes safe.

Python 3.11+, standard library. Run `python3 -m unittest discover -s tests -q`. MIT license.
