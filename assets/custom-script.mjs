import WaveSurfer from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js'
import Spectrogram from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/plugins/spectrogram.esm.js'

function closePlayer(wavesurfer) {
    const playerElement = document.querySelector("#popup");
    const backdrop = document.querySelector("#popup-backdrop");
    playerElement.classList.remove("visible");
    backdrop.classList.add("d-none");
    wavesurfer.destroy();
} 

function openPlayer(data) {
    console.log(data);
    const audioUrl = data.url_media;

    const wavesurfer = WaveSurfer.create({
        container: '#popup-audio-container',
        waveColor: 'rgb(200, 0, 200)',
        progressColor: 'rgb(100, 0, 100)',
        // url: audioUrl, // Production 
        // url: "./assets/example.mp3", // For main page
        url: "../assets/example.mp3", // for species page
        sampleRate: 32000,
        
    });
    
    wavesurfer.registerPlugin(
        Spectrogram.create({
          maxFrequency: 12000,
          splitChannels: false,
          fftSamples: 1024,
          labels: false,
          
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

    if (data.nextDataElementId) {
        nextButton.classList.remove("disabled");
    } else {
        nextButton.classList.add("disabled");
    }
    if (data.previousDataElementId) {
        previousButton.classList.remove("disabled");

    } else {
        previousButton.classList.add("disabled");
    }
}

window.openPlayer = openPlayer