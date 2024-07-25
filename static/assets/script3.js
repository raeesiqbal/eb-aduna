function isMobile() {
    var userAgent = navigator.userAgent || navigator.vendor || window.opera;
    
    // Controlla se l'user agent corrisponde a un dispositivo mobile
    if (/android/i.test(userAgent)) {
        return true;
    }
    
    if (/iPhone|iPad|iPod/i.test(userAgent)) {
        return true;
    }

    if (/windows phone/i.test(userAgent)) {
        return true;
    }

    // Altrimenti, assume che sia un PC
    return false;
}

window.addEventListener("load", function(){
	
	let dim;

	if (isMobile()) {
		dim=0.5
		dimPallini=0.85
    } else {
		dim=1;
		dimPallini=1
    }

    const canvas = document.getElementById("canvas1");
    const ctx = canvas.getContext("2d");
	
    canvas.width = document.documentElement.clientWidth;
    canvas.height = document.documentElement.clientHeight;
	
    class Particle {
        constructor(effect, x, y, color){
            this.effect = effect;
            this.x = x;
            this.y = y;
            this.ease = 0.001;
            this.friction = 0.995;
            this.originX = Math.floor(x);
            this.originY = Math.floor(y);
            //this.size = 1.5;
			this.size = (Math.random()*2.3+0.4)*dimPallini;

            // Give the particle an initial random direction
            let initialAngle = Math.random() * Math.PI * 2-Math.PI;
            let initialSpeed = Math.random() * 15;
            this.vx = Math.cos(initialAngle) * initialSpeed;
            this.vy = Math.sin(initialAngle) * initialSpeed;
            this.color = color;
		
        }

        draw(context) {
            context.beginPath();
            context.arc(this.x, this.y, this.size, 0, Math.PI*2);
            context.fillStyle = this.color;
            context.fill();
            context.closePath();
        }

        update() {
			if (this.effect.pippoMode) {
				
				this.ease = 0.1; // amplificato
				this.friction = 0.99; // amplificato
				this.effect.mouse.radius =15000*dim;
				
			} else if (this.effect.turtleMode) {
				
				this.ease = 0.005; // valore lento per turtleMode
				this.friction = 0.995; // valore lento per turtleMode
				
			} else {
				
				this.ease = 0.005;
				this.friction = 0.9;
				this.effect.mouse.radius =150;
			}
			
            this.dx = this.effect.mouse.x - this.x;
            this.dy = this.effect.mouse.y - this.y;
            this.distance = this.dx * this.dx + this.dy * this.dy;

            this.force = - (this.effect.mouse.radius)*1/ (this.distance^5);

            if (this.distance < this.effect.mouse.radius) {
                this.angle = Math.atan2(this.dy, this.dx);
                this.vx += this.force * Math.cos(this.angle)*dim;
                this.vy += this.force * Math.sin(this.angle)*dim;
            }

			let dax = this.originX - this.x;
			let day = this.originY - this.y;
			let distance3 = Math.sqrt(dax * dax + day * day);
			
			// Normalizza la distanza in modo che sia tra 0 e 1
			let distanceLim0 = (175-40)*dim; // Definisci una distanza massima in cui l'attrito sarà massimo
			let distanceLim1 = (175)*dim; // Definisci una distanza massima in cui l'attrito sarà massimo
			let distanceLim2 = (175+40)*dim; // Definisci una distanza massima in cui l'attrito sarà massimo
			let distanceLim3 = (195+80)*dim; // Definisci una distanza massima in cui l'attrito sarà massimo
			let distanceLim4 = (210+120)*dim; // Definisci una distanza massima in cui l'attrito sarà massimo
			let variableEase;
			let variableFriction; // Dichiara variableFriction all'esterno dei blocchi if-else

			if (!this.effect.turtleMode && !this.effect.pippoMode)
			{
				if (distance3 < distanceLim0) {
					variableEase = this.ease*0.05
					variableFriction = 1;
				} 
				else if(distance3 < distanceLim1)
				{
					variableEase = this.ease*0.075
					variableFriction =  0.9999999999999999999999999999999999999999999999999;

				}
				else if(distance3 < distanceLim2)
				{
					variableEase = this.ease*0.1
					variableFriction =  0.9999999999999999999999999999999999999999999999999;

				}
				else if(distance3 < distanceLim3)
				{
					variableEase = this.ease*0.15
					variableFriction =  0.9999999999999999999999999999999999999999999999999999999;;

				}
				else if(distance3 < distanceLim4)
				{
					variableEase = this.ease*0.1
					variableFriction =  0.999999999999999990000000999999999999999999999999999999999999999999999999999999999999999999;

				}
				else
				{
					variableFriction = this.friction;
					variableEase = this.ease;
				}
			}
			else
			{
				variableEase = this.ease;
				variableFriction = this.friction;
			}



			
			this.x += (this.vx *= variableFriction) + (this.originX - this.x) * variableEase/this.size + (Math.random() * 10 - 5) * 0.2*dim;
			this.y += (this.vy *= variableFriction) + (this.originY - this.y) * variableEase/this.size + (Math.random() * 10 - 5) * 0.2*dim;
			

        }
    }




    class Effect {
        constructor(width, height) {
            this.width = width;
            this.height = height;
            this.particlesArray = [];
            this.image = document.getElementById("logo");
            this.imagep = document.getElementById("pippo");
			
            this.centerX = this.width * 0.5;
            this.centerY = this.height * 0.5;
			this.x = this.centerX - this.image.width * 0.5;
			this.y = this.centerY - this.image.height * 0.5;
            this.gap = 3;
			
			//pippomode
			this.pippoMode = false;
			this.pippoTime = 0;
			this.pippoImage = document.getElementById("pippo");
			this.pippoDuration = 100; // 2 secondi
			
			//turtlemode
			this.turtleMode = true;
			this.turtleTime = 0;
			this.turtleDuration = 3000;
			
			this.lastTouchTime = 0;
			this.isPanning = false;
			
            this.mouse = {
                radius: 10,
                x: undefined,
                y: undefined
            };
			
			window.addEventListener("mousemove", event => {
				effect.mouse.x = event.x;
				effect.mouse.y = event.y;
			});
			
			window.addEventListener("touchmove", event => {
				event.preventDefault();
				for (let i = 0; i < event.touches.length; i++) {
					effect.mouse.x = event.touches[i].clientX;
					effect.mouse.y = event.touches[i].clientY;
					this.isPanning = true;
				}
			});

			window.addEventListener("touchstart", event => {
				for (let i = 0; i < event.touches.length; i++) {
					effect.mouse.x = event.touches[i].clientX;
					effect.mouse.y = event.touches[i].clientY;
				}
			});
			
			window.addEventListener("dblclick", () => {
				
			  if (!effect.turtleMode) {  
				effect.pippoMode = true;
				effect.pippoTime = 0;
				}
				//effect.init(ctx, effect.pippoImage); // Ora usa l'immagine di "pippo"
			});
			
			window.addEventListener("touchend", event => {
				
				if (this.isPanning) {
					this.isPanning = false;  // Resetta il flag isPanning
					return;  // Esci dal gestore dell'evento senza fare nulla
				}
				
				if (!this.pippoMode) {
					
				  if (!effect.turtleMode) {  
					effect.pippoMode = true;
					effect.pippoTime = 0;
					}
					
				}
			});
			

			
			
			/*
			window.addEventListener("touchend", event => {
				const currentTime = Date.now();
				if (currentTime - this.lastTouchTime < 300) { // 300ms è un intervallo comune per il doppio tap
					this.pippoMode = true;
					this.pippoTime = 0;
				}
				this.lastTouchTime = currentTime;
			});
			*/
			
        }




















		init(context, image) {
			
			context.drawImage(image, this.x, this.y);
			const pixels = context.getImageData(0, 0, this.width, this.height).data;
			this.particlesArray = []; // Ripulisci l'array delle particelle prima di inizializzare
			this.particlesArray = []; // Ripulisci l'array delle particelle prima di inizializzare
			
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
            this.particlesArray.forEach(particle => particle.draw(context));
			//this.particlesArray = []
        }

        update() {
            this.particlesArray.forEach(particle => particle.update());
			//this.particlesArray = []
        }
    }

    const effect = new Effect(canvas.width, canvas.height);
    effect.init(ctx,effect.image);

    function animate() {
		
		if (effect.turtleMode) {
			effect.turtleTime += 1000 / 60;  // supponendo 60fps
			
			if (effect.turtleTime > effect.turtleDuration) {
				effect.turtleMode = false;
			}
		}
		
		if (effect.pippoMode) {
			effect.pippoTime += 1000 / 60; // Supponendo 60fps
			
			if (effect.pippoTime > effect.pippoDuration) {
				effect.pippoMode = false;
				//effect.init(ctx, effect.image); // Torna a utilizzare l'immagine del logo
			}
		}
		
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        effect.draw(ctx);
        effect.update();
        requestAnimationFrame(animate);
    }

    animate();
});





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


