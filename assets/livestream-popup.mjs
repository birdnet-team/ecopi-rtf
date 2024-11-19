let animationId;
let canvas;
let canvasCtx;
let analyser;
let dataArray;
let bufferLength;
const zoomFactor = 0.25; // This might need to be adjusted according to the livestream

function closeLivestream(audioContext, audioElement, resizeEventListener) {
    const playerElement = document.querySelector("#livestream-popup");
    const backdrop = document.querySelector("#livestream-popup-backdrop");
    playerElement.classList.remove("visible");
    backdrop.classList.add("d-none");
    audioContext.close();
    audioElement.pause();
    audioElement.remove();
    window.removeEventListener('resize', resizeEventListener);
}

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight * 0.4; // 25% of the viewport height
    canvasCtx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
}


function draw() {
    animationId = requestAnimationFrame(draw);

    analyser.getByteFrequencyData(dataArray);

    // Shift the image left by 1 pixel
    const imageData = canvasCtx.getImageData(0, 0, canvas.width, canvas.height)
    canvasCtx.putImageData(imageData, -1, 0);

    // Calculate the number of bins to display based on the zoom factor
    const displayBufferLength = Math.floor(bufferLength * zoomFactor);

    // Draw the new FFT data using the Viridis colormap
    for (let i = 0; i < displayBufferLength; i++) {
        const value = dataArray[i];
        const percent = value / 255;
        const y = canvas.height - (i / displayBufferLength) * canvas.height;
        const barHeight = canvas.height / displayBufferLength;

        // Use the Viridis colormap
        const color = d3.interpolateMagma(percent);

        canvasCtx.fillStyle = color;
        canvasCtx.fillRect(canvas.width - 1, y - barHeight, 1, barHeight);
    }
}



function openLivestream(url) {
    const livestreamPopup = document.querySelector("#livestream-popup-content");
    const audioElement = document.createElement('audio');
    audioElement.crossOrigin = "anonymous";
    audioElement.src = url;
    livestreamPopup.appendChild(audioElement);

    canvas = document.getElementById('livestream-spectrogram');
    canvasCtx = canvas.getContext('2d');
    
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    const source = audioContext.createMediaElementSource(audioElement);

    source.connect(analyser);
    analyser.connect(audioContext.destination);

    analyser.fftSize = 2048;
    bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);

    resizeCanvas();
    let resizeEventListener = window.addEventListener('resize', resizeCanvas);

    audioElement.onplay = () => {
        audioContext.resume().then(() => {
            animationId = requestAnimationFrame(draw);
        });
    };

    audioElement.onpause = () => {
        cancelAnimationFrame(animationId);
    };

    audioElement.play();

    const playerElement = document.querySelector("#livestream-popup");
    playerElement.classList.add("visible");

    const backdrop = document.querySelector("#livestream-popup-backdrop");
    backdrop.classList.remove("d-none");

    let closeButton = document.querySelector("#close-livestream-popup-button");
    let livestreamPlayButton = document.querySelector("#livestream-popup-play-button");


    livestreamPlayButton.addEventListener("click", () => {
        if (audioElement.paused) {
            audioElement.play();
            livestreamPlayButton.children[0].classList.remove('bi-play-fill');
            livestreamPlayButton.children[0].classList.add('bi-pause-fill');
        } else {
            audioElement.pause();
            livestreamPlayButton.children[0].classList.add('bi-play-fill');
            livestreamPlayButton.children[0].classList.remove('bi-pause-fill');
        }
    })

    closeButton.addEventListener("click", () => {
        closeLivestream(audioContext, audioElement, resizeEventListener)
    }, {once: true});
    backdrop.addEventListener("click", () => {
        closeLivestream(audioContext, audioElement, resizeEventListener)
    }, {once: true});
}

window.openLivestream = openLivestream