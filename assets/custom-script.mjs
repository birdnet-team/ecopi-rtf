import WaveSurfer from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js'
import Spectrogram from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/plugins/spectrogram.esm.js'

function closePlayer(wavesurfer) {
    const playerElement = document.querySelector("#popup");
    const backdrop = document.querySelector("#popup-backdrop");
    playerElement.classList.remove("visible");
    backdrop.classList.add("d-none");
    wavesurfer.destroy();
} 

function openPlayer(audioUrl) {
    const wavesurfer = WaveSurfer.create({
        container: '#popup-content',
        waveColor: 'rgb(200, 0, 200)',
        progressColor: 'rgb(100, 0, 100)',
        url: audioUrl,
        // url: "./assets/example.mp3",
        sampleRate: 22050,
    });
    
    wavesurfer.registerPlugin(
        Spectrogram.create({
          height: 400,
          splitChannels: false,
          frequencyMax: 12000,
          labels: false,
        }),
      )

    wavesurfer.on('click', () => {
        wavesurfer.play()
    })

    wavesurfer.on('ready', () => {
        wavesurfer.play()
    })

    const closeButton = document.querySelector("#close-popup-button");

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
}

window.openPlayer = openPlayer