import WaveSurfer from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/wavesurfer.esm.js';
import Spectrogram from 'https://cdn.jsdelivr.net/npm/wavesurfer.js@7/dist/plugins/spectrogram.esm.js';
import Minimap from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/minimap.esm.js';
import colormap from 'https://cdn.jsdelivr.net/npm/colormap@2.3.2/+esm';

function closePlayer(wavesurfer) {
    const playerElement = document.querySelector("#popup");
    const backdrop = document.querySelector("#popup-backdrop");
    const popupContent = document.querySelector("#popup-content");
    playerElement.classList.remove("visible");
    backdrop.classList.add("d-none");
    popupContent.classList.add("d-none");
    wavesurfer.stop();
    wavesurfer.destroy();
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
        sampleRate: 48000,
        height: 0,
    });

    wavesurfer.registerPlugin(
        Minimap.create({
          height: 30,
          waveColor: '#a89f98',
          progressColor: '#2E261F',
          normalize: true,
        }),
    )
    
    // https://wavesurfer.xyz/docs/types/plugins_spectrogram.SpectrogramPluginOptions

    wavesurfer.registerPlugin(
        Spectrogram.create({
          frequencyMax: 12000,
          splitChannels: false,
          fftSamples: 512,
          frequencyMin: 300,
          labels: false,
          labelsBackground: '#3339',
          height: 150,
          scale: 'linear',
          colorMap: 'roseus', //customColormap,
          gainDB: 35,
          rangeDB: 100,
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
    dateElement.textContent = `${data.datetime}`;
    const recorderElement = document.querySelector("#popup-recorder");
    recorderElement.textContent = `${data.recorder_field_id}`;
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
    let shareButton = document.querySelector("#share-popup-button");
    let replayButton = document.querySelector("#popup-replay-button");
    let nextButton = document.querySelector("#popup-next-button");
    let previousButton = document.querySelector("#popup-previous-button");

    replayButton.replaceWith(replayButton.cloneNode(true));
    nextButton.replaceWith(nextButton.cloneNode(true));
    previousButton.replaceWith(previousButton.cloneNode(true));

    closeButton = document.querySelector("#close-popup-button");
    shareButton = document.querySelector("#share-popup-button");
    replayButton = document.querySelector("#popup-replay-button");
    nextButton = document.querySelector("#popup-next-button");
    previousButton = document.querySelector("#popup-previous-button");

    const playerElement = document.querySelector("#popup");
    playerElement.classList.add("visible");

    const backdrop = document.querySelector("#popup-backdrop");
    backdrop.classList.remove("d-none");

    const popupContent = document.querySelector("#popup-content");
    popupContent.classList.remove("d-none");

    closeButton.addEventListener("click", () => {
        closePlayer(wavesurfer)
    }, {once: true});
    backdrop.addEventListener("click", () => {
        closePlayer(wavesurfer)
    }, {once: true});

    if (navigator.share) {
        shareButton.replaceWith(shareButton.cloneNode(true));
        shareButton = document.querySelector("#share-popup-button");
        shareButton.addEventListener("click", async () => {
            try {
                const response = await fetch(audioUrl);
                const blob = await response.blob();
                const file = new File([blob], `${data.share_data.filename}`, { type: blob.type });
        
                const shareData = {
                    title: data.share_data.title,
                    text: data.share_data.text,
                    url: data.share_data.url,
                    files: [file]
                };
                
                await navigator.share(shareData);
        
            } catch (error) {
                
                // Fallback, share without file
                try {
                    const shareData = {
                        title: data.share_data.title,
                        text: data.share_data.text,
                        url: data.share_data.url
                    };

                    await navigator.share(shareData);
                } catch (error) {

                    //Finally, catch any error
                    console.error('Error sharing:', error);
                }
            }
        });
    } else {
        shareButton.style.display = 'none';
    }

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

window.openPlayer = openPlayer