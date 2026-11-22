"""Core's foundation scenarios: the config file, the taxonomy and the cause table (U299).

The config verbs write `config.toml` through `core.config`'s save and update,
so the file each writes is captured byte for byte: on a fresh state root, after
`crate profile set`, and refused for each schema shape the loader turns away.
The taxonomy verbs write the active copy, and a dump of the taxonomy built from
the shipped template and from the suite's second template, and of the whole
cause and exit code tables, is written into the scenario's directory, so a
refactor of the modules that hold them compares their content, base against
branch.
"""

from __future__ import annotations

import dataclasses
import enum
import json
import re
import tomllib
from collections.abc import Mapping
from pathlib import Path

from cratekit.core import cause, config, exit_codes, secrets, taxonomy
from cratekit.core.exit_codes import ExitCode
from tests.test_active_taxonomy import write_active
from tests.test_config import valid_data
from tests.test_taxonomy_upgrade import behind

OK = int(ExitCode.OK)
SECOND = Path(__file__).resolve().parent.parent / "taxonomies" / "second.toml"


def plain(value):
    """``value`` as JSON can hold it, in an order no hash seed moves."""
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        fields = {f.name: plain(getattr(value, f.name)) for f in dataclasses.fields(value)}
        return {"__class__": type(value).__name__, **fields}
    if isinstance(value, enum.Enum):
        return f"{type(value).__name__}.{value.name}={value.value!r}"
    if isinstance(value, Mapping):
        return {str(plain(k)): plain(v) for k, v in sorted(value.items(), key=lambda i: repr(i[0]))}
    if isinstance(value, (set, frozenset)):
        return sorted((plain(v) for v in value), key=repr)
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, re.Pattern):
        return f"re({value.pattern!r}, {value.flags})"
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(plain(value), indent=1, sort_keys=True) + "\n", encoding="utf-8")


def _configured(library: Path) -> config.Config:
    config.save(config.from_dict(valid_data(library)))
    config.reset_cache()
    return config.load()


def test_the_config_written_shown_and_changed(stage, tmp_path):
    library = tmp_path / "library"
    _configured(library)
    stage.crate("profile", "show")
    stage.json("profile", "show")
    shown = stage.crate("profile", "set", "full")
    assert shown.code != OK or "full" in shown.stdout, shown.stdout
    applied = stage.json("-d", "profile.set.apply=apply", "profile", "set", "full")
    assert applied.code == OK, applied.stdout
    stage.crate("profile", "show")
    stage.json("-d", "profile.set.apply=apply", "profile", "set", "nonesuch")

    def revise(document):
        document.setdefault("rekordbox", {})["pinned_app_version"] = "7.0.1"
        document["rekordbox"]["validated_on"] = "2026-08-01"
        return document

    config.update(revise)
    config.reset_cache()
    dump(tmp_path / "loaded.json", config.load().to_toml_dict())
    stage.crate("profile", "show")


def test_each_config_the_loader_turns_away(stage, tmp_path):
    library = tmp_path / "library"
    written = config.config_path()
    written.parent.mkdir(parents=True, exist_ok=True)
    shapes = {
        "gap": "schema_version = 0\n",
        "too-new": "schema_version = 99\n",
        "no-version": "[library]\nroot = 'x'\n",
        "not-an-integer": "schema_version = 'one'\n",
        "unknown-key": None,
        "invalid": None,
        "missing-keys": f"schema_version = {config.CURRENT_SCHEMA_VERSION}\n",
    }
    for name, text in shapes.items():
        if name == "unknown-key":
            data = valid_data(library, nonesuch={"key": 1})
            text = _toml(data)
        elif name == "invalid":
            data = valid_data(library, profile={"name": "nonesuch"})
            text = _toml(data)
        written.write_text(text, encoding="utf-8")
        config.reset_cache()
        stage.json("profile", "show")
        stage.crate("status")
        try:
            config.load()
        except Exception as refused:  # noqa: BLE001 - the refusal is what is captured
            (tmp_path / f"refusal-{name}.txt").write_text(
                f"{type(refused).__name__}: {refused}\n", encoding="utf-8"
            )


def _toml(data: dict) -> str:
    lines = []
    for key, value in data.items():
        if not isinstance(value, dict):
            lines.append(f"{key} = {json.dumps(value)}")
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"[{key}]")
            lines.extend(f"{k} = {json.dumps(v)}" for k, v in value.items())
    return "\n".join(lines) + "\n"


def test_the_taxonomy_verbs_write_the_active_copy(stage, tmp_path):
    cfg = _configured(tmp_path / "library")
    write_active(cfg, behind())
    for verb in (
        ("taxonomy", "upgrade"),
        ("taxonomy", "alias", "Latin Electronic", "Afro House"),
        ("taxonomy", "folder", "Zouk Bass"),
    ):
        refused = stage.json(*verb)
        assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
        run_id, gate = refused.envelope["run_id"], refused.envelope["cause"]["detail"]["gate"]
        assert stage.decide(run_id, gate, "approve").code == OK
        assert stage.json("--run", run_id, *verb).code == OK
        stage.crate(*verb)
    stage.crate("taxonomy", "alias", "nonesuch-word", "no-such-genre")
    stage.crate("taxonomy", "folder", "music")


def test_the_taxonomies_and_the_tables_dump_equal(stage, tmp_path):
    shipped = taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME)
    dump(tmp_path / "taxonomy-shipped.json", taxonomy.load_taxonomy(shipped))
    dump(tmp_path / "taxonomy-second.json", taxonomy.load_taxonomy(SECOND.read_text("utf-8")))
    for name in taxonomy.shipped_template_names():
        dump(tmp_path / f"fingerprint-{name}.json", taxonomy.shipped_template_fingerprint(name))
    raw = tomllib.loads(shipped)
    raw["bucket"][0]["id"] = "Not An Id"
    raw["fallback"]["bucket"] = "nowhere"
    raw["fuzzy"][0]["bucket"] = "also_nowhere"
    refusals = []
    for refused_text in (raw, "this is not = = toml"):
        try:
            if isinstance(refused_text, str):
                taxonomy.load_taxonomy(refused_text)
            else:
                taxonomy.build_taxonomy(refused_text)
        except taxonomy.TaxonomyError as refused:
            refusals.append(plain(list(refused.problems)))
    assert len(refusals) == 2
    dump(tmp_path / "taxonomy-refused.json", refusals)
    dump(
        tmp_path / "causes.json",
        {
            "reasons": {slug: int(code) for slug, code in cause.REASONS.items()},
            "access_reasons": cause.ACCESS_REASONS,
            "access_remedies": cause.ACCESS_REMEDIES,
            "exit_codes": {code.name: int(code) for code in ExitCode},
            "remedies": list(exit_codes.Remedy),
            "bands": exit_codes.BANDS,
            "meanings": exit_codes.MEANINGS,
            # Every field of every entry but ``why``, which is prose kept as data
            # and never shown, so a refactor may shorten it.
            "state_files": [
                {k: v for k, v in plain(entry).items() if k != "why"}
                for entry in config.STATE_FILES
            ],
        },
    )
    told = []
    for name in sorted(secrets.Credential):
        try:
            secrets.get(name)
        except secrets.CredentialError as refused:
            told.append(f"{name}: {type(refused).__name__}: {refused}")
    (tmp_path / "secrets-refused.txt").write_text("\n".join(told) + "\n", encoding="utf-8")
