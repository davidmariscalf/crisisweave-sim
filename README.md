# crisisweave-sim

Deterministic synthetic crisis-event generator for testing the CrisisWeave pipeline without depending on live disasters or unstable external APIs.

## Why a simulator matters

A crisis tool that is only tested during real incidents is not testable enough. This repository generates controlled duplicate reports, source disagreement, missing coordinates and timing jitter so ingestion, verification, mapping, offline caching and alert rules can be exercised repeatedly.

## Run

```bash
python simulate.py --scenario flood --count 20 --seed 42 > events.jsonl
python simulate.py --scenario wildfire --count 20 --seed 42 > events.jsonl
python simulate.py --scenario earthquake --count 20 --seed 42 > events.jsonl
```

Use `--scenario mixed` to interleave all three.

Generated events already follow the CrisisWeave event contract. Some are deliberately incomplete or low-confidence so downstream modules can be tested against realistic imperfections.

## Important

Everything emitted here is synthetic. Do not publish simulator output into real emergency feeds without an explicit test label.
