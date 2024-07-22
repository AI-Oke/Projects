README

Instructions to Run Transatlantic Synergy Flask App:

1. Install Python:
   - Make sure you have Python installed on your system. If not, download and install it from https://www.python.org/downloads/.

2. Navigate to the Project Directory:
   - Open a terminal or command prompt and navigate to the directory where you cloned or downloaded the repository.

3. Install Dependencies:
   - Run the following command to install the required Python packages:
     ```
     pip install -r requirements.txt
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

