"""Shared test settings.

The gate at a run's start (run.start_gate, W-111 §4) is tested in test_cybertron2_start_gate.py. Elsewhere, runs started in tests
use small or old test worlds that the gate check would refuse, and test other things (the journal, branches, replay), so the gate
is replaced there by its "not checked" record; a test marked `gate` keeps the real one."""
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "gate: keep the real gate at a run's start (run.start_gate)")


@pytest.fixture(autouse=True)
def _no_start_gate(request, monkeypatch):
    if request.node.get_closest_marker("gate") or request.module.__name__.endswith("test_cybertron2_start_gate"):
        return
    from cybertron2.engine import run as R
    monkeypatch.setattr(R, "start_gate", lambda spec, ungated=False: {
        "line": "gate: not checked (tests)", "verdict": "not checked", "ungated": False, "refuse": [], "waived": []})
