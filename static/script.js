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
    this.size = Math.random() * 5 + 1;
    this.speedX = Math.random() * 3 - 1.5;
    this.speedY = Math.random() * 3 - 1.5;
    this.color = 'rgba(255, 0, 0, ' + Math.random() + ')';
  }
  update() {
    this.x += this.speedX;
    this.y += this.speedY;
    if (this.size > 0.2) this.size -= 0.1;
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
  for (let i = 0; i < 10; i++) {
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
    particleInterval = setInterval(emitParticles, 100);
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
