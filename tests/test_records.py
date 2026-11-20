"""The records (D2-232): the views render from the items exactly, and the items check clean."""
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run(*args):
    return subprocess.run([sys.executable, os.path.join(ROOT, "tools", "records.py"), *args], cwd=ROOT,
                          capture_output=True, text=True)


def test_views_in_step_with_items():
    r = run("render", "--check")
    assert r.returncode == 0, r.stdout + r.stderr


def test_items_check_clean():
    r = run("check")
    assert r.returncode == 0, r.stdout + r.stderr


def test_show_reads_a_decision_and_a_spec_file():
    assert "decision" in run("show", "D2-232").stdout
    assert "decided:" in run("show", "docs/cybertron2/spec/environment/land.md").stdout
