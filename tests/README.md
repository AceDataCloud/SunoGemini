# Runtime checks

Run ordinary contracts: `python3 -m unittest discover -s tests`.

Download the official Gemini CLI bundle, then run a no-charge local fixture:

```sh
python3 tests/smoke_extension.py --cli /absolute/path/to/gemini.js --output /tmp/suno-local-check.json
```

To read only the deployed Suno model reference tool, export an existing authorized Suno application key as `ACEDATACLOUD_SUNO_TEST_TOKEN`, then add `--live-info`. No generation/search tool is called; the model is still a deterministic localhost fixture. Token acquisition/configuration uses native extension settings and an isolated encrypted fallback, never the user's keychain. Do not pass a key on the command line or commit the result.

Remote Git installation is checked separately after the review branch is published; `--source` can point to the actual GitHub URL and `--ref` to a review commit/branch. Local fixtures rewrite only an isolated copy's endpoint and never publish it.
