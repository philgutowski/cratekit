import base64
from enum import StrEnum

from tidalapi import Quality

CTX_TIDAL: str = "tidal"
REQUESTS_TIMEOUT_SEC: int = 45
EXTENSION_LYRICS: str = ".lrc"
UNIQUIFY_THRESHOLD: int = 99
FILENAME_SANITIZE_PLACEHOLDER: str = "_"
COVER_NAME: str = "cover.jpg"
BLOCK_SIZE: int = 4096
BLOCKS: int = 1024
CHUNK_SIZE: int = BLOCK_SIZE * BLOCKS
PLAYLIST_EXTENSION: str = ".m3u"
PLAYLIST_PREFIX: str = "_"
FILENAME_LENGTH_MAX: int = 255
FORMAT_TEMPLATE_EXPLICIT: str = " (Explicit)"
METADATA_EXPLICIT: str = " 🅴"

# Dolby Atmos API credentials: REMOVED WHEN VENDORED (Cratekit patch).
#
# Upstream ships a third-party streaming client id and client secret here,
# base64-encoded and split across concatenated literals. Cratekit ships no
# credential material (R1), so both are empty. The Atmos session switch
# therefore fails its login and returns False, which the download path
# already handles.
#
# Nothing is lost: the Atmos path is gated on a setting that defaults to
# False and requests Quality.low_320k, which R21's lossless policy refuses.
ATMOS_ID_B64 = ""  # emptied when vendored (Cratekit patch, R1)
ATMOS_SECRET_B64 = ""  # emptied when vendored (Cratekit patch, R1)

ATMOS_CLIENT_ID = base64.b64decode(ATMOS_ID_B64).decode("utf-8")
ATMOS_CLIENT_SECRET = base64.b64decode(ATMOS_SECRET_B64).decode("utf-8")
ATMOS_REQUEST_QUALITY = Quality.low_320k


class QualityVideo(StrEnum):
    P360 = "360"
    P480 = "480"
    P720 = "720"
    P1080 = "1080"


class MediaType(StrEnum):
    TRACK = "track"
    VIDEO = "video"
    PLAYLIST = "playlist"
    ALBUM = "album"
    MIX = "mix"
    ARTIST = "artist"


class CoverDimensions(StrEnum):
    Px80 = "80"
    Px160 = "160"
    Px320 = "320"
    Px640 = "640"
    Px1280 = "1280"
    PxORIGIN = "origin"


class TidalLists(StrEnum):
    Playlists = "Playlists"
    Favorites = "Favorites"
    Mixes = "Mixes"


class QueueDownloadStatus(StrEnum):
    Waiting = "⏳️"
    Downloading = "▶️"
    Finished = "✅"
    Failed = "❌"
    Skipped = "↪️"


FAVORITES: dict[str, dict[str, str]] = {
    "fav_videos": {"name": "Videos", "function_name": "videos"},
    "fav_tracks": {"name": "Tracks", "function_name": "tracks_paginated"},
    "fav_mixes": {"name": "Mixes & Radio", "function_name": "mixes"},
    "fav_artists": {"name": "Artists", "function_name": "artists_paginated"},
    "fav_albums": {"name": "Albums", "function_name": "albums_paginated"},
}


class AudioExtensionsValid(StrEnum):
    FLAC = ".flac"
    M4A = ".m4a"
    MP4 = ".mp4"
    MP3 = ".mp3"
    OGG = ".ogg"
    ALAC = ".alac"


class MetadataTargetUPC(StrEnum):
    UPC = "UPC"
    BARCODE = "BARCODE"
    EAN = "EAN"


METADATA_LOOKUP_UPC: dict[str, dict[str, str]] = {
    "UPC": {"MP3": "UPC", "MP4": "UPC", "FLAC": "UPC"},
    "BARCODE": {"MP3": "BARCODE", "MP4": "BARCODE", "FLAC": "BARCODE"},
    "EAN": {"MP3": "EAN", "MP4": "EAN", "FLAC": "EAN"},
}


class InitialKey(StrEnum):
    ALPHANUMERIC = "alphanumeric"
    CLASSIC = "classic"
