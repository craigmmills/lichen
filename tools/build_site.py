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
import collections, csv, html, json, shutil
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
    "lede": "Find your organisation, check what it says, and tell me if it is wrong or missing.",
    "address": "giarcsllim+lichen@gmail.com",
    "repo": "https://github.com/craigmmills/lichen",
    "site": "https://craigmmills.github.io/lichen/",
    "description": "18,407 organisations, projects, datasets and models in 207 countries. Find yours, check it, and fix it if it is wrong.",
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
page = page.replace("{{records}}", f"{len(E):,}")
for k in ("title", "site", "description", "lede"):
    page = page.replace("{{" + k + "}}", html.escape(CONFIG[k], quote=True))
(OUT / "index.html").write_text(page)

# The link preview image: one mark per record, in bands by kind. build/og.html is turned into
# tools/og.png with a browser at 1200 by 627 (see the README of this folder), then copied to docs/.
kinds = collections.Counter(e["kind"] for e in E)
COL = {"organisation": "#262a2b", "project": "#4e5a63", "programme": "#64796f", "dataset": "#7c7d52", "model": "#d3aa3f"}
P, COLS, X0, Y0 = 3.7, 140, 642, 62
marks, n = [], 0
for k in KINDS:
    d = "".join(f"M{X0 + (i % COLS) * P:.1f} {Y0 + (i // COLS) * P:.1f}h2.6v2.6h-2.6z" for i in range(n, n + kinds[k]))
    marks.append(f'<path d="{d}" fill="{COL[k]}"/>'); n += kinds[k]
legend = "".join(f'<span><i style="background:{COL[k]}"></i>{kinds[k]:,} {k}s</span>' for k in KINDS)
og = (ROOT / "tools/og_template.html").read_text().replace("{{marks}}", "".join(marks)).replace("{{legend}}", legend)
og = og.replace("{{records}}", f"{len(E):,}").replace("{{countries}}", str(stats["countries"])).replace("{{facts}}", f"{facts:,}")
(ROOT / "build").mkdir(exist_ok=True)
(ROOT / "build/og.html").write_text(og)
if (ROOT / "tools/og.png").exists():
    shutil.copy(ROOT / "tools/og.png", OUT / "og.png")
size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"site: {len(E)} records, {facts} facts, {len(hosts)} websites, {len(detail)} data files, {size / 1e6:.1f} MB in docs/")
