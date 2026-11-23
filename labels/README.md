# Labels on the AI records

`ai-records.csv` has one row for each of the 3,863 records where two separate readings found AI in use:
the label the record was given when it was added (`ai_label: ai`), and a second reading by an AI model
(Claude Sonnet) that saw only the record's name, kind, country, summary and quoted facts, and none of
the first labels. The headline findings are counted from this file. `tools/findings.py` prints them.

`rubric.md` is the written rule the second reader was given, word for word. The columns:

| Column | Meaning |
| --- | --- |
| `ai` | `built` (develops, trains or adapts AI itself) or `used` (applies AI built by others) |
| `stage` | research, pilot, operational (in routine use), product (sold or offered to others), unclear |
| `chain` | the furthest step the evidence shows the output reaching: observe, assess, predict, decide, act |
| `task` | what the technology does, up to two codes |
| `threat` | the pressure on nature the work is aimed at, up to two codes; `none-specific` means general monitoring or research |
| `taxon` | the living things the work is about, up to three codes; `habitat` and `many` name no species group |
| `users` | who the evidence says uses the output |
| `method` | the data the work rests on |
| `open` | whether the evidence says the tool, model or data is open |

## What these labels cannot show

- They read only what the stored facts say. An agency that acts on a model's output and never writes
  that up is labelled as stopping early. "Not shown" is weaker than "did not happen".
- One model made them. A second model (Codex) labelled a sample of 400 for comparison. The two gave
  the same `chain` step for 76% of records and the same `stage` for 71%, and named an overlapping
  species group for 86%. Agreement was lowest on `users` (63%). Treat a difference of a few points
  between two groups as noise.
- The set leaves out records that only one reading called AI, so it is a conservative set, and it
  should not be used to work out what share of all organisations use AI.
- Records overlap: a project and the organisation that runs it can both be here.
