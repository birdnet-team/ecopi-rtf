# SWAMP - Web app

This is a web application for the **Sapsucker Woods Acoustic Monitoring Project (SWAMP)**. 

SWAMP is a project that uses acoustic monitoring to study the biodiversity of birds in Sapsucker Woods, Ithaca, NY. We use real-time recording units to collect audio data, which is then processed using machine learning models to identify bird species. The web application allows users to explore the data collected by SWAMP and learn more about the bird species present in the Sapsucker Woods bird sanctuary.

Please check out the [SWAMP website](https://birdnet.cornell.edu/swamp) for more information about the project and to access the web app.

We use recording units developed by OekoFor GbR. To learn more about the recording units, visit the [OekoFor website](https://www.oekofor.de/de/portfolio/erfassungstechnik/).

## Setup for development

1. Clone the repository

```bash
git clone https://github.com/birdnet-team/swamp.git
```

2. Create and activate a virtual environment

```bash
cd swamp
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required packages

```bash
pip3 install -r requirements.txt
```

4. Create a file `.env` and add your API token to the `API_TOKEN` key

```bash
API_TOKEN=<your api token>
```

5. You'll also need a mapbox token. Add your token to the `.env` file as follows:

```bash
MAPBOX_TOKEN=<your mapbox token>
```

## Running the app

This is a Dash app, so you can run it with the following command:

```bash
python3 app.py
```

The app will be available at `http://localhost:8050/`.

Note: You'll need an OekoFor API key to run the app. Please send an email to [info@oekofor.de](mailto:info@oekofor.de) to request an API key.

## License

- **Source Code**: The source code for this project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
- **Models**: The models used in this project are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Please ensure you review and adhere to the specific license terms provided with each model. 

*Please note that all educational and research purposes are considered non-commercial use cases and it therefore is free to use BirdNET models in any way.*

## Citation

Feel free to use birdnet for your acoustic analyses and research. If you do, please cite as:

```bibtex
@article{kahl2021birdnet,
  title={BirdNET: A deep learning solution for avian diversity monitoring},
  author={Kahl, Stefan and Wood, Connor M and Eibl, Maximilian and Klinck, Holger},
  journal={Ecological Informatics},
  volume={61},
  pages={101236},
  year={2021},
  publisher={Elsevier}
}
```

## Funding

This project is supported by Jake Holshuh (Cornell class of '69) and The Arthur Vining Davis Foundations. Our work in the K. Lisa Yang Center for Conservation Bioacoustics is made possible by the generosity of K. Lisa Yang to advance innovative conservation technologies to inspire and inform the conservation of wildlife and habitats.

The German Federal Ministry of Education and Research is funding the development of BirdNET through the project "BirdNET+" (FKZ 01|S22072).
Additionally, the German Federal Ministry of Environment, Nature Conservation and Nuclear Safety is funding the development of BirdNET through the project "DeepBirdDetect" (FKZ 67KI31040E).

## Partners

BirdNET is a joint effort of partners from academia and industry.
Without these partnerships, this project would not have been possible.
Thank you!

![Our partners](https://tuc.cloud/index.php/s/KSdWfX5CnSRpRgQ/download/box_logos.png)


