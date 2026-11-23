# /// script
# requires-python = ">=3.11"
# ///
"""Print the headline findings from build/lichen.sqlite (run tools/build_db.py first).

Usage: uv run tools/findings.py
Every figure is a share of the AI records in labels/ai-records.csv: records whose pages show AI in use
according to two separate readings. labels/README.md says how the labels were made and what they cannot show.
"""
import sqlite3
from collections import Counter
from pathlib import Path

con = sqlite3.connect(Path(__file__).resolve().parent.parent / "build/lichen.sqlite")
rows = [dict(zip([c[1] for c in con.execute("pragma table_info(ai_labels)")], r)) for r in con.execute("select * from ai_labels")]
n = len(rows)
pct = lambda a, b: f"{100 * a / b:5.1f}%"


def table(title, counts, base, order=None):
    print(f"\n{title} (of {base:,})")
    for k in order or [k for k, _ in counts.most_common()]:
        print(f"  {k:<22}{counts[k]:>6,}  {pct(counts[k], base)}")


print(f"AI records: {n:,}")
chain = Counter(r["chain"] for r in rows)
table("1. Furthest step the public evidence shows", chain, n, ["observe", "assess", "predict", "decide", "act", "none"])
print(f"  observe or assess: {pct(chain['observe'] + chain['assess'], n)};  decide or act: {pct(chain['decide'] + chain['act'], n)}")

GROUPS = ["mammals", "plants", "birds", "fish", "other-invertebrates", "insects", "reptiles", "amphibians", "fungi"]
taxa = Counter(t for r in rows for t in r["taxon"].split() if t in GROUPS)
table("2. Species groups named (a record can name up to three)", taxa, sum(taxa.values()))
print(f"  mammals and birds together: {pct(taxa['mammals'] + taxa['birds'], sum(taxa.values()))}")

named = [r for r in rows if set(r["threat"].split()) - {"none-specific"}]
print(f"\n3. Records naming no threat to nature: {n - len(named):,} of {n:,} ({pct(n - len(named), n).strip()})")
table("   Threats named (a record can name two, so shares sum to more than 100%)",
      Counter(t for r in named for t in r["threat"].split() if t != "none-specific"), len(named))

print("\n4. Stage of the work, by sector of the organisation (organisations only)")
STAGES = ["research", "pilot", "operational", "product", "unclear"]
print(f"  {'':<12}{'n':>6}" + "".join(f"{s:>13}" for s in STAGES))
for s in ["academic", "company", "government", "ngo"]:
    g = [r for r in rows if r["kind"] == "organisation" and r["sector"] == s]
    c = Counter(r["stage"] for r in g)
    print(f"  {s:<12}{len(g):>6}" + "".join(f"{pct(c[x], len(g)):>13}" for x in STAGES))
