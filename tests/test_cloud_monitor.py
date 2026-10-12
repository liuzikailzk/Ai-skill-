import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import cloud_monitor as monitor
import skill_sync as sync


class CloudMonitorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "registry").mkdir()
        sync.write_json(self.root / "registry/latest.json", {
            "schema": 1, "skills": {n: {"history": []} for n in sync.NAMES}})
        self.fingerprint = patch.object(monitor, "tree_fingerprint", return_value={"registry": "a", "tools": "b"})
        self.fingerprint.start()
        self.addCleanup(self.fingerprint.stop)

    def test_no_real_files_never_reports_success(self):
        report = monitor.audit(self.root)
        self.assertEqual(report["overall_status"], "blocked_source_connection")
        self.assertEqual(report["repository_integrity"], "awaiting_real_skill_files")
        self.assertEqual(report["verified_snapshots"], 0)

    def test_verified_repository_still_does_not_prove_chat_save(self):
        with patch.object(sync, "verify", return_value=({}, 3)):
            report = monitor.audit(self.root)
        self.assertEqual(report["repository_integrity"], "verified")
        self.assertEqual(report["maintenance_save_success"], "unverified")
        self.assertEqual(report["automatic_maintenance_repair"], "not_available")

    def test_integrity_failure_gets_explicit_report(self):
        with patch.object(sync, "verify", side_effect=ValueError("missing file")):
            report = monitor.audit(self.root)
        self.assertEqual(report["overall_status"], "repository_integrity_failed")
        self.assertIn("missing file", monitor.markdown(report))

    def test_unchanged_verified_tree_avoids_full_reads(self):
        previous = {"schema": 1, "audit_tree": {"registry": "a", "tools": "b"},
                    "repository_integrity": "verified", "verified_snapshots": 3}
        with patch.object(sync, "verify") as verify:
            report = monitor.audit(self.root, previous)
            verify.assert_not_called()
        self.assertEqual(report["verified_snapshots"], 3)
        self.assertEqual(report["overall_status"], "blocked_source_connection")

    def test_changed_tree_rechecks_files(self):
        previous = {"schema": 1, "audit_tree": {"registry": "old", "tools": "b"},
                    "repository_integrity": "verified", "verified_snapshots": 3}
        with patch.object(sync, "verify", return_value=({}, 0)) as verify:
            monitor.audit(self.root, previous)
            verify.assert_called_once_with(self.root)

    def test_malformed_manifest_produces_failure_report(self):
        (self.root / "registry/latest.json").write_text("not json")
        self.assertEqual(monitor.audit(self.root)["repository_integrity"], "failed")


if __name__ == "__main__":
    unittest.main()
