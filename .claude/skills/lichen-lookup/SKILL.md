---
name: lichen-lookup
description: Find a record in the lichen database and show what it says and where each fact came from. Use when asked about one organisation, project, dataset or model, whether something is in lichen, who it is linked to, or to draft a correction for a record.
---

# Looking up a record

## Find it

`records.csv` has one row per record (file, name, kind, scope, sector, labels, website, summary).
Search it first, by name and by website host, because names vary:

```sh
grep -i "kenya wildlife" records.csv | cut -c1-200
grep -ril "kws.go.ke" entries/ke/ | head          # by website, within a country folder
```

Other names a record goes by are in its `also_known_as` field. If `build/lichen.sqlite` exists:

```sql
select e.file, e.name from entries e left join labels l on l.id = e.id and l.field = 'also_known_as'
where e.name like '%KWS%' or l.value like '%KWS%';
```

An organisation's projects, programmes, datasets and models are separate records linked to it.
Find them with `select * from links where source = '<id>' or target = '<id>'`.

## Show it

Read the YAML file. Report the summary, then each fact as the claim, the quote and the page address
with the date it was read. Do not add anything you know about the organisation from elsewhere: the
point of the database is that every statement traces to a page. If you check a page and it has
changed, say so.

## If it is wrong or missing

Do not edit the files in this copy: changes go through the maintainer so each one is checked against
a public page. Draft an email for the person to send to the address in the README, with:

- subject `[lichen <scope>/<id>] <name>` for a correction, or `[lichen new] <name>` for a new record;
- what is wrong and what it should say;
- a link to a public page that shows it. Without one the change cannot be made.
