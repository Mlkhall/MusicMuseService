document.addEventListener('DOMContentLoaded', function() {
    const miniPlayer = document.getElementById('miniPlayer');
    const fullPlayer = document.getElementById('fullPlayer');
    const audioPlayer = document.getElementById('audioPlayer');
    const trackItems = document.querySelectorAll('.track-item');
    const mainPlayButton = document.getElementById('playArtistButton');
    
    function playTrack(trackData) {
        // Обновляем информацию в плеере
        document.querySelector('.mini-player-cover').src = trackData.coverUrl;
        document.querySelector('.mini-player-title').textContent = trackData.trackName;
        document.querySelector('.mini-player-artist').textContent = trackData.artistName;
        
        // Обновляем полноэкранный плеер
        document.getElementById('trackCover').src = trackData.coverUrl;
        document.getElementById('trackTitle').textContent = trackData.trackName;
        document.getElementById('trackArtist').textContent = trackData.artistName;
        
        // Устанавливаем аудио
        audioPlayer.src = trackData.audioUrl;
        audioPlayer.play();
        
        // Показываем мини-плеер
        miniPlayer.style.transform = 'translateY(0)';
    }
    
    // Обработчик для кнопок воспроизведения в списке треков
    trackItems.forEach(item => {
        item.querySelector('.play-button-small').addEventListener('click', (e) => {
            e.stopPropagation();
            const trackData = {
                trackName: item.dataset.trackName,
                artistName: item.dataset.artistName,
                coverUrl: item.dataset.coverUrl,
                audioUrl: item.dataset.audioUrl
            };
            playTrack(trackData);
        });
    });
    
    // Обработчик для главной кнопки воспроизведения
    mainPlayButton.addEventListener('click', () => {
        // Воспроизводим первый трек из списка
        const firstTrack = trackItems[0];
        const trackData = {
            trackName: firstTrack.dataset.trackName,
            artistName: firstTrack.dataset.artistName,
            coverUrl: firstTrack.dataset.coverUrl,
            audioUrl: firstTrack.dataset.audioUrl
        };
        playTrack(trackData);
    });
}); 