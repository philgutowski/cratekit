#!/usr/bin/env python
import importlib.metadata
# `from pathlib import Path` removed when vendored: only the replaced metadata_project() used it.
from urllib.parse import urlparse

import requests
# `import toml` removed when vendored: only the replaced metadata_project() used it.

from cratekit._vendor.downloader.constants import REQUESTS_TIMEOUT_SEC
from cratekit._vendor.downloader.model.meta import ProjectInformation, ReleaseLatest


# Cratekit patch: the version is PINNED at vendoring time.
#
# Upstream discovered it by walking up to three parent directories from its own
# __file__ looking for a pyproject.toml, then reading ["project"]["version"] and
# ["project"]["urls"]["repository"] out of whichever one it found first, with no
# check on whose file that was.
#
# Vendored, the nearest such file is the HOST application's. Reading it would
# raise KeyError at import time, because Cratekit declares no [project.urls] and
# that lookup sits outside upstream's try block, so `import tidal_dl_ng` would
# fail for a reason naming none of this. Today the walk misses Cratekit's
# pyproject.toml by exactly one directory level. A pinned constant does not
# depend on how deep the package happens to sit.
_VENDORED_VERSION = "0.33.0"
_UPSTREAM_REPOSITORY = "https://github.com/exislow/tidal-dl-ng"


def metadata_project() -> ProjectInformation:
    return ProjectInformation(version=_VENDORED_VERSION, repository_url=_UPSTREAM_REPOSITORY)


def version_app() -> str:
    metadata: ProjectInformation = metadata_project()
    version: str = metadata.version

    return version


def repository_url() -> str:
    metadata: ProjectInformation = metadata_project()
    url_repo: str = metadata.repository_url

    return url_repo


def repository_path() -> str:
    url_repo: str = repository_url()
    url_path: str = urlparse(url_repo).path

    return url_path


def latest_version_information() -> ReleaseLatest:
    release_info: ReleaseLatest
    repo_path: str = repository_path()
    url: str = f"https://api.github.com/repos{repo_path}/releases/latest"

    try:
        response = requests.get(url, timeout=REQUESTS_TIMEOUT_SEC)
        response.raise_for_status()

        release_info_json: dict = response.json()

        release_info = ReleaseLatest(
            version=release_info_json["tag_name"],
            url=release_info_json["html_url"],
            release_info=release_info_json["body"],
        )
    except (requests.RequestException, KeyError, ValueError):
        release_info = ReleaseLatest(
            version="v0.0.0",
            url=url,
            release_info=f"Something went wrong calling {url}. Check your internet connection.",
        )

    return release_info


def name_package() -> str:
    package_name: str = __package__ or __name__

    return package_name


def is_dev_env() -> bool:
    package_name: str = name_package()
    result: bool = False

    # Check if package is running from source code == dev mode
    # If package is not running in Nuitka environment, try to import it from pip libraries.
    # If this also fails, it is dev mode.
    if "__compiled__" not in globals():
        try:
            importlib.metadata.version(package_name)
        except Exception:
            # If package is not installed
            result = True

    return result


def name_app() -> str:
    app_name: str = name_package()
    is_dev: bool = is_dev_env()

    if is_dev:
        app_name += "-dev"

    return app_name


# Cratekit patch: pinned. Derived from __package__ upstream, which vendored
# would name the settings, log, and token directory after an import path.
__name_display__ = "cratekit-downloader"
__version__ = version_app()


def update_available() -> tuple[bool, ReleaseLatest]:
    latest_info: ReleaseLatest = latest_version_information()
    version_current: str = f"v{__version__}"

    result = version_current not in [latest_info.version, "v0.0.0"]
    return result, latest_info
