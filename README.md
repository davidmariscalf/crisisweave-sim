# crisisweave-sim

**Generate realistic, deterministic crisis-event streams in seconds — without calling a live emergency API.**

`crisisweave-sim` creates synthetic flood, wildfire and earthquake reports for testing ingestion, deduplication, mapping, alerting and offline crisis tooling. The same seed always produces the same data, so bugs and evaluations are reproducible.

> Every record is explicitly synthetic. This is test data, not an emergency feed.

## 60-second demo

Requires Python 3.10+ and no third-party packages.

```bash
python simulate.py --scenario flood --count 20 --seed 42 > events.jsonl
head -n 2 events.jsonl
```

Other scenarios:

```bash
python simulate.py --scenario wildfire --count 20 --seed 42 > events.jsonl
python simulate.py --scenario earthquake --count 20 --seed 42 > events.jsonl
python simulate.py --scenario mixed --count 60 --seed 42 > events.jsonl
```

## What it deliberately generates

The generator includes imperfections that downstream systems need to survive:

- multiple independent source types
- official and non-official reports
- duplicate/near-duplicate incident descriptions
- source disagreement
- timing jitter and stale outliers
- missing coordinates
- varying confidence and severity
- a minority of unrelated geographic outliers

That makes it useful for regression tests, demos, benchmarks and failure-mode testing — not just happy-path screenshots.

## Example uses

```bash
# Create a fixed regression fixture
python simulate.py --scenario mixed --count 100 --seed 7 > fixture.jsonl

# Re-run exactly the same fixture later
python simulate.py --scenario mixed --count 100 --seed 7 > fixture-again.jsonl
```

A practical pairing is **crisisweave-sim → crisisweave-verify**: generate noisy reports here, then test whether the verifier clusters likely duplicates while preserving provenance.

## Output contract

Each line is a JSON object containing fields such as:

- event ID and kind
- title and synthetic description
- observation time
- severity and confidence
- official/non-official source flag
- optional GeoJSON point
- source metadata
- evidence metadata
- explicit `synthetic: true` and `environment: "simulation"` markers

The output is already compatible with the public CrisisWeave event contract.

## Reproducibility

`--seed` controls all random choices. Given the same scenario, count and seed, the output is deterministic. This makes failures easy to reproduce in CI and local debugging.

The CLI rejects counts outside `1..100000`.

## Part of CrisisWeave

This repository is a small standalone component of [CrisisWeave](https://github.com/davidmariscalf/CrisisWeave), a public-beta project for provenance-preserving crisis information and recovery coordination.

Related repositories:

- [crisisweave-verify](https://github.com/davidmariscalf/crisisweave-verify) — deduplication and confidence aggregation
- [crisisweave-map](https://github.com/davidmariscalf/crisisweave-map) — browser interfaces for incident and recovery views

## Safety

Everything emitted here is synthetic. Do not publish simulator output into real emergency feeds without an explicit test label, and do not use this project as a source of real-world emergency information.
