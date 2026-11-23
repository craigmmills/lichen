# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Build build/lichen.sqlite from entries/ so the records can be counted with SQL.

Usage: uv run tools/build_db.py
Tables:
  entries(id, kind, name, scope, sector, ai_label, scale, status, hq, website, summary, n_facts, file)
  facts(id, claim, url, fetched, quote)            one row per quoted fact
  links(source, target, type, url, quote)          one row per relationship between two records
  labels(id, field, value)                         list fields, one row per value:
                                                   roles, realms, techniques, ai_types, countries, also_known_as, found_by
  ai_labels(...)                                   labels/ai-records.csv, if present (see labels/README.md)
Links are stored in one direction. A file may say "A run-by B"; the table holds "B runs A". The inverse
forms turned round are: uses -> used-by, run-by -> runs, led-by -> leads, funded-by -> funds,
built-by -> builds, represented-by -> represents.
"""
import csv, sqlite3
from pathlib import Path
import yaml

try:
    Loader = yaml.CSafeLoader
except AttributeError:
    Loader = yaml.SafeLoader

ROOT = Path(__file__).resolve().parent.parent
INVERSE = {"uses": "used-by", "run-by": "runs", "led-by": "leads", "funded-by": "funds", "built-by": "builds", "represented-by": "represents"}
LISTS = ["roles", "realms", "techniques", "ai_types", "countries", "also_known_as", "found_by"]

out = ROOT / "build/lichen.sqlite"
out.parent.mkdir(exist_ok=True)
out.unlink(missing_ok=True)
con = sqlite3.connect(out)
con.executescript("""
create table entries(id text primary key, kind, name, scope, sector, ai_label, scale, status, hq, website, summary, n_facts int, file);
create table facts(id, claim, url, fetched, quote);
create table links(source, target, type, url, quote);
create table labels(id, field, value);
""")
n = 0
for f in sorted((ROOT / "entries").glob("*/*.yaml")):
    d = yaml.load(f.read_text(), Loader=Loader)
    i, facts = d["id"], d.get("facts") or []
    con.execute("insert into entries values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (i, d["kind"], d["name"], d["scope"], d.get("sector"), d.get("ai_label"), d.get("scale"), d.get("status"),
                 str(d["hq"]) if d.get("hq") else None, d.get("website"), d.get("summary"), len(facts), str(f.relative_to(ROOT))))
    con.executemany("insert into facts values (?,?,?,?,?)", [(i, str(x.get("claim", "")), str(x.get("url", "")), str(x.get("fetched", "")), str(x.get("quote", ""))) for x in facts])
    for l in d.get("links") or []:
        s, t, ty = i, l.get("to"), l.get("type")
        if ty in INVERSE:
            s, t, ty = t, s, INVERSE[ty]
        con.execute("insert into links values (?,?,?,?,?)", (s, t, ty, str(l.get("url", "")), str(l.get("quote", ""))))
    for k in LISTS:
        con.executemany("insert into labels values (?,?,?)", [(i, k, str(v)) for v in d.get(k) or []])
    n += 1
lab = ROOT / "labels/ai-records.csv"
if lab.exists():
    rows = list(csv.reader(lab.open()))
    con.execute(f"create table ai_labels({', '.join(rows[0])})")
    con.executemany(f"insert into ai_labels values ({','.join('?' * len(rows[0]))})", rows[1:])
con.executescript("create index f_id on facts(id); create index l_s on links(source); create index l_t on links(target); create index lab_id on labels(id, field);")
con.commit()
print(f"build/lichen.sqlite: {n} records, {con.execute('select count(*) from facts').fetchone()[0]} facts, "
      f"{con.execute('select count(*) from links').fetchone()[0]} links")
