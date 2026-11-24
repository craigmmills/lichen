# lichen

A database of who works on data and AI for nature: biodiversity, ecosystems, land, fresh
water and the ocean. Every fact in it is quoted from a public web page, with the page's
address and the date it was read.

This is a snapshot taken on 23 November 2026. It will be updated as the database grows.

## What is in it

- 18,407 records: 10,557 organisations, 3,787 projects, 2,669 programmes, 1,107 datasets
  and 287 models.
- 207 countries and territories, plus a global layer for bodies that work across borders.
- 53,735 quoted facts from about 24,600 web pages on about 10,000 websites.
- Organisations by sector: government 3,092, NGO 2,453, academic 2,324, company 1,626,
  Indigenous and community bodies 584, funders 371, multilateral 107.

Records of individual people are left out of this copy.

## How it was built

AI agents searched the web country by country under written rules, in October and
November 2026. An agent could only record a fact if it had fetched a page that says it,
and each fact stores the page address, the date and a short quote. Nothing comes from a
model's memory. Only open pages were read: nothing behind a login or paywall, and a
site that refused automated reading was left alone. A second AI model re-read records
without seeing the first labels, and samples were checked against the live pages.

## How far to trust it

- No person has reviewed the records one by one. In two blind samples of 150 records,
  read by two other AI models, 8% and 11% had a fault of some kind, and 5% and 7% made
  a false claim about who runs, leads, funds or built something.
- It records what organisations publish online. Work nobody wrote up is missing, and
  pages in English are easier to find, so treat every count as a floor.
- "Nothing found" is weaker than "does not exist". A record labelled `none` for
  technology means the pages read showed none.
- Records overlap by design: a project and the organisation that runs it are separate
  records.
- A quote was on the page on the date given. Pages change.

## The files

`docs/` is the explorer site. `records.csv` has one row per record: file, name, kind, scope, sector, labels, website,
number of facts and a one-sentence summary. Start there.

`entries/<scope>/<id>.yaml` holds one record per file. `scope` is `global` or a
two-letter country code (`br` is Brazil). The fields:

| Field | Meaning |
| --- | --- |
| `kind` | organisation, programme, project, dataset or model |
| `sector` | for organisations: government, multilateral, academic, ngo, community, company or funder |
| `roles` | what it does in the field: `builds-ai`, `uses-ai`, `supplies-data`, `funds`, `governs` (manages or regulates a named place), `convenes` |
| `ai_label` | `ai` if the pages show AI in use; `conservation-tech` for technology without AI; `data-infrastructure` for nature data that models are trained and checked on; `none` if the pages showed no technology |
| `realms` | land, freshwater, ocean |
| `techniques` | the kinds of data the work uses, such as satellite images, camera traps or sound |
| `ai_types` | the kind of AI, set only where a page names the method, so counts from it are floors |
| `summary` | one or two sentences written from the facts |
| `facts` | each has a `claim`, the page `url`, the date `fetched` and a `quote` from the page |
| `links` | relationships to other records (runs, funds, builds, uses, partners-with and so on), each with the page and quote behind it |
| `found_by`, `added_by`, `checked` | how the record was found, and when it was last checked |

"AI" here means any method that learns from data, from random forests to deep learning
and language models. Weather and climate modelling and most agricultural AI are out of
scope.

## Correcting a record or adding one

Use the explorer site: https://craigmmills.github.io/lichen/

Search for your organisation, open its record and press "Suggest a fix by email". If it is not
there, press "Add a record by email" under the list. An AI agent reads each email and checks the
change against the public page you link to, and a change goes in only when a public page supports
it. Please do not open pull requests against `entries/`: this is a copy, and they cannot be merged.

## Counting from it

```sh
uv run tools/build_db.py      # builds build/lichen.sqlite from entries/ (needs uv, nothing else)
uv run tools/findings.py      # prints the headline findings about AI for nature
```

The tables are listed at the top of `tools/build_db.py`. `labels/ai-records.csv` holds the labels the
findings are counted from, for the 3,863 records where two separate readings found AI in use, and
`labels/README.md` says how they were made.

## Using it with a coding agent

Clone the repository and open it in Claude Code, Codex, Cursor or a similar agent. `AGENTS.md` tells
the agent what the data is and the rules for reporting from it, and three skills in `.claude/skills/`
cover counting, looking up a record and checking the findings. Claude Code picks the skills up by
itself. With another agent, start with "read AGENTS.md first". Then ask in plain words, for example:

- "Using lichen, how many government bodies in Indonesia are recorded as using AI? Give the base,
  five examples with their files, and what the count cannot show."
- "Find my organisation in lichen and show me every fact it holds about us with the page each came
  from. Draft a correction for anything out of date."
- "Reproduce the finding on how far AI outputs get, then break it down for ocean work only."
- "Which funders appear most often in funding links to records in East Africa? Check ten of the
  links against the quoted pages before you answer."

Three habits make the answers better: ask for the base behind every percentage, ask for examples you
can open, and ask the agent to try to break its own answer before it reports.

## Licence

The data is in the public domain under [CC0 1.0](LICENSE): the records, `records.csv`, the labels and
the summaries. Use it for anything, with no need to ask or to credit, though a mention of where it
came from helps others find it. The scripts in `tools/` and the skills are under the
[MIT licence](LICENSE-CODE).

Two things the licence does not cover. The short quotes in each fact are the words of the pages they
came from and belong to their publishers; they are here as brief quotations with their source. The
fonts in `tools/fonts/` and `docs/fonts/` carry their own open licence, included beside them.
