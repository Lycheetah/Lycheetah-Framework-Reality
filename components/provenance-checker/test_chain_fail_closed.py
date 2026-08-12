#!/usr/bin/env python3
"""
Focused regression for OPUS12-P1-025 — chain fail-closed on unknown/truncated ids.

Covers:
  - unknown origin (position 0)
  - unknown id at position 1
  - unknown id at last position
  - truncated id
  - valid chain still succeeds
  - CLI exit codes and structured NODE_NOT_FOUND output

Prefer stdlib only. Run from this directory:

  python3 -m unittest test_chain_fail_closed -v
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import provenance_checker as pc  # noqa: E402


GHOST = "0000000000000000000000000000000000000000000000000000000000000000"
TRUNCATED = "abc123"  # not a full 64-char ledger id; absent from any fresh ledger


def _assert_node_not_found(test: unittest.TestCase, result: dict, *, position: int, node_id: str) -> None:
    test.assertEqual(result.get("status"), "NODE_NOT_FOUND")
    test.assertEqual(result.get("position"), position)
    test.assertEqual(result.get("node_id"), node_id)
    test.assertIsNone(result.get("drift_score"))
    test.assertIsNone(result.get("drift_cumulative"))
    test.assertIsNone(result.get("alert_level"))
    test.assertIsNone(result.get("action_required"))  # not "none" success signal
    test.assertIsNone(result.get("steps"))
    alert = result.get("alert_level")
    test.assertNotIn(alert, ("clean", "CLEAN"))
    test.assertNotEqual(result.get("action_required"), "none")
    # No CLEAN/clean string anywhere that would imply success.
    blob = json.dumps(result)
    test.assertNotIn('"alert_level": "clean"', blob)
    test.assertNotIn('"alert_level": "CLEAN"', blob)
    test.assertNotIn('"action_required": "none"', blob)


class ChainFailClosedLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(prefix="prov-chain-")
        self.db_path = Path(self._tmpdir.name) / "ledger.db"
        self.conn = pc.init_db(self.db_path)
        self.origin_text = "CASCADE Framework tracks knowledge drift across transformation chains."
        self.step1_text = "CASCADE Framework tracks knowledge drift."
        self.step2_text = "CASCADE tracks knowledge."
        self.fp0 = pc.create_fingerprint(self.origin_text, source_uri="test://origin", author="test", conn=self.conn)
        self.fp1 = pc.create_fingerprint(self.step1_text, source_uri="test://s1", author="test", parent_id=self.fp0["node_id"], conn=self.conn)
        self.fp2 = pc.create_fingerprint(self.step2_text, source_uri="test://s2", author="test", parent_id=self.fp1["node_id"], conn=self.conn)
        self.ids = [self.fp0["node_id"], self.fp1["node_id"], self.fp2["node_id"]]
        self.contents = [self.origin_text, self.step1_text, self.step2_text]

    def tearDown(self) -> None:
        self.conn.close()
        self._tmpdir.cleanup()

    def test_unknown_origin_position_0(self) -> None:
        result = pc.check_chain(
            [GHOST, self.ids[1], self.ids[2]],
            self.contents,
            self.conn,
        )
        _assert_node_not_found(self, result, position=0, node_id=GHOST)

    def test_unknown_position_1(self) -> None:
        result = pc.check_chain(
            [self.ids[0], GHOST, self.ids[2]],
            self.contents,
            self.conn,
        )
        _assert_node_not_found(self, result, position=1, node_id=GHOST)

    def test_unknown_last_position(self) -> None:
        result = pc.check_chain(
            [self.ids[0], self.ids[1], GHOST],
            self.contents,
            self.conn,
        )
        _assert_node_not_found(self, result, position=2, node_id=GHOST)

    def test_truncated_id(self) -> None:
        # Truncated id at position 1 (classic list-prefix paste failure).
        result = pc.check_chain(
            [self.ids[0], TRUNCATED, self.ids[2]],
            self.contents,
            self.conn,
        )
        _assert_node_not_found(self, result, position=1, node_id=TRUNCATED)

    def test_valid_chain_still_succeeds(self) -> None:
        result = pc.check_chain(self.ids, self.contents, self.conn)
        self.assertNotEqual(result.get("status"), "NODE_NOT_FOUND")
        self.assertIsNotNone(result.get("chain_id"))
        self.assertEqual(result.get("origin_node"), self.ids[0])
        self.assertEqual(result.get("n_transformations"), 2)
        self.assertIsInstance(result.get("steps"), list)
        self.assertEqual(len(result["steps"]), 3)
        self.assertIn(result.get("alert_level"), ("clean", "caution", "warning", "critical"))
        self.assertIsInstance(result.get("drift_cumulative"), float)
        self.assertIn(result.get("action_required"), ("none", "review", "quarantine", "reject"))


class ChainFailClosedCLITests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(prefix="prov-chain-cli-")
        self.work = Path(self._tmpdir.name)
        # Isolate ledger next to a copy of the script so DB_PATH is local.
        self.script = ROOT / "provenance_checker.py"
        self.env = os.environ.copy()
        # Run from a disposable work dir with a private ledger via chdir + copy.
        # The module binds DB_PATH to script parent, so we invoke the real script
        # but point cwd at a work dir that we seed by fingerprinting through -c
        # with an explicit connection is harder for CLI; use library seed then
        # temporarily swap by running CLI from ROOT with a fresh DB path via
        # monkeypatch is not available. Seed using library into ROOT would
        # pollute. Instead: copy script+deps into work and run there.
        for name in ("provenance_checker.py",):
            (self.work / name).write_text((ROOT / name).read_text(encoding="utf-8"), encoding="utf-8")
        sys.path.insert(0, str(self.work))
        # Re-import under work path for seeding.
        if "provenance_checker" in sys.modules:
            del sys.modules["provenance_checker"]
        import importlib.util
        spec = importlib.util.spec_from_file_location("pc_work", self.work / "provenance_checker.py")
        assert spec and spec.loader
        self.pc_work = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.pc_work)
        conn = self.pc_work.init_db(self.work / "provenance_ledger.db")
        self.origin_text = "Origin content for chain CLI test."
        self.step1_text = "Step one content for chain CLI test."
        self.step2_text = "Step two content for chain CLI test."
        self.fp0 = self.pc_work.create_fingerprint(self.origin_text, conn=conn)
        self.fp1 = self.pc_work.create_fingerprint(self.step1_text, parent_id=self.fp0["node_id"], conn=conn)
        self.fp2 = self.pc_work.create_fingerprint(self.step2_text, parent_id=self.fp1["node_id"], conn=conn)
        conn.close()
        self.ids = [self.fp0["node_id"], self.fp1["node_id"], self.fp2["node_id"]]

    def tearDown(self) -> None:
        # Restore import of the real module for other tests.
        if "provenance_checker" in sys.modules:
            del sys.modules["provenance_checker"]
        sys.path = [p for p in sys.path if p != str(self.work)]
        self._tmpdir.cleanup()

    def _run_chain(self, node_ids: list[str], contents: list[str]) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable,
            str(self.work / "provenance_checker.py"),
            "chain",
            *node_ids,
            "--contents",
            *contents,
        ]
        return subprocess.run(
            cmd,
            cwd=str(self.work),
            capture_output=True,
            text=True,
            env=self.env,
        )

    def test_cli_unknown_origin_exits_nonzero(self) -> None:
        proc = self._run_chain(
            [GHOST, self.ids[1]],
            [self.origin_text, self.step1_text],
        )
        self.assertNotEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        _assert_node_not_found(self, data, position=0, node_id=GHOST)

    def test_cli_unknown_position_1_exits_nonzero(self) -> None:
        proc = self._run_chain(
            [self.ids[0], GHOST],
            [self.origin_text, self.step1_text],
        )
        self.assertNotEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        _assert_node_not_found(self, data, position=1, node_id=GHOST)

    def test_cli_unknown_last_exits_nonzero(self) -> None:
        proc = self._run_chain(
            [self.ids[0], self.ids[1], GHOST],
            [self.origin_text, self.step1_text, self.step2_text],
        )
        self.assertNotEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        _assert_node_not_found(self, data, position=2, node_id=GHOST)

    def test_cli_truncated_exits_nonzero(self) -> None:
        proc = self._run_chain(
            [self.ids[0], TRUNCATED],
            [self.origin_text, self.step1_text],
        )
        self.assertNotEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        _assert_node_not_found(self, data, position=1, node_id=TRUNCATED)

    def test_cli_valid_chain_exits_zero(self) -> None:
        proc = self._run_chain(
            self.ids,
            [self.origin_text, self.step1_text, self.step2_text],
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)
        data = json.loads(proc.stdout)
        self.assertNotEqual(data.get("status"), "NODE_NOT_FOUND")
        self.assertIsNotNone(data.get("chain_id"))
        self.assertEqual(data.get("n_transformations"), 2)


if __name__ == "__main__":
    unittest.main()
