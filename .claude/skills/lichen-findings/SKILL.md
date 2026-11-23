---
name: lichen-findings
description: Reproduce, check or extend the headline findings about AI for nature from the lichen database (how far AI outputs get, which species and threats get attention, which sectors research, sell or run it). Use when asked to verify a published figure, break a finding down by country, sector or realm, or test a new claim about the AI records.
---

# The headline findings

```sh
uv run tools/build_db.py && uv run tools/findings.py
```

That prints the four findings from the `ai_labels` table, which is `labels/ai-records.csv`: 3,863
records where two separate readings found AI in use. Read `labels/README.md` before going further.
It says how the labels were made and what they cannot show, and `labels/rubric.md` is the exact
rule the labeller was given.

## Breaking a finding down

Join `ai_labels` to `entries` and `labels` on `id`. List columns (`task`, `threat`, `taxon`, `users`,
`method`) hold several codes separated by spaces, so match with `' ' || taxon || ' ' like '% birds %'`.

```sql
-- how far outputs get, for ocean work only
select a.chain, count(*) from ai_labels a join labels l on l.id = a.id
where l.field = 'realms' and l.value = 'ocean' group by 1 order by 2 desc;
```

## Testing a new claim

1. Write down the claim and how you will count it before you look at the result.
2. Count it, with the base stated. Under about 50 records in a group, give counts and no percentages.
3. Try to break it: count it a second way (a different field, facts text as well as labels), and read
   ten of the records behind it, opening the quoted pages.
4. Report what held and what did not. Four of the first ten conclusions drawn from this database
   failed a second check, mostly because a pattern came from which organisations publish lists
   online, and not from what they do.

Do not use these labels to say what share of all organisations use AI. The set was built to be
conservative and leaves out records that only one reading called AI.
