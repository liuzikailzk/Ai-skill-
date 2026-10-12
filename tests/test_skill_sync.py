"""All content is synthetic and lives in temporary directories."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_sync", REPO / "tools/skill_sync.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)
NAME = "script-visual-assets"


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        (self.root / "registry").mkdir(parents=True)
        self.initial = {"schema": 1, "channels": {}, "skills": {
            n: {"files": {}, "history": []} for n in sync.NAMES}}
        sync.write_json(self.root / "registry/latest.json", self.initial)
        (self.root / "docs").mkdir()
        (self.root / "docs/production-access.md").write_text("TEST instructions only")
        self.bundle = self.base / "bundle"
        self.bundle.mkdir()
        self.payload = self.bundle / NAME
        (self.payload / "references").mkdir(parents=True)
        (self.payload / "SKILL.md").write_text("TEST ONLY [reference](references/test.md)\n")
        (self.payload / "references/test.md").write_text("TEST RULE A\n")
        (self.payload / "scripts").mkdir()
        (self.payload / "scripts/test.py").write_text("print('TEST ONLY')\n")
        (self.payload / "assets").mkdir()
        (self.payload / "assets/test.bin").write_bytes(bytes(range(256)))
        self.item = {"name": NAME, "weekly_version": "1.0", "revision": "test-r1",
                     "source_updated_at": "2026-10-01T09:00:00+08:00",
                     "parent_content_sha256": None, "files": sync.inventory(self.payload)}
        self.metadata = {"schema": 1, "source": "chatgpt-maintenance", "source_saved": True,
                         "save_evidence": "SYNTHETIC TEST ONLY", "skills": [self.item]}
        self.save()

    def save(self):
        sync.write_json(self.bundle / "release.json", self.metadata)

    def current(self):
        return sync.read_json(self.root / "registry/latest.json")["skills"][NAME]

    def first(self):
        sync.import_bundle(self.root, self.bundle)

    def revision(self, day=2):
        old = self.current()
        self.item.update(revision=f"test-r{day}", source_updated_at=f"2026-10-{day:02d}T09:00:00+08:00",
                         parent_content_sha256=old["content_sha256"], files=sync.inventory(self.payload))
        self.save()

    def test_complete_import_all_three_and_roundtrip_export(self):
        for name in sync.NAMES - {NAME}:
            import shutil
            shutil.copytree(self.payload, self.bundle / name)
            self.metadata["skills"].append({**self.item, "name": name})
        self.save()
        self.first()
        self.assertEqual(sync.verify(self.root)[1], 3)
        output = self.base / "delivery.zip"
        sync.export_bundle(self.root, output)
        with ZipFile(output) as archive:
            for name in sync.NAMES:
                for path, checksum in self.item["files"].items():
                    self.assertEqual(sync.digest(archive.read(f"{name}/{path}")), checksum)

    def test_same_week_new_revision_and_old_snapshot_preserved(self):
        self.first()
        old = self.current()
        (self.payload / "references/test.md").write_text("TEST RULE B\n")
        self.revision()
        self.first()
        new = self.current()
        self.assertEqual(old["weekly_version"], new["weekly_version"])
        self.assertNotEqual(old["revision"], new["revision"])
        self.assertNotEqual(old["content_sha256"], new["content_sha256"])
        self.assertEqual(sync.verify(self.root)[1], 2)

    def test_idempotent_replay(self):
        self.first()
        before = (self.root / "registry/latest.json").read_bytes()
        self.first()
        self.assertEqual(before, (self.root / "registry/latest.json").read_bytes())

    def test_missing_file_rejected_without_changing_registry(self):
        (self.payload / "references/test.md").unlink()
        with self.assertRaisesRegex(ValueError, "inventory"):
            self.first()
        self.assertEqual(sync.read_json(self.root / "registry/latest.json"), self.initial)

    def test_changed_file_rejected(self):
        (self.payload / "references/test.md").write_text("CHANGED")
        with self.assertRaisesRegex(ValueError, "inventory"):
            self.first()

    def test_extra_file_rejected(self):
        (self.payload / "extra").write_text("UNLISTED")
        with self.assertRaisesRegex(ValueError, "inventory"):
            self.first()

    def test_saved_copy_damage_detected(self):
        self.first()
        target = self.root / self.current()["snapshot"] / "payload/references/test.md"
        target.write_text("DAMAGED")
        with self.assertRaisesRegex(ValueError, "Changed, missing or extra"):
            sync.verify(self.root)
        target.unlink()
        with self.assertRaisesRegex(ValueError, "Changed, missing or extra"):
            sync.verify(self.root)

    def test_broken_reference_detected_even_with_matching_hashes(self):
        (self.payload / "SKILL.md").write_text("[broken](references/missing.md)")
        self.item["files"] = sync.inventory(self.payload)
        self.save()
        with self.assertRaisesRegex(ValueError, "reference"):
            self.first()

    def test_symlinks_rejected(self):
        (self.payload / "link").symlink_to(self.base)
        with self.assertRaisesRegex(ValueError, "Symlink"):
            self.first()

    def test_unsaved_source_rejected(self):
        self.metadata["source_saved"] = False
        self.save()
        with self.assertRaisesRegex(ValueError, "confirmed saved"):
            self.first()

    def test_stale_export_rejected(self):
        self.first()
        old_item = copy.deepcopy(self.item)
        (self.payload / "references/test.md").write_text("NEW")
        self.revision()
        self.first()
        self.metadata["skills"] = [old_item]
        (self.payload / "references/test.md").write_text("TEST RULE A\n")
        self.save()
        with self.assertRaisesRegex(ValueError, "stale parent"):
            self.first()

    def test_revision_cannot_be_reused_for_different_content(self):
        self.first()
        (self.payload / "references/test.md").write_text("NEW")
        self.revision()
        self.item["revision"] = "test-r1"
        self.save()
        with self.assertRaisesRegex(ValueError, "reused revision"):
            self.first()

    def test_withdrawn_file_removed_from_export_and_restore_requires_declaration(self):
        self.first()
        (self.payload / "scripts/test.py").unlink()
        self.revision()
        self.first()
        self.assertEqual(self.current()["removed_paths"], ["scripts/test.py"])
        output = self.base / "delivery.zip"
        sync.export_bundle(self.root, output)
        with ZipFile(output) as archive:
            self.assertNotIn(f"{NAME}/scripts/test.py", archive.namelist())
        (self.payload / "scripts/test.py").write_text("RESTORED TEST SCRIPT\n")
        self.revision(3)
        with self.assertRaisesRegex(ValueError, "restored_paths"):
            self.first()
        self.item["restored_paths"] = ["scripts/test.py"]
        self.save()
        self.first()
        self.assertEqual(self.current()["withdrawn_paths"], [])

    def test_obsolete_content_cannot_be_relabelled_as_new(self):
        self.first()
        (self.payload / "references/test.md").write_text("NEW")
        self.revision()
        self.first()
        (self.payload / "references/test.md").write_text("TEST RULE A\n")
        self.revision(3)
        with self.assertRaisesRegex(ValueError, "obsolete content"):
            self.first()

    def test_numeric_versions_and_no_automatic_release(self):
        self.item["weekly_version"] = "1.9"
        self.save()
        self.first()
        self.revision()
        self.item["weekly_version"] = "1.10"
        self.save()
        self.first()
        self.assertEqual(self.current()["weekly_version"], "1.10")
        self.revision(3)
        self.item["weekly_version"] = "1.9"
        self.save()
        with self.assertRaisesRegex(ValueError, "rollback"):
            self.first()

    def test_failed_multi_skill_import_leaves_current_pointer_unchanged(self):
        self.metadata["skills"].append({**self.item, "name": "manga-reasoning-storyboard"})
        self.save()
        with self.assertRaises(ValueError):
            self.first()
        self.assertEqual(sync.read_json(self.root / "registry/latest.json"), self.initial)

    def test_cannot_export_placeholders(self):
        with self.assertRaisesRegex(ValueError, "No real Skill"):
            sync.export_bundle(self.root, self.base / "delivery.zip")


if __name__ == "__main__":
    unittest.main()
