"""The rest of core read through its library calls, written down for the capture (U301).

No verb prints these whole, so each answer is written into the scenario's directory.
"""

from __future__ import annotations

import json
from pathlib import Path

from cratekit.core import pool, preflight, provider_gate, tags
from cratekit.core.cause import CratekitError
from tests._containers import synth_container
from tests.test_provider_gate import Clock, Transport, rate_limited
from tests.test_tags import ALL_FIELDS

GIB = 1024**3


def _caught(call) -> object:
    try:
        value = call()
        return {"returned": getattr(value, "status_code", None) or repr(value)}
    except CratekitError as error:
        return error.cause.to_json()
    except Exception as error:  # noqa: BLE001, the capture holds what each refusal is
        return {"raised": type(error).__name__, "message": str(error)}


def _plans() -> list[dict]:
    rows = []
    for available, pressure, worker, items, ceiling in (
        (16 * GIB, 0, GIB, 8, 4),
        (16 * GIB, 0, GIB, 2, 8),
        (3 * GIB, 0, GIB, 8, 8),
        (GIB // 2, 0, GIB, 8, 8),
        (16 * GIB, 95, GIB, 8, 8),
        (None, None, GIB, 8, 8),
        (64 * GIB, 10, 2 * GIB, 100, 12),
    ):
        plan = pool.plan_pool(
            worker_bytes=worker,
            items=items,
            ceiling=ceiling,
            read_available=lambda value=available: value,
            read_pressure=(lambda value=pressure: None if value is None else pool.Pressure(
                swap_used_bytes=0, used_percent=float(value)
            )),
        )
        rows.append(
            {
                "workers": plan.workers,
                "bound": str(plan.bound),
                "explain": plan.explain(),
                "in_process": plan.in_process,
                "generations": plan.generations,
                "account": plan.account(),
            }
        )
    return rows


def _gate(root: Path) -> dict:
    clock = Clock()
    settings = provider_gate.GateSettings(min_interval_s=1.0, cooldown_s=900.0, calls_per_command=4)
    gate = provider_gate.Gate(
        settings, path=root / "gate.json", lock_path=root / "gate.lock", clock=clock, sleep=clock.sleep
    )
    fine, limited = Transport(), Transport(rate_limited("2"))
    said = {"calls": [_caught(lambda: gate.call(lambda: fine.request("GET", "https://api.invalid/x")))]}
    said["limited"] = [
        _caught(lambda: gate.call(lambda: limited.request("GET", "https://api.invalid/x")))
        for _ in range(provider_gate.TRIP_AFTER + 1)
    ]
    said["open"] = _caught(gate.assert_open)
    said["slept"] = clock.slept
    said["spend"] = repr(gate.spend())
    said["standing"] = repr(provider_gate.read_standing(clock.now, path=root / "gate.json"))
    return said


def _preflight(root: Path) -> dict:
    present = root / "here.flac"
    present.write_bytes(b"x")
    samples = {
        "missing": [root / "gone.flac", root / "also.flac"],
        "a directory": [root],
        "one present": [present, root / "gone.flac"],
        "none": [],
    }
    return {
        name: _caught(lambda paths=paths: preflight.assert_paths_readable(paths, root=root))
        for name, paths in samples.items()
    }


def _tags(root: Path) -> dict:
    said = {}
    for suffix in (".flac", ".aiff", ".wav", ".mp3"):
        path = synth_container(root, suffix)
        said[suffix] = {
            "written": tags.write_tags(path, ALL_FIELDS),
            "read": {field: tags.read_tag(path, field) for field in ALL_FIELDS},
            "genre": tags.write_genre(path, "Second Genre"),
            "tempo": _caught(lambda path=path: tags.write_tags(path, {"bpm": "120"})),
        }
    return said


def test_pool_gate_preflight_and_tags_answers(stage, tmp_path):
    out = tmp_path / "answers"
    out.mkdir()
    for name, answer in (
        ("plans", _plans()),
        ("gate", _gate(out)),
        ("preflight", _preflight(out)),
        ("tags", _tags(out)),
    ):
        (out / f"{name}.json").write_text(json.dumps(answer, indent=1, sort_keys=True, default=str))
    stage.crate("doctor", "--help")
