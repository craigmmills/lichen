---
name: lichen-counts
description: Count, compare or list records in the lichen database of data and AI for nature (organisations, projects, programmes, datasets, models in 207 countries). Use when asked how many, which, what share, top countries or sectors, who funds or uses what, or to check a claim against lichen.
---

# Counting from lichen

## Set up (once per session)

```sh
uv run tools/build_db.py      # writes build/lichen.sqlite from entries/, about 30 seconds
```

Then query with `sqlite3 build/lichen.sqlite` or Python's `sqlite3`. The tables and columns are listed
at the top of `tools/build_db.py`. Allowed values for each label are in the README's field table.

## Rules for any count you report

1. State the base. "Of 10,557 organisations" or "of the 3,863 AI records", never a bare percentage.
2. Records overlap by design. A project and the organisation that runs it are separate records, so
   count one `kind` at a time unless the question is about records in general.
3. Every count is a floor. The database holds what organisations publish on pages the searches reached.
   Say "at least" or "about", and never write "none" or "only one" from a search.
4. For "how many do X" questions, search the facts as well as the summaries, and search named tools as
   well as generic words. A keyword count from summaries alone has been wrong by a factor of two or more.
5. `ai_label = 'none'` means the pages read showed no technology. It does not mean there is none.
6. Do not report what share of all organisations use AI. The labels here are a first pass and that
   figure has not been checked. Shares within the AI records (`ai_labels` table) are fine.
7. Give examples with every count: three to five record names and their files, so a reader can check.
8. About 1,200 links point to a name that has no record yet. Join `links` to `entries` on both ends
   to keep only links between records.
9. For anything you will publish, open the quoted pages of the records behind the claim. Pages change,
   and in blind samples about one record in ten had a fault.

## Recipes

```sql
-- organisations by sector
select sector, count(*) from entries where kind = 'organisation' group by 1 order by 2 desc;

-- records per country, with the place name left as a code (names are in tools/places.tsv)
select scope, count(*) from entries group by 1 order by 2 desc limit 20;

-- bodies that manage or regulate a named place, by country
select e.scope, count(*) from entries e join labels l on l.id = e.id
where l.field = 'roles' and l.value = 'governs' group by 1 order by 2 desc;

-- who is recorded as using a tool (links are stored as "tool used-by user")
select e.name, e.scope from links l join entries e on e.id = l.target
where l.source = 'earthranger' and l.type = 'used-by' order by 1;

-- who funds whom
select s.name as funder, t.name as funded, l.url from links l
join entries s on s.id = l.source join entries t on t.id = l.target where l.type = 'funds' limit 50;

-- a topic, searching facts as well as summaries (rule 4)
select distinct e.id, e.name, e.scope from entries e left join facts f on f.id = e.id
where e.summary like '%camera trap%' or f.claim like '%camera trap%' or f.quote like '%camera trap%';

-- stage of AI work by sector, from the labelled AI records
select sector, stage, count(*) from ai_labels where kind = 'organisation' group by 1, 2 order by 1, 3 desc;
```

## Reporting

Lead with the answer and its base. Then the examples. Then one or two sentences on what the count
cannot show, chosen from the rules above for this question. Keep SQL in the answer so it can be rerun.
