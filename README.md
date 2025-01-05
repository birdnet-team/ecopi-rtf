# ecoPi Real-Time Frontend (ecoPi-RTF)

This is a web application built with Dash for visualizing data recorded with **ecoPi** real-time audio recorders. The application allows users to explore the data collected by ecoPi and learn more about the species present in the monitored areas. 

ecoPi is a recording device used in various projects to perform acoustic monitoring and study the biodiversity of birds and other wildlife. The device collects audio data in real-time, which is then processed using machine learning models to identify species. The ecoPi Real Time Frontend (ecoPi-RTF) web application allows users to browse the data collected by ecoPi devices and view the species detected in the recordings.

To learn more about the recording units, visit the [OekoFor website](https://www.oekofor.de/de/portfolio/erfassungstechnik/).

We currently support these monitoring projects:

- SWAMP: Sapsucker Woods Acoustic Monitoring Project - [birdnet.cornell.edu/swamp/](https://birdnet.cornell.edu/swamp/)
- AMiC: Acoustic Monitoring in Chemnitz - [birdnet.cornell.edu/amic/](https://birdnet.cornell.edu/amic/)
- BirdLife Neeracherried Acoustic Monitoring Project - [birdnet.cornell.edu/neeri/](https://birdnet.cornell.edu/neeri/)

Interested? Want to host your own project? Please don't hesitate to contact us at [ccb-birdnet@cornell.edu](mailto:ccb-birdnet@cornell.edu).

**ecoPi-RTF** is a collaboration between the [K. Lisa Yang Center for Conservation Bioacoustics](https://www.birds.cornell.edu/ccb/) at the [Cornell Lab of Ornithology](https://www.birds.cornell.edu), [Chemnitz University of Technology](https://www.tu-chemnitz.de/index.html.en), and [OekoFor GbR](https://www.oekofor.de/).

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

4. Create a file `.env` and add your OekoFor API key to the `API_TOKEN` key

```bash
API_TOKEN=<your api token>
```

**Note:** You'll need an OekoFor API key to run the app. Please send an email to [info@oekofor.de](mailto:info@oekofor.de) to request API access.

5. Add these additional environment variables to the `.env` file:

```bash
CONFIG_FILE=configs/swamp_config.yaml
SITE_ROOT=''
PORT=8050
```

**Note:** If you want to create a new project, you can create a new config file in the `configs` directory and copy the `swamp_config.yaml` file as a template.

## Running the app

This is a Dash app, so you can run it with the following command:

```bash
python3 app.py
```

The app will be available at `http://localhost:8050/`.

You can also specify config files, site root (in case of URL forwarding), and dedicated port using command line arguments:

```bash
python3 app.py --config_file configs/swamp_config.yaml --site_root /swamp --port 8050
```

## Running the app in production

We use Gunicorn to run the app in production. 

Install Gunicorn with the following command:

```bash
sudo apt-get install gunicorn
```

You can now run the app with the following command (from the root directory of the project):

```bash
gunicorn app:server --bind 0.0.0.0:8050 --workers 4 --env CONFIG_FILE=configs/swamp_config.yaml --env SITE_ROOT=/swamp
```

The app will be available at `http://localhost:8050/`. You can specify the number of workers to run with the `--workers` flag based on the number of cores available on your machine. Make sure to set 'debug=False' in the app.py file before running the app in production. You also may have to set `SITE_ROOT` in when using URL forwarding in your domain.

## License

- **Source Code**: The source code for this project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
- **Models**: The models used in this project are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Please ensure you review and adhere to the specific license terms provided with each model. 

*Please note that all educational and research purposes are considered non-commercial use and it is therefore freely permitted to use BirdNET models in any way.*

## Citation

Feel free to use BirdNET for your acoustic analyses and research. If you do, please cite as:

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

The development of BirdNET is supported by the German Federal Ministry of Education and Research through the project “BirdNET+” (FKZ 01|S22072). The German Federal Ministry for the Environment, Nature Conservation, Nuclear Safety and Consumer Protection contributes through the “DeepBirdDetect” project (FKZ 67KI31040E). In addition, the Deutsche Bundesstiftung Umwelt supports BirdNET through the project “RangerSound” (project 39263/01).

## Partners

BirdNET is a joint effort of partners from academia and industry.
Without these partnerships, this project would not have been possible.
Thank you!

![Our partners](https://tuc.cloud/index.php/s/KSdWfX5CnSRpRgQ/download/box_logos.png)


