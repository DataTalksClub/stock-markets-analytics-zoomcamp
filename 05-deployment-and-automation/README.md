# Deployment and Automation Module

- Youtube Recording of the livestream on June 24th 2024 <br>
[![Youtube Recording](https://markdown-videos-api.jorgenkh.no/youtube/tk7UoILcJ34)](https://www.youtube.com/watch?v=tk7UoILcJ34)

- [View the Slides](https://docs.google.com/presentation/d/e/2PACX-1vSYzqwh8LkFDc2v-3BEr2UnFe5ifL5Hp3a5iWbjhJ86xjtaLu7HrIMH82JU4yOO7NcY9c5pcnDui6gG/pub?start=false&loop=false&delayms=3000)  

- [Code in Colab : Module_05_Advanced_Strategies_And_Simulation.ipynb](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/05-deployment-and-automation/Module_05_Advanced_Strategies_And_Simulation.ipynb) 
  * Please make sure you clone the repo to a local machine and view via Jupyter Notebook 
  * OR open the notebook from https://colab.research.google.com/ 
  * (Note: GitHub's UI may truncate the code and the output) 

- **Home assignment (Homework 5)** No Homework Assignment for Module 5

---
# Local Automation Instructions

## Setting Up the Project Environment (in Terminal)

* Change the working directory to the Module5 folder: `cd 05-deployment-and-automation/`
* Install virtual environment: `pip3 install virtualenv`
* Create a new virtual environment (venv): `virtualenv venv` (or run `python3 -m venv venv`)
* Activate the new virtual environment: `source venv/bin/activate`

* Install Ta-lib (on Mac):
  * Step 1: Install Homebrew (if not already installed): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  * Step 2: Install TA-Lib using Homebrew: `brew install ta-lib`
  * Step 3: Install the ta-lib Python package (After the TA-Lib C library is installed, you can proceed to install the Python package using pip. Make sure you're in your virtual environment if you're using one):
`pip3 install ta-lib`
  * Step 4: Make sure you have Numpy of version earliar than 2, so that ta-lib can be successfully imported (e.g. "numpy==1.26.4" in requirements.txt). [LINK](https://stackoverflow.com/questions/78634235/numpy-dtype-size-changed-may-indicate-binary-incompatibility-expected-96-from)

* Install all requirements to the new environment (venv): `pip3 install -r requirements.txt`

## Running the Project

* Start the local Jupyter Server (after activating venv): `jupyter notebook` (you can check all servers running with `jupyter notebook list`)
* Open `test.ipynb` to check the system's operation:
  * From your web browser (navigate to http://localhost:8888/tree or similar)
  * Or via the VS Code UI (specify the server address kernel) 
* Run `main.py` from the Terminal (or Cron) to simulate one new day of data.
