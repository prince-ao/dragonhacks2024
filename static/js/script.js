document.addEventListener("DOMContentLoaded", function () {
  let isPlaying = false;
  const canvas = document.getElementById("particleCanvas");
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const btn = document.getElementById("playPauseBtn");
  btn.addEventListener("click", togglePlayPause);

  let particles = [];

  class Particle {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.size = Math.random() * 8 + 3; // Size range of 3-11
      this.speedX = Math.random() * 4 - 2; // Slower movement speed
      this.speedY = Math.random() * 4 - 2;
      this.color = `rgba(255, 0, 0, ${Math.random().toFixed(2)})`;
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      if (this.size > 0.3) this.size -= 0.2;
    }
    draw() {
      ctx.fillStyle = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function handleParticles() {
    for (let i = particles.length - 1; i >= 0; i--) {
      particles[i].update();
      particles[i].draw();
      if (particles[i].size <= 0.3) {
        particles.splice(i, 1);
      }
    }
  }

  function emitParticles() {
    const rect = btn.getBoundingClientRect(); // Get the position and dimensions of the button
    const x = rect.left + rect.width / 2 + window.scrollX; // Center X of the button
    const y = rect.top + rect.height / 2 + window.scrollY; // Center Y of the button

    for (let i = 0; i < 25; i++) {
      particles.push(new Particle(x, y));
    }
  }

  function togglePlayPause() {
    const btn = document.getElementById("playPauseBtn");
    const icon = btn.querySelector("i");

    if (isPlaying) {
      icon.classList.remove("fa-pause");
      icon.classList.add("fa-play");
      console.log("Paused");
      clearInterval(particleInterval);
      stopRecording();
    } else {
      icon.classList.remove("fa-play");
      icon.classList.add("fa-pause");
      console.log("Playing");
      particleInterval = setInterval(emitParticles, 70);
      startRecording();
    }
    isPlaying = !isPlaying;
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    handleParticles();
    requestAnimationFrame(animate);
  }

  animate();
  let particleInterval;
});
