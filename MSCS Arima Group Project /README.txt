Repository available at: https://github.gatech.edu/aklein36/Transatlantic-Synergy

# Transatlantic-Synergy


<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Transatlantic-Synergy installation guide for running the website and also the model development jupyter notebook.

## Description

This is a robust toolkit designed to facilitate both the development of time-series models and their subsequent visualization through a dynamic web interface. This comprehensive package caters to data scientists and developers looking to integrate and visualize data analysis seamlessly. It will particularly beneficial to energy providers and customers who are also trying to have greater insights into thier energy consumption.

### Components of the Package
The project is structured into two primary components:

- Model Development: Conducted in a Jupyter Notebook (Forecasting.ipynb and Clustering.ipynb), this component is tailored for building and refiningtime-series models models. Users can interactively test, validate, and analyze data, benefiting from the flexibility and power of the Jupyter environment.

- Visualization: Implemented through a Python script (app.py), this aspect focuses on the visualization of the data and model outcomes. It utilizes Flask, a lightweight web framework, to serve interactive data visualizations directly to a web browser, facilitating an intuitive user interface for exploring complex datasets and model results.


## Executions to Run Transatlantic Synergy Flask App Website:

1. Install Python:
   - Make sure you have Python installed on your system. If not, download and install it from https://www.python.org/downloads/.

2. Navigate to the Project Directory:
   - Open a terminal or command prompt and navigate to the directory where you cloned or downloaded the repository
   - Navigate to the "App" folder.

3. Install Dependencies:
   - Run the following command to install the required Python packages:
    ```
    conda install -c plotly plotly 
    conda install flask
    conda install pandas
    ```

4. Run the Flask App:
   - Once the dependencies are installed, run the Flask app by executing the following command:
     ```
     python app.py
     ```
   - This will start the Flask development server.

5. Access the Web Application:
   - Open a web browser and go to http://127.0.0.1:5000/ to access the Transatlantic Synergy Flask App.
   - From the navigation bar, you can navigate to different sections of the application such as ACORN Details, KMeans, and Forecast.

6. Explore the Application:
   - In the ACORN Details section, select an ACORN group from the dropdown menu and click "Submit" to view energy consumption data and temperature time series.
   - In the KMeans section, select the X-axis, Y-axis, and the number of clusters, then click "Generate Plot" to visualize KMeans clustering.
   - In the Forecast section, select an ACORN group from the dropdown menu and click "Submit" to view daily energy consumption forecast data.

7. Shutdown the Flask App:
   - To shutdown the Flask app, press Ctrl+C in the terminal or command prompt where the Flask app is running.

## Executions to run the Analysis (Clustering and Forecasting) 

### Envioronment Setup

1. First download conda [here](https://docs.anaconda.com/free/miniconda/).

2. Create a new conda environment and activate it using the code below.
    ``` python 
    conda create -n myenv
    conda activate myenv
    ```

3. You can now install the following packages requried to run the file.

    ```
    conda install -c conda-forge scikit-learn pandas
    conda install -c conda-forge statsmodels
    conda install -c conda-forge ipykernel
    conda install -c plotly plotly 
    conda install matplotlib    
    conda install seaborn 
    conda install flask
    pip install pmdarima
    pip install kmodes
    pip install chardet charset-normalizer (depending on OS)
    ```

4. Activate your kernel (optional)

    ```
    python -m ipykernel install --user --name=myenv
    ```

5. In your environment install jupyter notebook with the code below.
    ```
    conda install -c anaconda jupyter notebook 
      ```

    You can start the server with command

    ```
    jupyter-notebook
    ```     

    Open the `Forecasting.ipynb and Clustering.ipynb` file and select the kernel you created above.


## Folder Structure

1. Ensure you have the following structure when running the jupyter notebooks:
```
.
└── Project Directory/
    ├── Forecasting.ipynb
    ├── Clustering.ipynb
    ├── figures/
    ├── forecast/
    ├── future/
    ├── data/
    │   ├── acorn_details.csv
    │   ├── daily_dataset.csv
    │   ├── informations_households.csv
    │   ├── uk_bank_holidays.csv
    │   ├── weather_daily_darksky.csv
    │   ├── weather_hourly_darksky.csv
    │   └── daily_dataset/
    │       ├── block_0.csv
    │       ├── ...
    │       └── block_111.csv
    └── App/
        ├── app.py
        ├── requirements.txt
        ├── data/
        │   ├── acorn_details.csv
        │   ├── compiled/
        │   │   ├── compiled_0.csv
        │   │   ├── ...
        │   │   └── compiled_3.csv
        │   ├── Gen_data/
        │   │   └── forecast/
        │   │       ├── cur_test_ACORN-A.csv
        │   │       ├── ...
        │   │       ├── cur_test_ACORN-Q.csv
        │   │       ├── cur_train_ACORN-A.csv
        │   │       ├── ...
        │   │       ├── cur_train_ACORN-Q.csv
        │   │       ├── MAEs_ACORN-A.txt
        │   │       ├── ...
        │   │       └── MAEs_ACORN-Q.txt
        │   └── k_means/
        │       └── kmeans.csv
        ├── static/
        │   └── Version_1/
        │       ├── logo_info.txt
        │       ├── Transatlantic Synergy-logos_black.png
        │       ├── Transatlantic Synergy-logos_transparent.png
        │       ├── Transatlantic Synergy-logos_white.png
        │       └── Transatlantic Synergy-logos.jpeg
        └── templates/
            ├── forecast.html
            ├── index.html
            └── kmeans.html
```

2. To obtain the dataset:

The energy consumption data (10.27 GB) is available on Kaggle to download and is a refactored version from the London Data Store. The dataset contains files with readings from 5567 residential households. It includes detailed profiles and attributes of acorn groups which segments the residents into different groups, household information including group classification, UK bank holidays, daily weather metrics from and daily measurements such as minimum, maximum, mean, median, sum, and standard deviation.

Dataset is available here:
https://www.kaggle.com/datasets/jeanmidev/smart-meters-in-london
