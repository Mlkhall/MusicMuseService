from django.shortcuts import get_object_or_404, render
from .models import Track

def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    release_tracks = track.release.tracks.all()
    
    # Форматирование длительности для всех треков
    for t in release_tracks:
        if t.duration:
            minutes = t.duration // 60
            seconds = t.duration % 60
            t.duration_formatted = f"{minutes}:{seconds:02d}"
        else:
            t.duration_formatted = "0:00"
    
    context = {
        'track': track,
        'release_tracks': release_tracks,
    }
    return render(request, 'track_detail.html', context) 