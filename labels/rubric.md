You are labelling entries from a map of who builds, funds, governs or uses AI for nature (biodiversity,
ecosystems, land, fresh water, ocean). Each entry has a name, a kind, a country and a list of facts, each a claim
with a quote from a public page. Label each entry from its evidence only. Do not use outside knowledge about the
organisation, and do not guess: when the evidence does not say, use the "unclear" or "none" code.

Return one JSON object per entry with exactly these keys. Where a field allows several codes, give a list.

"id": the entry id, copied exactly.

"ai": one code. Does the evidence show this entry itself using artificial intelligence or machine learning
(any statistical learning method, from random forests to deep learning and language models)?
  "built"     it develops, trains or adapts AI models or AI tools itself (alone or as a named partner in building).
  "used"      it applies AI in its work but the evidence does not show it building the model or tool.
  "planned"   it has announced or begun a pilot, grant or plan to use AI, with no use shown yet.
  "supports"  it does not use AI itself but funds, governs, convenes, teaches or supplies data for AI by others.
  "none"      no AI or machine learning appears in the evidence.

The next three fields describe the technology, model or data work in the evidence, whether or not AI is named.
Use the "none" code only when the entry does no such work itself (for example a funder, a policy body or a network).

"stage": one code for how far the work has got.
  "research"     papers, theses, prototypes, benchmarks or experiments.
  "pilot"        a trial at one or a few sites, or a tool announced as under test.
  "operational"  in routine use for monitoring, management, enforcement or reporting, or run as a standing service.
  "product"      sold, licensed or offered to others as a product or platform.
  "unclear"
  "none"

"task": up to two codes for what the technology or analysis does.
  "identify-species"   recognises species or individuals in images, sound or DNA.
  "count-populations"  counts or estimates numbers of animals or plants.
  "map-habitat"        maps land cover, habitat, vegetation, water or ecosystem extent and condition.
  "detect-threat"      detects or alerts on harm or illegal activity (deforestation, fire, poaching, illegal fishing, logging).
  "predict"            forecasts or models distribution, risk, movement or future change.
  "plan"               recommends, prioritises or optimises actions (where to protect, patrol, restore or invest).
  "text"               reads, searches, summarises or answers questions over documents or data in words (assistants, chatbots).
  "collect-data"       gathers, hosts or publishes data, or tracks animals, with no automated analysis shown.
  "other"
  "none"

"chain": one code, the furthest step along this chain that the evidence shows the output reaching.
  "observe"   turns raw data into records (a species name, a land cover class, a detection). No use beyond that is shown.
  "assess"    the records are combined into a stated status, trend, indicator, map product or report.
  "predict"   used to forecast or to model what is not directly observed.
  "decide"    the evidence says the output feeds a named decision, plan, permit, policy, investment or priority list.
  "act"       the evidence says it triggered or guided action on the ground (a patrol sent, an arrest, a fire fought, a
              vessel inspected, a turbine stopped, animals moved, a site restored).
  "none"      the entry does no such work itself.

"threat": up to two codes for the pressure on nature the work is aimed at.
  "land-use-change"  deforestation, habitat loss or degradation, conversion to farming, mining, building.
  "exploitation"     poaching, hunting, wildlife trade, overfishing or illegal fishing, illegal logging, bycatch.
  "climate"          climate change effects (warming, bleaching, drought, sea level), or carbon stocks.
  "pollution"        water, air, soil, plastic, noise, light or nutrient pollution.
  "invasives"        invasive or pest species.
  "fire"             wildfire.
  "conflict"         human-wildlife conflict, collisions with roads, ships, turbines or power lines.
  "disease"          wildlife or plant disease.
  "none-specific"    general monitoring, inventory or research with no named pressure.

"taxon": up to three codes for the living things the work is about.
  "mammals", "birds", "fish", "reptiles", "amphibians", "insects", "other-invertebrates" (corals, molluscs,
  crustaceans, plankton), "plants" (named plant species, trees as species, forest inventory by species),
  "fungi", "microbes",
  "habitat"  land cover, forest extent, vegetation, water or whole ecosystems with no named group of species,
  "many"     biodiversity in general across many groups,
  "none"     not about living things (for example funding or policy in general).

"users": up to two codes for who the evidence says uses the output.
  "researchers", "managers" (conservation NGOs, park and reserve staff, rangers), "government" (agencies,
  regulators, enforcement, national reporting), "business" (companies, investors, supply chains, credits),
  "communities" (Indigenous peoples, local communities, farmers, fishers), "public" (citizen scientists,
  the general public), "unclear".

"outcome": "yes" only if a fact reports a concrete result beyond the technology working: a decision taken, a law or
  plan changed, an enforcement action, an area protected or restored, harm avoided, a population change. Accuracy
  figures, numbers of images processed, users, downloads, awards and funding raised are not outcomes. Else "no".
"outcome_quote": if outcome is "yes", the words from the evidence that show it, at most 25 words. Else "".

"ai_type": list. "classical-ml" (random forest, SVM, regression-type learners, Maxent), "deep-learning" (neural
  networks, CNNs), "foundation-model" (large pre-trained models adapted to tasks), "llm" (large language models,
  chatbots), "generative", "agentic", "unspecified" (AI or machine learning with the kind not stated), "none".

"method": list of the data the work rests on. "satellite-aerial" (satellites, aircraft, drones, lidar, radar),
  "camera" (camera traps, underwater video, photographs, microscopes), "sound", "dna" (eDNA, genomics, barcoding),
  "tracking-sensors" (tags, collars, GPS, vessel tracking, in-place sensors), "text" (documents, reports, literature),
  "field-records" (occurrence records, surveys, citizen observations, specimens), "other", "none".

"roles": list, what the entry does on the evidence. "builds-ai", "uses-ai", "supplies-data" (collects, hosts or
  publishes nature data others use), "governs" (regulates, sets policy, manages land or sea by mandate), "funds",
  "convenes" (networks, standards, conferences, training), "other".

"open": "yes" if the evidence says its tool, model or data is open source, open access or free to use; "no" if it
  says closed, licensed or paid; else "unclear".

Rules:
- Judge the entry, not its partners. If a fact describes AI built by someone else that this entry only funds, that is "supports".
- A university listed because one paper used machine learning is "built" at stage "research" if the authors trained
  the model, and "used" if they applied an existing one.
- Choose the most specific code. Use "other" and "unclear" only when nothing fits.
- Output a JSON array only, one object per entry, in the order given, with no commentary and no code fence.
