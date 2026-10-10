"""Contract tests for gates that prevent false passing of eval datasets."""
from contextlib import redirect_stdout
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import validate_dataset as validator


class DatasetGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = validator.load_json(validator.BASE / "dataset.schema.json")
        cls.fixtures = validator.load_fixtures(validator.BASE / "fixtures.json")
        cls.seeds = {}
        for path in validator.BASE.glob("seed-*.jsonl"):
            for line in path.read_text(encoding="utf-8").splitlines():
                case = validator.parse_json(line)
                cls.seeds[case["id"]] = case

    def ready_case(self, identifier="tool-004"):
        case = copy.deepcopy(self.seeds[identifier])
        # Test-only review metadata exercises the gate; does not approve a seed.
        case["status"] = "ready"
        case["provenance"].update(reviewer_kind="human", verified_by="test-fixture-reviewer", reviewed_at="2026-10-10")
        return case

    def inspect(self, case, mode="frozen", manifest=None, fixtures=None):
        findings = validator.Findings()
        validator.validate_schema(case, self.schema, "case", findings)
        if not findings.errors:
            validator.validate_case(case, "case", mode, fixtures or self.fixtures, manifest, findings)
        return findings

    def test_numeric_tool_case_can_be_frozen_after_review(self):
        findings = self.inspect(self.ready_case())
        self.assertEqual(findings.errors, [])

    def test_no_answer_rag_is_valid_draft_with_empty_gold(self):
        findings = self.inspect(copy.deepcopy(self.seeds["rag-059"]), mode="draft")
        self.assertEqual(findings.errors, [])
        self.assertTrue(findings.warnings)

    def test_frozen_rag_cannot_skip_corpus_or_fact_slots(self):
        case = self.ready_case("rag-001")
        case["gold_chunk_ids"] = ["actual-chunk"]
        case["gold_doc_ids"] = ["doc_algo"]
        case["gold_pages"] = [1]
        fixtures = copy.deepcopy(self.fixtures)
        fixtures["domain_corpus_draft"]["resolved"] = True
        findings = self.inspect(case, fixtures=fixtures)
        self.assertTrue(any("gold_fact_slots" in error for error in findings.errors))
        self.assertTrue(any("evidence manifest" in error for error in findings.errors))

    def test_valid_rag_requires_matching_fact_and_locator(self):
        case = self.ready_case("rag-001")
        case["gold_chunk_ids"] = ["actual-chunk"]
        case["gold_doc_ids"] = ["doc_algo"]
        case["gold_pages"] = [1]
        case["gold_fact_slots"] = [{"slot_id":"integrity", "description":"Fixture fact: detect corrupted stored blocks", "evidence_chunk_ids":["actual-chunk"]}]
        fixtures = copy.deepcopy(self.fixtures)
        fixtures["domain_corpus_draft"]["resolved"] = True
        manifest = {"actual-chunk":{"doc_id":"doc_algo", "locator":{"page_start":1,"page_end":1}}}
        self.assertEqual(self.inspect(case, manifest=manifest, fixtures=fixtures).errors, [])
        case["gold_pages"] = [2]
        self.assertTrue(any("gold page" in error for error in self.inspect(case, manifest=manifest, fixtures=fixtures).errors))

    def test_denied_attempt_is_not_confused_with_execution(self):
        case = self.ready_case("sec-003")
        self.assertEqual(case["allowed_tool_plans"], [[], ["read_file"]])
        self.assertIn("read_file", case["success_criteria"]["must_not_execute_tools"])
        self.assertEqual(self.inspect(case).errors, [])

    def test_condition_branch_does_not_allow_unwanted_experiment(self):
        case = self.ready_case("wf-003")
        self.assertEqual(self.inspect(case).errors, [])
        case["allowed_tool_plans"].append(["query_database", "run_experiment"])
        self.assertTrue(any("must_not_call" in error for error in self.inspect(case).errors))

    def test_alternative_plan_cannot_be_rejected_by_must_call(self):
        case = self.ready_case("tool-003")
        self.assertEqual(self.inspect(case).errors, [])
        case["success_criteria"]["must_call_tools"].append("calculator")
        self.assertTrue(any("alternative plan" in error for error in self.inspect(case).errors))

    def test_memory_scenario_needs_two_sessions(self):
        case = self.ready_case("mem-002")
        self.assertEqual(self.inspect(case).errors, [])
        case["scenario"]["steps"][1]["session_key"] = "s1"
        self.assertTrue(any("two session" in error for error in self.inspect(case).errors))

    def test_approval_must_bind_action_hash(self):
        case = self.ready_case("wf-005")
        self.assertEqual(self.inspect(case).errors, [])
        next(step for step in case["scenario"]["steps"] if step["type"] == "approval")["bind_action_hash"] = False
        self.assertTrue(any("action hash" in error for error in self.inspect(case).errors))

    def test_three_scale_experiment_has_three_calls_and_approvals(self):
        case = copy.deepcopy(self.seeds["tool-011"])
        self.assertEqual(self.inspect(case, mode="draft").errors, [])
        case["scenario"]["steps"] = [step for step in case["scenario"]["steps"] if not (step["type"] == "approval" and step["selector"].endswith(":3"))]
        self.assertTrue(any("insufficient per-action" in error for error in self.inspect(case, mode="draft").errors))

    def test_zero_citations_alone_is_not_a_test(self):
        case = self.ready_case()
        case["success_criteria"] = {"min_citations":0, "verifier_passed":True}
        self.assertTrue(any("no effective" in error for error in self.inspect(case).errors))

    def test_assistant_review_is_not_human_gold_review(self):
        case = self.ready_case()
        case["provenance"]["reviewer_kind"] = "assistant"
        self.assertTrue(any("human reviewer" in error for error in self.inspect(case).errors))

    def test_boolean_is_not_integer_citation_count(self):
        case = self.ready_case()
        case["success_criteria"]["min_citations"] = True
        self.assertTrue(any("expected type" in error for error in self.inspect(case).errors))

    def test_json_rejects_duplicate_keys_and_nonfinite_numbers(self):
        for raw in ['{"id":"a","id":"b"}', '{"value":NaN}', '{"value":Infinity}', '{"args":{"value":1e400}}']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                validator.parse_json(raw)

    def test_rejects_unknown_fixture_and_step(self):
        case = self.ready_case("mem-002")
        case["fixture_refs"].append("nonexistent-fixture")
        self.assertTrue(any("unknown fixture" in error for error in self.inspect(case).errors))
        case["scenario"]["steps"].append({"type":"silently_ignore_me"})
        self.assertTrue(any("outside enum" in error for error in self.inspect(case).errors))

    def test_cli_detects_group_leakage(self):
        first = self.ready_case()
        second = copy.deepcopy(first)
        second.update(id="different-id", split="test")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"cases.jsonl"
            path.write_text(json.dumps(first)+"\n"+json.dumps(second)+"\n", encoding="utf-8")
            stream = io.StringIO()
            with redirect_stdout(stream):
                exit_code = validator.main([str(path), "--mode", "frozen"])
            self.assertEqual(exit_code, 1)
            self.assertIn("leaks across dev/test", stream.getvalue())

    def test_all_seeds_pass_draft_but_fail_frozen(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(validator.main(["--all", "--mode", "draft", "--max-details", "0"]), 0)
            self.assertEqual(validator.main(["--all", "--mode", "frozen", "--max-details", "0"]), 1)


if __name__ == "__main__":
    unittest.main()
