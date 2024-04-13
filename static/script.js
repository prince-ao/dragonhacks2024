let isPlaying = false;

function togglePlayPause() {
    const btn = document.getElementById('playPauseBtn');
    const icon = btn.querySelector('i');

    if (isPlaying) {
        icon.classList.remove('fa-pause');
        icon.classList.add('fa-play');
        console.log('Paused'); // Replace with your pause functionality
    } else {
        icon.classList.remove('fa-play');
        icon.classList.add('fa-pause');
        console.log('Playing'); // Replace with your play functionality
    }
    isPlaying = !isPlaying;
}
