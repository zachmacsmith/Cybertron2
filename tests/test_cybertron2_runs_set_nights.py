"""D2-231: a world may set its fish runs on their windows' set nights though the climate is on (runs_set_nights)."""
from types import SimpleNamespace

from cybertron2.engine import wild as WL


def test_runs_follow_weather_only_without_the_switch(monkeypatch):
    monkeypatch.setattr(WL, "_climate", lambda w: True)
    assert WL._runs_by_weather(SimpleNamespace(spec={})) is True
    assert WL._runs_by_weather(SimpleNamespace(spec={"runs_set_nights": True})) is False
    monkeypatch.setattr(WL, "_climate", lambda w: False)
    assert WL._runs_by_weather(SimpleNamespace(spec={})) is False
