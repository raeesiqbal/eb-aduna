window.addEventListener("load", function () {
  const canvas = document.getElementById("canvas1");
  const ctx = canvas.getContext("2d");
  canvas.width = document.documentElement.clientWidth;
  canvas.height = document.documentElement.clientHeight;

  // Particle class definition
  class Particle {
    constructor(effect, x, y, color) {
      this.effect = effect;
      this.x = x;
      this.y = y;
      // this.ease = 0.1;
      this.ease = 0.003;
      this.friction = 0.995;
      this.originX = Math.floor(x);
      this.originY = Math.floor(y);
      this.size = 1.5;
      this.vx = Math.cos(Math.random() * Math.PI * 2) * (Math.random() * 10);
      this.vy = Math.sin(Math.random() * Math.PI * 2) * (Math.random() * 10);
      this.color = color;
      this.noisex = Math.random() * 0.5;
      this.noisey = Math.random() * 0.5;
      this.dx = 0;
      this.dy = 0;
      this.distance = 0;
      this.force = 0;
      this.angle = 0;
    }

    draw(context) {
      context.beginPath();
      context.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      context.fillStyle = this.color;
      context.fill();
      context.closePath();
    }

    update() {
      this.dx = this.effect.mouse.x - this.x;
      this.dy = this.effect.mouse.y - this.y;
      this.distance = this.dx * this.dx + this.dy * this.dy;
      if (this.distance < 5) {
        this.distance = 0.1;
      }
      this.force = -this.effect.mouse.radius / this.distance;

      if (this.distance < this.effect.mouse.radius) {
        this.angle = Math.atan2(this.dy, this.dx);
        this.vx += this.force * Math.cos(this.angle);
        this.vy += this.force * Math.sin(this.angle);
      }

      this.x +=
        (this.vx *= this.friction) +
        (this.originX - this.x) * this.ease +
        (Math.random() * 10 - 5) * 0.1;
      this.y +=
        (this.vy *= this.friction) +
        (this.originY - this.y) * this.ease +
        (Math.random() * 10 - 5) * 0.1;
    }
  }

  // Effect class definition
  class Effect {
    constructor(width, height) {
      this.width = width;
      this.height = height;
      this.particlesArray = [];
      this.image = document.getElementById("logo");
      this.centerX = this.width * 0.5;
      this.centerY = this.height * 0.5;
      this.x = this.centerX - this.image.width * 0.5;
      this.y = this.centerY - this.image.height * 0.5;
      this.gap = 3;
      this.mouse = {
        radius: 50,
        x: undefined,
        y: undefined,
      };

      window.addEventListener("mousemove", (event) => {
        this.mouse.x = event.clientX;
        this.mouse.y = event.clientY;
      });

      window.addEventListener("touchmove", (event) => {
        event.preventDefault();
        for (let i = 0; i < event.touches.length; i++) {
          this.mouse.x = event.touches[i].clientX;
          this.mouse.y = event.touches[i].clientY;
        }
      });
    }

    init(context) {
      context.drawImage(this.image, this.x, this.y);
      const pixels = context.getImageData(0, 0, this.width, this.height).data;
      for (let y = 0; y < this.height; y += this.gap) {
        for (let x = 0; x < this.width; x += this.gap) {
          const index = (y * this.width + x) * 4;
          const red = pixels[index];
          const green = pixels[index + 1];
          const blue = pixels[index + 2];
          const alpha = pixels[index + 3];
          const color = `rgb(${red}, ${green}, ${blue})`;

          if (alpha > 0) {
            this.particlesArray.push(new Particle(this, x, y, color));
          }
        }
      }
    }

    draw(context) {
      this.particlesArray.forEach((particle) => particle.draw(context));
    }

    update() {
      this.particlesArray.forEach((particle) => particle.update());
    }
  }

  const effect = new Effect(canvas.width, canvas.height);
  effect.init(ctx);

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    effect.draw(ctx);
    effect.update();
    animationId = requestAnimationFrame(animate);
  }

  animate(); // Start animation
});

// window.addEventListener("resize", function () {
//   window.location.reload();
// });

// Text animations
function animateText() {
  const texts = document.querySelectorAll(".text");
  texts.forEach((text, index) => {
    setTimeout(() => {
      text.classList.remove("hidden");
      text.classList.add("animated-text");
      setTimeout(() => {
        text.classList.remove("animated-text");
        text.classList.add("animated-text-out");
        text.classList.add("d-none");
      }, 500);
    }, index * 500 + index * 50); // Delay modified to include 100ms delay per index
  });

  setTimeout(() => {
    const helloDiv = document.getElementById("helloDiv");
    helloDiv.classList.remove("hidden");
    helloDiv.classList.add("animated-hello");

    setTimeout(() => {
      const enterLink = document.getElementById("enterLink");
      enterLink.classList.remove("hidden");
      enterLink.classList.add("animated-hello-link");
    }, 1000);
  }, (texts.length + 1) * 500);
}
setTimeout(animateText, 2000);

setTimeout(function () {
  var backgroundAnimation = document.getElementById("background-animation");
  if (backgroundAnimation) {
    backgroundAnimation.classList.add("d-block");
  }
}, 500);
