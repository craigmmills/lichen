# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Build the record explorer in docs/ (served by GitHub Pages) from entries/.

Usage: uv run tools/build_site.py
Writes docs/index.html, docs/data/index.json (one slim row per record) and docs/data/s/<letter>.json
(summary, quoted facts and links, fetched when a record is opened). The page wording and the address
that corrections go to are in the CONFIG block below.
"""
import collections, csv, json, shutil
from datetime import date
from pathlib import Path
import yaml

try:
    Loader = yaml.CSafeLoader
except AttributeError:
    Loader = yaml.SafeLoader

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
CONFIG = {
    "title": "Who works on data and AI for nature",
    "lede": "Every record is built from public web pages, and every fact quotes the page it came from. "
            "Find your organisation, check what it says, and tell me if it is wrong or missing.",
    "address": "giarcsllim+lichen@gmail.com",
    "repo": "https://github.com/craigmmills/lichen",
}
KINDS = ["organisation", "project", "programme", "dataset", "model"]
SECTORS = ["government", "ngo", "academic", "company", "community", "funder", "multilateral"]
ROLES = ["builds-ai", "uses-ai", "supplies-data", "governs", "funds", "convenes"]
LABELS = ["ai", "conservation-tech", "data-infrastructure", "none"]

names = {r["code"]: r["name"] for r in csv.DictReader((ROOT / "tools/places.tsv").open(), delimiter="\t")}
names["global"] = "Global"
E = [yaml.load(f.read_text(), Loader=Loader) for f in sorted((ROOT / "entries").glob("*/*.yaml"))]
by_id = {e["id"]: e for e in E}
mask = lambda vals, vocab: sum(1 << vocab.index(v) for v in (vals or []) if v in vocab)

rows, detail, facts, hosts = [], collections.defaultdict(dict), 0, set()
for e in sorted(E, key=lambda e: e["name"].lower()):
    rows.append([e["id"], e["name"], KINDS.index(e["kind"]), e["scope"],
                 SECTORS.index(e["sector"]) if e.get("sector") in SECTORS else -1, mask(e.get("roles"), ROLES),
                 LABELS.index(e["ai_label"]) if e.get("ai_label") in LABELS else 3, " ".join(e.get("also_known_as") or [])])
    fs = [[str(f.get(k, "")) for k in ("claim", "url", "quote", "fetched")] for f in e.get("facts") or []]
    facts += len(fs)
    hosts.update(f[1].split("/")[2].removeprefix("www.") for f in fs if f[1].count("/") >= 2)
    ls = [[l["type"], l["to"], by_id[l["to"]]["name"]] for l in e.get("links") or [] if l.get("to") in by_id]
    detail[e["id"][0]][e["id"]] = [e.get("summary", ""), e.get("website") or "", fs, ls]

if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "data/s").mkdir(parents=True)
dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
(OUT / "data/index.json").write_text(dump(rows))
for key, d in detail.items():
    (OUT / f"data/s/{key}.json").write_text(dump(d))
(OUT / ".nojekyll").write_text("")
shutil.copytree(ROOT / "tools/fonts", OUT / "fonts")

scopes = collections.Counter(e["scope"] for e in E)
stats = {"built": date.today().isoformat(), "records": len(E), "countries": len(scopes) - ("global" in scopes),
         "facts": facts, "sites": len(hosts),
         "scopes": sorted([[s, names.get(s, s), n] for s, n in scopes.items()], key=lambda r: (r[0] != "global", r[1]))}
page = (ROOT / "tools/site_template.html").read_text()
page = page.replace("/*CONFIG*/{}", dump(CONFIG).replace("</", "<\\/")).replace("/*STATS*/{}", dump(stats).replace("</", "<\\/"))
(OUT / "index.html").write_text(page.replace("{{title}}", CONFIG["title"]))
size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"site: {len(E)} records, {facts} facts, {len(hosts)} websites, {len(detail)} data files, {size / 1e6:.1f} MB in docs/")
