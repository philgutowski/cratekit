"""Doctor's checks of the keychain, the credentials, the binaries and the adapter contract."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

from cratekit import acquire
from cratekit.acquire import adapter as adapter_contract
from cratekit.acquire import catalogue_api
from cratekit.cli.doctor_model import Finding, Status, _Inputs, _unchecked
from cratekit.core import (
    binaries,
    secrets,
)
from cratekit.core.exit_codes import Remedy
from cratekit.tagging import searchers


def _check_keychain(inputs: _Inputs) -> Finding:
    key, title = "keychain.reachable", "OS keychain"
    if inputs.probes.keychain_available():
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail="a keychain backend that can store a credential is available",
        )
    # The environment fallback this message names is honoured: a headless
    # machine that opted in and set every variable is a documented setup.
    needed = _required_credentials(inputs)
    supplied = [name for name in needed if inputs.probes.environment_credential(name)]
    if needed and len(supplied) == len(needed):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"no keychain backend resolves here and every credential this "
                f"profile needs is supplied by the opted-in environment fallback "
                f"({', '.join(needed)}). Nothing can be RECORDED until a backend "
                f"is installed, which is what {secrets.ENV_ALLOW_ENV_CREDENTIALS} "
                f"is for"
            ),
        )
    outstanding = [name for name in needed if name not in supplied]
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            "no keychain backend resolves on this machine. Credentials are never "
            "written to a plain file, so this installation cannot hold one until a "
            "backend is installed or the environment fallback is opted into by name"
            + (
                f". The fallback is supplying {', '.join(supplied)} and not "
                f"{', '.join(outstanding)}"
                if supplied
                else ""
            )
        ),
        remedy=Remedy.INSTALL_KEYCHAIN_BACKEND,
    )


#: Which stored credentials each check key asks about, declared because the
#: grouping is a decision (recognition needs both values). A test asserts every
#: ``secrets.Credential`` appears exactly once, so none goes unchecked (P3, P4).
CREDENTIALS_BY_CHECK: Mapping[str, tuple[secrets.Credential, ...]] = MappingProxyType(
    {
        # Declared by no verb, so it reports and never fails; the verbs that
        # spend it are in ``_SPENT_WHEN_ASKED`` (U176).
        "credential.bandcamp": (secrets.Credential.BANDCAMP_SESSION,),
        # Never fails: without it catalogue lookups go to the account (U205).
        "credential.catalogue": catalogue_api.CREDENTIALS,
        # Only the Cyanite trial script spends it, so it never fails (U245).
        "credential.cyanite": (secrets.Credential.CYANITE_KEY,),
        # Never fails: without it the tagging verbs skip Discogs (U244).
        "credential.discogs": (secrets.Credential.DISCOGS_TOKEN,),
        "credential.provider": (secrets.Credential.PROVIDER_SESSION,),
        "credential.recognition": (
            secrets.Credential.IDENTIFY_KEY,
            secrets.Credential.IDENTIFY_SIGNING_KEY,
        ),
    }
)


#: The remediation for each credential group, kept apart because a session is
#: obtained by authorising and a key by copying it from an account page.
_CREDENTIAL_REMEDY: Mapping[str, Remedy] = MappingProxyType(
    {
        "credential.bandcamp": Remedy.AUTHENTICATE_PROVIDER,
        "credential.catalogue": Remedy.SET_CREDENTIAL,
        "credential.cyanite": Remedy.SET_CREDENTIAL,
        "credential.discogs": Remedy.SET_CREDENTIAL,
        "credential.provider": Remedy.AUTHENTICATE_PROVIDER,
        "credential.recognition": Remedy.SET_CREDENTIAL,
    }
)


#: Credentials no verb declares and the verbs that spend one when asked, named
#: in the finding since "no verb needs it" would be false.
_SPENT_WHEN_ASKED: Mapping[str, tuple[str, ...]] = MappingProxyType(
    {"credential.bandcamp": ("acquire bandcamp", "acquire bandcamp-fetch")}
)


#: Credentials only a trial script spends, and that script, named in the
#: finding so the credential's purpose is clear (U245).
_SPENT_BY_TRIAL: Mapping[str, str] = MappingProxyType(
    {"credential.cyanite": "the Cyanite trial, scripts/cyanite_trial.py"}
)


#: Credentials no verb needs and the verbs that spend one when present (U244).
#: Never a failure; setup offers it whenever one of those verbs is on.
OFFERED_WHEN_SPENT: Mapping[str, tuple[str, ...]] = MappingProxyType(
    {"credential.discogs": ("tag.folder", "tag.retag", "tag.suggest")}
)


def _required_credentials(inputs: _Inputs) -> tuple[str, ...]:
    """Every credential name some verb this profile switches on will spend.

    Derived as the per credential checks derive it, so the two cannot disagree.
    """
    return tuple(
        str(name)
        for check, names in sorted(CREDENTIALS_BY_CHECK.items())
        if inputs.required(check)
        for name in names
    )


def _gate_counts(inputs: _Inputs) -> str:
    """What the provider gate has counted under each identity, as one clause.

    An unreadable state file is said, never shown as nothing spent.
    """
    spent = inputs.probes.provider_spend()
    if spent is None:
        return (
            "the provider gate's state file could not be read, so how many calls "
            "each identity made is not known"
        )
    limited = (
        f", of which {spent.account_rate_limited} and {spent.app_rate_limited} were "
        f"answered with a rate limit"
        if spent.rate_limited
        else ""
    )
    return (
        f"the provider gate has counted {spent.account_calls} calls on the account and "
        f"{spent.app_calls} under Cratekit's app credentials{limited}"
    )


def _check_catalogue(key: str, inputs: _Inputs) -> Finding:
    """Where catalogue lookups go, and what each identity has spent (U205).

    Never a failure, since without the app every lookup goes to the account.
    One value of two is not set up, since one alone cannot ask for a token.
    """
    names = CREDENTIALS_BY_CHECK[key]
    title = "credentials for the catalogue app"
    missing = [str(n) for n in names if not inputs.probes.credential_recorded(str(n))]
    counts = _gate_counts(inputs)
    if not missing:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                # Doctor never reads a value, so this says recorded, not usable.
                f"recorded in this installation: {', '.join(str(n) for n in names)}. "
                f"ISRC lookups and track reads go under Cratekit's app credentials "
                f"whenever the keychain gives both values, and a run that finds one "
                f"missing says so and asks the account; the label crawl and every "
                f"read or write of the account's own things stay on the account "
                f"session; {counts}"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"not recorded ({', '.join(missing)}), so catalogue lookups go to the "
            f"account session, beside its playlists, hearts and downloads"
            + (
                ", since one value without the other cannot ask for a token"
                if len(missing) < len(names)
                else ""
            )
            + f"; {counts}. To move them: {catalogue_api.LOGIN_STEPS}"
        ),
    )


def _check_credential(key: str, inputs: _Inputs) -> Finding:
    if key == "credential.catalogue":
        return _check_catalogue(key, inputs)
    names = CREDENTIALS_BY_CHECK[key]
    title = f"credentials for {key.split('.', 1)[1]}"
    missing = [str(n) for n in names if not inputs.probes.credential_recorded(str(n))]
    if not missing:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"recorded: {', '.join(str(n) for n in names)}",
        )
    if not inputs.required(key) and key in OFFERED_WHEN_SPENT:
        verbs = ", ".join("crate " + verb.replace(".", " ") for verb in OFFERED_WHEN_SPENT[key])
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not recorded ({', '.join(missing)}); {verbs} "
                f"ask Discogs only with it, and without it record Discogs as not "
                f"asked and leave those files askable. To record it: "
                f"{searchers.DISCOGS_LOGIN_STEPS}"
            ),
        )
    if not inputs.required(key) and key in _SPENT_BY_TRIAL:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not recorded ({', '.join(missing)}); no verb uses it, only "
                f"{_SPENT_BY_TRIAL[key]}, which refuses without it naming crate login"
            ),
        )
    if not inputs.required(key):
        spenders = _SPENT_WHEN_ASKED.get(key)
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not recorded ({', '.join(missing)}); only "
                f"{' and '.join(f'crate {verb}' for verb in spenders)} use it, and "
                f"each refuses without it naming crate login"
                if spenders
                else f"not recorded ({', '.join(missing)}), and no verb this profile "
                f"switches on needs it"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"not recorded ({', '.join(missing)}), and this profile switches on a "
            f"verb that spends it. Recording it before the run is the difference "
            f"between a refusal now and a refusal after the first paid call"
        ),
        remedy=_CREDENTIAL_REMEDY[key],
    )


#: Every external binary this product shells out to, derived from the binaries
#: module's tables so a binary added there is probed here at once (P3).
BINARY_NAMES: tuple[str, ...] = (
    *binaries.INSTALLABLE_BINARIES,
    *sorted(binaries.PLATFORM_BINARIES),
)


def _check_binary(key: str, inputs: _Inputs) -> Finding:
    name = key.split(".", 1)[1]
    title = f"external binary {name}"
    found = inputs.probes.find_binary(name)
    if found:
        return Finding(key=key, title=title, status=Status.OK, detail=found)
    override = binaries.env_var(name)
    broken = inputs.probes.binary_override_problem(name)
    if broken is not None:
        # A set override that is not an executable is its own failure, since
        # ``find`` never falls through to PATH while it is set.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL if inputs.required(key) else Status.INFO,
            detail=(
                f"{override} is set to {broken!r}, which is not an executable "
                f"file. Nothing falls through to PATH while it is set, because "
                f"silently running a different binary than the one you named is "
                f"worse than finding none"
            ),
            remedy=Remedy.FIX_BINARY_OVERRIDE,
        )
    if name in binaries.PLATFORM_BINARIES:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL if inputs.required(key) else Status.INFO,
            detail=(
                f"{name} is provided by the operating system and was not found. "
                f"There is nothing to install; its absence means this is not the "
                f"platform it ships with"
            ),
            remedy=Remedy.UNSUPPORTED_PLATFORM if inputs.required(key) else None,
        )
    hint = binaries.install_hint(name)
    source = (
        f"{hint.manager} package {', '.join(hint.packages)}"
        if hint is not None
        else "no packaged source is known for this platform"
    )
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not found, and no verb this profile switches on declares it "
                f"({source}; override with {override})"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"not found on PATH or in the launcher fallback directories, and this "
            f"profile switches on verbs that shell out to it, "
            f"{', '.join(inputs.requiring(key))} ({source}; override with {override})"
        ),
        remedy=(
            Remedy.INSTALL_BINARY if hint is not None
            else Remedy.INSTALL_BINARY_SOURCE_UNKNOWN
        ),
    )


def contract_members(protocol: type = adapter_contract.AcquisitionAdapter) -> tuple[str, ...]:
    """The public members the acquisition protocol declares, derived from it.

    Derived so an adapter is measured against the whole contract, including a
    member added later (P4).
    """
    annotated = set(protocol.__annotations__)
    methods = {
        name
        for name, value in vars(protocol).items()
        if not name.startswith("_") and callable(value)
    }
    return tuple(sorted(annotated | methods))


def _check_adapter(inputs: _Inputs) -> Finding:
    key, title = "adapter.contract", "acquisition adapter"
    if inputs.cfg is None:
        return _unchecked(key, title)
    name = inputs.cfg.acquisition.adapter
    try:
        loaded = acquire.load(name)
    except adapter_contract.UnknownAdapter as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=str(exc),
            remedy=Remedy.CHOOSE_KNOWN_ADAPTER,
        )
    except ImportError as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the adapter {name!r} is registered and its tool is not installed "
                f"here: {exc}. R9's whole point is that acquisition survives one "
                f"tool breaking, and the alternatives are "
                f"{', '.join(acquire.alternatives_to(name)) or 'none'}"
            ),
            remedy=Remedy.INSTALL_ADAPTER,
        )
    required = contract_members()
    absent = [member for member in required if not hasattr(loaded, member)]
    if absent:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the adapter {name!r} resolves to {loaded.__qualname__}, which does "
                f"not satisfy the acquisition contract: missing {', '.join(absent)}"
            ),
            remedy=Remedy.SWITCH_ADAPTER,
        )
    # Read directly, since the membership check proved it is there; a default
    # would misreport a missing name as a mismatch.
    declared = loaded.name
    if declared != name:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"acquisition.adapter names {name!r} and the resolved class calls "
                f"itself {declared!r}. The name is the identifier configuration "
                f"records and every result is reported under, so the two "
                f"disagreeing means a run reports work against an adapter nobody "
                f"selected"
            ),
            remedy=Remedy.SWITCH_ADAPTER,
        )
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=(
            f"{name!r} resolves to {loaded.__qualname__} and satisfies the "
            f"contract ({', '.join(required)})"
        ),
    )
