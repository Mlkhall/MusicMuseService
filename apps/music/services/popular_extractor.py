from apps.music.models import Artists, Releases, Tracks


def popular_extractor() -> tuple[Artists, Releases, Tracks]:
    popular_artists = _extract_popular_artists()
    popular_releases = _extract_popular_releases()
    popular_tracks = _extract_popular_tracks()
    return popular_artists, popular_releases, popular_tracks


def _extract_popular_artists(limit: int = 10) -> Artists:
    return Artists.objects.filter().order_by("-created")[:limit]


def _extract_popular_releases(limit: int = 10) -> Releases:
    release_types = [
        Releases.TypesOfReleases.ALBUM,
        Releases.TypesOfReleases.MINI_ALBUM,
        Releases.TypesOfReleases.SINGLE,
    ]
    return Releases.objects.filter(release_type__in=release_types).order_by("-created")[:limit]


def _extract_popular_tracks(limit: int = 10) -> Tracks:
    return Tracks.objects.filter().order_by("-created")[:limit]
