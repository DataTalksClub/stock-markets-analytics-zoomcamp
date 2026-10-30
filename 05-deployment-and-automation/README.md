# Deployment and Automation Module

## 2026
- Youtube Recording of the livestream

[![[Stock Market Analytics Zoomcamp 2026] Module 5 "Advanced Trading Simulation and Automation"](https://markdown-videos-api.jorgenkh.no/url?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DuZ51CQumsAM)](https://www.youtube.com/watch?v=uZ51CQumsAM)

- [Code in Colab : \[2026\]_Module_05_Advanced_Strategies_And_Simulation.ipynb](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/05-deployment-and-automation/%5B2026%5D_Module_05_Advanced_Strategies_And_Simulation.ipynb)
  * Please make sure you clone the repo to a local machine and view via Jupyter Notebook
  * OR open the notebook from https://colab.research.google.com/
  * (Note: GitHub's UI may truncate the code and the output)

- **Home assignment (Homework 5)**: exploratory, no-code assignment — propose three stock research ideas. See [cohorts/2026/homework5.md](../cohorts/2026/homework5.md)

- See [UPDATE_SUMMARIES.md](UPDATE_SUMMARIES.md) for the 2026 update summary covering the yfinance upgrade, refreshed stock universe, and the new best model (RandomForest, max_depth=13, n_estimators=100, rule threshold=0.55) used in `main.py`'s local automation pipeline below.
---

## 2025
- Youtube Recording of the livestream on August 4th 2025 

[![[Stock Market Analytics Zoomcamp 2025] Module 5 "Advanced Trading Simulation and Automation"](https://markdown-videos-api.jorgenkh.no/url?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DFA0x_yBfMjM)](https://www.youtube.com/watch?v=FA0x_yBfMjM)


- [View the Slides](https://docs.google.com/presentation/d/e/2PACX-1vQbhpwqnfNTvo1Q4jxeWs5UnncPVhMPrro9iy2Y74ObF0NgfRCzPLBeXvs55Xp2vR-2RknrpQSwefXH/pub?start=false&loop=false&delayms=3000)  


- [Code in Colab : Module_05_Advanced_Strategies_And_Simulation.ipynb](https://github.com/DataTalksClub/stock-markets-analytics-zoomcamp/blob/main/05-deployment-and-automation/%5B2025%5D_Module_05_Advanced_Strategies_And_Simulation.ipynb) 
  * Please make sure you clone the repo to a local machine and view via Jupyter Notebook 
  * OR open the notebook from https://colab.research.google.com/ 
  * (Note: GitHub's UI may truncate the code and the output) 

- **Home assignment (Homework 5)** No Homework Assignment for Module 5
---

## 2024
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

### Option A: `system_test.ipynb` (interactive check)

* Start the local Jupyter Server (after activating venv): `jupyter notebook` (you can check all servers running with `jupyter notebook list`)
* Open `system_test.ipynb` to check the system's operation:
  * From your web browser (navigate to http://localhost:8888/tree or similar)
  * Or via VS Code:
    1. Make sure the venv is created and `requirements.txt` is installed (it already includes `jupyter` and `ipykernel`, so no extra installs are needed).
    2. (Optional, but makes the kernel easier to find) Register the venv as a named Jupyter kernel:
       ```bash
       cd 05-deployment-and-automation/
       source venv/bin/activate
       python -m ipykernel install --user --name=sma-zoomcamp-05 --display-name "Python (sma-zoomcamp 05 venv)"
       ```
    3. Install the **Jupyter** and **Python** extensions (by Microsoft) if not already installed.
    4. Open `system_test.ipynb`, click **"Select Kernel"** in the top-right corner, then choose either **"Python (sma-zoomcamp 05 venv)"** (registered above) or **"Python Environments..."** → browse to `05-deployment-and-automation/venv/bin/python` directly (VS Code usually auto-detects the local `venv/` folder too).
    5. Run the cells with `Shift+Enter` or the ▶️ button.
  * **Note:** the notebook reads from the relative path `local_data/`, so its working directory must be `05-deployment-and-automation/`. In recent versions of the VS Code Jupyter extension this is the default (`jupyter.notebookFileRoot` = `${fileDirname}`). You can confirm this by running `import os; os.getcwd()` in the first cell.

### Option B: `main.py` (full pipeline, for Terminal or Cron)

`main.py` runs the full pipeline once: fetch fresh data (with Stooq/FRED fallback) → transform → train the model → make inference → print top/bottom-3 daily predictions. It takes a few minutes to run (mostly spent downloading per-ticker history via yfinance).

* Run it manually from the Terminal (after activating venv) to simulate one new day of data:
  ```bash
  cd 05-deployment-and-automation/
  source venv/bin/activate
  python main.py
  ```
* Or schedule it with Cron, e.g. every weekday evening after US market close:
  ```bash
  crontab -e
  ```
  Add a line like this (adjust the paths to your machine, and the time/timezone to your needs):
  ```cron
  0 21 * * 1-5 cd /absolute/path/to/05-deployment-and-automation && /absolute/path/to/05-deployment-and-automation/venv/bin/python main.py >> /absolute/path/to/05-deployment-and-automation/cron.log 2>&1
  ```
  * Use the **absolute path** to the venv's `python` binary (`venv/bin/python`) rather than relying on `source venv/bin/activate`, since Cron doesn't run an interactive shell.
  * `cd` into the project folder first, since `main.py` reads/writes `local_data/` using a relative path.
  * Redirecting output to a log file (`cron.log`) makes it easy to debug failed runs (e.g. yfinance rate limits).
