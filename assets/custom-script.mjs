import WaveSurfer from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js';
import Spectrogram from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/plugins/spectrogram.esm.js';
import Minimap from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/minimap.esm.js';
import colormap from 'https://cdn.jsdelivr.net/npm/colormap@2.3.2/+esm';

let animationId;
let canvas;
let canvasCtx;
let analyser;
let dataArray;
let bufferLength;
const zoomFactor = 0.25; // This might need to be adjusted according to the livestream

function closePlayer(wavesurfer) {
    const playerElement = document.querySelector("#popup");
    const backdrop = document.querySelector("#popup-backdrop");
    playerElement.classList.remove("visible");
    backdrop.classList.add("d-none");
    wavesurfer.destroy();
} 

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

function openPlayer(index) {
    const dataListElement = document.querySelector("#audio-data-list");
    const dataList = JSON.parse(dataListElement.value)
    let data = dataList[index];
    const audioUrl = data.url_media;

    // Generate the colormap array
    const customColormap = colormap({
        colormap: 'magma',
        nshades: 256,
        format: 'rgba',
        alpha: 1
    }).map(color => [color[0] / 255, color[1] / 255, color[2] / 255, color[3]]);    

    const wavesurfer = WaveSurfer.create({
        container: '#popup-audio-container',
        progressColor: '#FFF',
        url: audioUrl, // Production 
        // url: "./assets/example.mp3", // For main page
        // url: "../assets/example.mp3", // for species page
        sampleRate: 32000,
        height: 0,
    });

    wavesurfer.registerPlugin(
        Minimap.create({
          height: 30,
          waveColor: '#6D6762',
          progressColor: '#2E261F',
          normalize: true,
        }),
    )
    
    wavesurfer.registerPlugin(
        Spectrogram.create({
          frequencyMax: 12000,
          splitChannels: false,
          fftSamples: 256,
          labels: false,
          labelsBackground: '#3339',
          height: 150, //this is a bug in wavesurfer and we have to wait untul it is fixed - spectrogram height is not working (seems to work only if spec is greater than height)
          scale: 'linear',
          colorMap: 'roseus' //customColormap,
        }),
      )

    wavesurfer.on('click', () => {
        wavesurfer.play()
    })

    wavesurfer.on('ready', () => {
        wavesurfer.play()
    })

    const comNameElement = document.querySelector("#popup-com-name");
    comNameElement.textContent = data.common_name;
    const sciNameElement = document.querySelector("#popup-sci-name");
    sciNameElement.textContent = data.scientific_name;
    const dateElement = document.querySelector("#popup-date");
    dateElement.textContent = `Date: ${data.datetime}`;
    const recorderElement = document.querySelector("#popup-recorder");
    recorderElement.textContent = `Recorder: #${data.recorder_field_id}`;
    const confidenceElement = document.querySelector("#popup-confidence-text");
    confidenceElement.textContent = `${(data.confidence / 10).toFixed(1)}`;
    const confidenceBar = document.querySelector("#popup-confidence-bar");
    const confidence = data.confidence;
    if (confidence < 33) {
        confidenceBar.style.backgroundColor = "#B31B1B"
    } else if (confidence < 50) {
        confidenceBar.style.backgroundColor = "#FF672E"
    } else if (confidence < 75) {
        confidenceBar.style.backgroundColor = "#FFBC10"
    } else if (confidence < 85) {
        confidenceBar.style.backgroundColor = "#D9EB6F"
    } else if (confidence < 90) {
        confidenceBar.style.backgroundColor = "#A3BC09"
    } else {
        confidenceBar.style.backgroundColor = "#296239"
    }

    let closeButton = document.querySelector("#close-popup-button");
    let replayButton = document.querySelector("#popup-replay-button");
    let nextButton = document.querySelector("#popup-next-button");
    let previousButton = document.querySelector("#popup-previous-button");

    replayButton.replaceWith(replayButton.cloneNode(true));
    nextButton.replaceWith(nextButton.cloneNode(true));
    previousButton.replaceWith(previousButton.cloneNode(true));

    closeButton = document.querySelector("#close-popup-button");
    replayButton = document.querySelector("#popup-replay-button");
    nextButton = document.querySelector("#popup-next-button");
    previousButton = document.querySelector("#popup-previous-button");

    const playerElement = document.querySelector("#popup");
    playerElement.classList.add("visible");

    const backdrop = document.querySelector("#popup-backdrop");
    backdrop.classList.remove("d-none");

    closeButton.addEventListener("click", () => {
        closePlayer(wavesurfer)
    }, {once: true});
    backdrop.addEventListener("click", () => {
        closePlayer(wavesurfer)
    }, {once: true});

    replayButton.addEventListener("click", () => {
        wavesurfer.setTime(0);
        wavesurfer.play();
    });

    if (index < dataList.length - 1) {
        nextButton.classList.remove("disabled");
        nextButton.addEventListener("click", () => {
            closePlayer(wavesurfer);
            openPlayer(index + 1);
        });
    } else {
        nextButton.classList.add("disabled");
    }
    if (index > 0) {
        previousButton.classList.remove("disabled");
        previousButton.addEventListener("click", () => {
            closePlayer(wavesurfer);
            openPlayer(index - 1);
        });
    } else {
        previousButton.classList.add("disabled");
    }
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


window.openPlayer = openPlayer
window.openLivestream = openLivestream