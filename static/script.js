let isPlaying = false;
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

class Particle {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.size = Math.random() * 8 + 3; // Decreased size range to 3-11
    this.speedX = Math.random() * 4 - 2; // Decreased speed for slower movement
    this.speedY = Math.random() * 4 - 2; // Decreased speed for slower movement
    this.color = `rgba(255, 0, 0, ${Math.random().toFixed(2)})`;
  }
  update() {
    this.x += this.speedX;
    this.y += this.speedY;
    if (this.size > 0.3) this.size -= 0.2; // Slower size reduction
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
  const x = canvas.width / 2;
  const y = canvas.height / 2;
  for (let i = 0; i < 25; i++) { // Slightly reduced the number of particles emitted per interval
    particles.push(new Particle(x, y));
  }
}

function togglePlayPause() {
  const btn = document.getElementById('playPauseBtn');
  const icon = btn.querySelector('i');

  if (isPlaying) {
    icon.classList.remove('fa-pause');
    icon.classList.add('fa-play');
    console.log('Paused');
    clearInterval(particleInterval);
  } else {
    icon.classList.remove('fa-play');
    icon.classList.add('fa-pause');
    console.log('Playing');
    particleInterval = setInterval(emitParticles, 70); // Slightly less frequent emission for a slower effect
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
