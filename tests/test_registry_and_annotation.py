import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from annotation.prepare_packets import build
from tools.cr07_batch_registry import inspect_batch


BASE_REGISTRY = {
    "schema_version": "CR07-CUMULATIVE-REGISTRY-1",
    "project": "CUBE-REV",
    "protocol_version": "0.7.11",
    "clock": {"state": "NOT_STARTED", "activated_at": None, "authorization_id": None},
    "batches": [],
    "sessions": {},
}


class RegistryTests(unittest.TestCase):
    def make_zip(self, directory, name, sessions):
        target = Path(directory) / name
        with zipfile.ZipFile(target, "w") as archive:
            for index, session in enumerate(sessions):
                archive.writestr(f"session-{index}.json", json.dumps(session))
        return target

    def test_cumulative_deduplication(self):
        with tempfile.TemporaryDirectory() as directory:
            session = {
                "project": "CUBE-REV",
                "version": "0.6.11",
                "session_id": "CR-TEST-001",
                "trials": [],
            }
            first_zip = self.make_zip(directory, "CR07-BATCH-001.zip", [session, session])
            report, updated = inspect_batch(first_zip, BASE_REGISTRY)
            self.assertEqual(report["status"], "accepted")
            self.assertEqual(report["accepted_sessions"], ["CR-TEST-001"])
            self.assertEqual(report["duplicate_sessions"], ["CR-TEST-001"])
            self.assertEqual(updated["clock"]["state"], "NOT_STARTED")
            again, no_update = inspect_batch(first_zip, updated)
            self.assertEqual(again["status"], "duplicate_batch")
            self.assertIsNone(no_update)

    def test_conflicting_session_id_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            first = {"project": "CUBE-REV", "session_id": "CR-X", "trials": []}
            second = {"project": "CUBE-REV", "session_id": "CR-X", "trials": [{"x": 1}]}
            zip_a = self.make_zip(directory, "a.zip", [first])
            _, registry = inspect_batch(zip_a, BASE_REGISTRY)
            zip_b = self.make_zip(directory, "b.zip", [second])
            report, update = inspect_batch(zip_b, registry)
            self.assertEqual(report["status"], "conflict")
            self.assertIsNone(update)

    def test_two_pass_packets_are_separate(self):
        session = {
            "session_id": "CR-TEST",
            "trials": [{
                "trial_id": "T1",
                "condition": "same_endpoint_history",
                "accepted_moves": [{"move": "R"}],
                "calibration_assignment": {"memory": {"history_visibility": "shown"}},
            }],
        }
        pass_a, pass_b = build(session)
        self.assertNotIn("context", pass_a[0])
        self.assertTrue(pass_a[0]["blinding"]["condition_hidden"])
        self.assertEqual(pass_b[0]["pass_a_reference"]["packet_id"], pass_a[0]["packet_id"])
        self.assertTrue(pass_b[0]["requires_completed_pass_a"])


if __name__ == "__main__":
    unittest.main()
