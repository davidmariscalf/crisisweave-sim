import itertools
import unittest

from simulate import MAX_COUNT, SCENARIOS, generate


class SimulationTests(unittest.TestCase):
    def test_all_scenarios_are_unmistakably_synthetic(self):
        for scenario in [*SCENARIOS, "mixed"]:
            with self.subTest(scenario=scenario):
                events = generate(scenario, 9 if scenario == "mixed" else 3, 42)
                for event in events:
                    self.assertIs(event["synthetic"], True)
                    self.assertEqual(event["environment"], "simulation")
                    self.assertIs(event["raw"]["synthetic"], True)
                    self.assertIn("synthetic", event["tags"])
                    self.assertTrue(event["source"]["name"].startswith("Synthetic "))
                    self.assertTrue(event["source"]["source_id"].startswith("SIM-"))
                    self.assertIsNone(event["source"]["url"])
                    self.assertIn("not a real emergency", event["description"])

    def test_generation_is_deterministic_for_same_seed(self):
        self.assertEqual(generate("mixed", 12, 1234), generate("mixed", 12, 1234))

    def test_different_seed_changes_output(self):
        self.assertNotEqual(generate("mixed", 12, 1), generate("mixed", 12, 2))

    def test_count_bounds_are_enforced(self):
        for count in (0, -1, MAX_COUNT + 1):
            with self.subTest(count=count), self.assertRaises(ValueError):
                generate("flood", count, 1)

    def test_unknown_scenario_is_rejected(self):
        with self.assertRaises(ValueError):
            generate("not-a-scenario", 1, 1)

    def test_mixed_distribution_includes_each_scenario(self):
        events = generate("mixed", len(SCENARIOS) * 3, 42)
        self.assertEqual({e["kind"] for e in events}, set(SCENARIOS))


if __name__ == "__main__":
    unittest.main()
