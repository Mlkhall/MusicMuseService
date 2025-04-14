from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from random import randint
from apps.music.models import Artists, Tracks, Releases
from apps.music.services.popular_extractor import popular_extractor


def music(request: HttpRequest) -> HttpResponse:
    template = loader.get_template("music.html")

    popular_artists, popular_releases, popular_tracks = popular_extractor()
    context = {
        "artists": popular_artists,
        "releases": popular_releases,
        "tracks": popular_tracks,
    }

    return HttpResponse(template.render(context, request))


def music_artist_page(request: HttpRequest, artist_id: int) -> HttpResponse:
    template = loader.get_template("music_artist.html")

    artist = get_object_or_404(Artists, pk=artist_id)
    popular_tracks = Tracks.objects.filter(artists__id=artist_id).order_by("-created")[:10]
    releases = Releases.objects.filter(artists__in=[artist])[:10]
    context = {
        'artist': artist,
        'popular_tracks': popular_tracks,
        'releases': releases,
        'monthly_listeners': randint(1, 100),
    }

    return HttpResponse(template.render(context, request))


def music_track_page(request: HttpRequest, track_id: int) -> HttpResponse:
    template = loader.get_template("track_detail.html")

    track = get_object_or_404(Tracks, pk=track_id)
    release_tracks = Tracks.objects.filter(release__id=track.release.pk)

    context = {
        "track": track,
        "release_tracks": release_tracks,
        "total_duration": _calculate_total_duration(release_tracks),
    }

    return HttpResponse(template.render(context, request))


def music_release_page(request: HttpRequest, release_id: int) -> HttpResponse:
    template = loader.get_template("release_detail.html")

    release = get_object_or_404(Releases, pk=release_id)
    tracks = Tracks.objects.filter(release__id=release_id)

    context = {
        "release": release,
        "tracks": tracks,
        "total_duration": _calculate_total_duration(tracks),
    }

    return HttpResponse(template.render(context, request))


def _calculate_total_duration(tracks: list[Tracks]) -> str:
    hours_minutes_seconds = "{hours} ч. {minutes} мин. {seconds} сек."
    minutes_seconds = "{minutes} мин. {seconds} сек."

    total_duration = sum(track.track.duration.seconds for track in tracks)
    seconds = f"0{total_duration % 60}" if total_duration % 60 < 10 else total_duration % 60

    if total_duration >= 3600:
        return hours_minutes_seconds.format(
            hours=total_duration // 3600,
            minutes=(total_duration % 3600) // 60,
            seconds=seconds,
        )
    return minutes_seconds.format(
        minutes=total_duration // 60,
        seconds=seconds,
    )
