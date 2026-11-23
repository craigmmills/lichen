# For coding agents

This repository is a public copy of lichen, a database of who works on data and AI for nature. It is
data plus a few scripts. Your job here is to read, count and report. Nothing in it needs installing
beyond [uv](https://docs.astral.sh/uv/).

- Start with `README.md` for what the data is and how far to trust it.
- Three skills in `.claude/skills/` say how to do the common jobs. Claude Code loads them by itself.
  Any other agent should read the one that fits before starting:
  - `lichen-counts/SKILL.md`: counting and comparing records with SQL, and the rules that keep counts sound.
  - `lichen-lookup/SKILL.md`: finding one record and showing its sources.
  - `lichen-findings/SKILL.md`: reproducing and extending the headline findings.
- `uv run tools/build_db.py` builds `build/lichen.sqlite`. `uv run tools/findings.py` prints the findings.
  `uv run tools/build_site.py` rebuilds the explorer in `docs/`.

Rules:

- Say nothing about a record that its quoted facts do not support. Do not fill gaps from memory.
- Give the base with every percentage, and say "at least" for counts: the database is a floor.
- Do not edit files under `entries/`. Corrections go by email through the explorer site, so each one
  is checked against a public page.
- Do not send automated requests to the websites quoted here in bulk. Open pages one at a time when
  checking a claim.
