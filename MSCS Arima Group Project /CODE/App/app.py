from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import plotly.graph_objs as go
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/acorn_categories', methods=['GET'])
def acorn_categories():
    # Load the ACORN details dataset
    acorn_df = pd.read_csv('data/acorn_details.csv', encoding='latin-1')
    # Get unique ACORN categories
    acorn_categories = acorn_df.columns[3:].tolist()
    return jsonify({'acorn_categories': acorn_categories})


@app.route('/acorn_data', methods=['POST'])
def acorn_data():
    # Load the ACORN details dataset
    acorn_df = pd.read_csv('data/acorn_details.csv', encoding='latin-1')
    # Get selected ACORN category
    selected_acorn = request.form['acorn']
    # Filter ACORN details based on selected ACORN
    filtered_acorn_data = acorn_df[['MAIN CATEGORIES', 'CATEGORIES', 'REFERENCE', selected_acorn]]
    # Aggregate data based on MAIN CATEGORIES and CATEGORIES for ACORN details
    grouped_acorn_data = filtered_acorn_data.groupby(['MAIN CATEGORIES', 'CATEGORIES', 'REFERENCE']).sum().reset_index()
    
    # Create separate tables for each group in ACORN details
    tables_by_category = {}
    for index, row in grouped_acorn_data.iterrows():
        main_category = row['MAIN CATEGORIES']
        if main_category not in tables_by_category:
            tables_by_category[main_category] = []
        
        # Check if the current category is different from the previous one
        if index == 0 or row['CATEGORIES'] != grouped_acorn_data.iloc[index - 1]['CATEGORIES']:
            category_html = f'<tr><td>{row["CATEGORIES"]}</td><td>{row["REFERENCE"]}</td><td>{int(row[selected_acorn])}</td></tr>'
        else:
            category_html = f'<tr><td></td><td>{row["REFERENCE"]}</td><td>{int(row[selected_acorn])}</td></tr>'
        
        tables_by_category[main_category].append(category_html)

    # Format tables for each main category
    for category, tables in tables_by_category.items():
        tables_html = '<table class="table table-bordered"><thead><tr><th>CATEGORIES</th><th>REFERENCE</th><th>PEOPLE COUNT</th></tr></thead><tbody>'
        tables_html += ''.join(tables)
        tables_html += '</tbody></table>'
        tables_by_category[category] = tables_html
        
    # Set the directory containing your CSV files
    directory = 'data/compiled'
    
    # Initialize an empty list to store dataframes
    all_dataframes = []
    
    # Loop through each CSV file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            # Read the CSV file into a dataframe
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath, encoding='latin-1')
            # Append the dataframe to the list
            all_dataframes.append(df)
    
    # Concatenate all dataframes into a single dataframe
    daily_df= pd.concat(all_dataframes, ignore_index=True)

    # Filter daily compile data based on selected ACORN
    filtered_daily_data = daily_df[daily_df['Acorn'] == selected_acorn]
    filtered_daily_data = filtered_daily_data[['day','energy_sum','temperatureLow','temperatureHigh']]
    filtered_daily_data = filtered_daily_data.groupby(['day']).mean().reset_index()

    # Generate time series plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_daily_data['day'], y=filtered_daily_data['energy_sum'], mode='lines', name='Energy Consumption'))
    fig.add_trace(go.Scatter(x=filtered_daily_data['day'], y=(filtered_daily_data['temperatureLow'] + filtered_daily_data['temperatureHigh']) / 2, mode='lines', name='Temperature', yaxis='y2'))

    fig.update_layout(title='Daily Energy Consumption and Temperature Time Series',
                      xaxis_title='Day',
                      yaxis_title='Energy Consumption',
                      yaxis2=dict(title='Temperature', overlaying='y', side='right'),
                      legend=dict(x=1.1, y=0.5),
                      width=900)  # Set the width of the plot

    # Convert the Plotly figure to JSON
    plot_json = fig.to_json()

    return jsonify({'plot_json': plot_json, 'tables_by_category': tables_by_category})

@app.route('/kmeans.html')
def kmeans():
    return render_template('kmeans.html')

@app.route('/kmeans_data', methods=['POST'])
def kmeans_data():
    # Load the kmeans dataset
    kmeans_df = pd.read_csv('data/kmeans/kmeans.csv')

    kmeans_df.rename(columns={
        "temperatureMax": 'Temperature Max',
        "temperatureMin": 'Temperature Min',
        "windBearing": 'Wind Bearing',
        "dewPoint": 'Dew Point',
        "cloudCover": 'Cloud Cover',
        "apparentTemperatureMin": 'Apparent Temperature Min',
        "apparentTemperatureMax": 'Apparent Temperature Max',
        "pressure": 'Pressure',
        "precipType": 'Precipitation Type',
        "uvIndex": 'UV Index',
        "energy_sum": 'Energy Consumption',	
    }, inplace=True)

    # Get user-selected x and y axis values
    x_axis = request.form['x_axis']
    y_axis = request.form['y_axis']

    # Get user-selected cluster group
    cluster_group = request.form['cluster_group']

    # Create scatter plot data
    scatter_data = []
    for cluster_label in sorted(kmeans_df[cluster_group].unique()):
        cluster_data = kmeans_df[kmeans_df[cluster_group] == cluster_label]
        scatter_data.append(go.Scatter(
            x=cluster_data[x_axis],
            y=cluster_data[y_axis],
            mode='markers',
            name=f'Cluster {cluster_label}',
            marker=dict(size=8)
        ))

    # Create layout for the scatter plot
    layout = go.Layout(
        title='KMeans Clustering',
        xaxis=dict(title=x_axis),
        yaxis=dict(title=y_axis),
        legend=dict(x=1.0, y=0.9),
        width=1000
    )

    # Create the figure
    fig = go.Figure(data=scatter_data, layout=layout)

    # Convert the Plotly figure to JSON
    plot_json = fig.to_json()

    return jsonify({'plot_json': plot_json})

@app.route('/forecast.html')
def forecast():
    return render_template('forecast.html')

@app.route('/forecast_data', methods=['POST'])
def forecast_data():
    # Get selected ACORN group from the form
    selected_acorn_name = request.form['acorn']
    
    # Load the necessary dataframes for the selected ACORN group
    train_df = pd.read_csv(f'data/Gen_data/forecast/cur_train_{selected_acorn_name}.csv')
    test_df = pd.read_csv(f'data/Gen_data/forecast/cur_test_{selected_acorn_name}.csv')

    # Merge the daily and test dataframes on the 'day' column
    merged_data = pd.merge(train_df, test_df[['day', 'energy_sum','naive_seasonal', 'pred_ARIMA', 'SARIMA_pred', 'pred_STLARIMA']], on='day', how='outer')

    # Concatenate 'energy_sum' columns from train and test DataFrames
    merged_data['energy_sum'] = merged_data['energy_sum_x'].fillna(merged_data['energy_sum_y'])

    # Sort the merged data by 'day' column to ensure proper alignment
    merged_data.sort_values(by='day', inplace=True)

    # Rename the columns
    merged_data.rename(columns={
        'energy_sum': 'Actual',
        'naive_seasonal': 'Naive Seasonal (baseline)',
        'pred_ARIMA': 'ARIMA',
        'SARIMA_pred': 'SARIMA',
        'pred_STLARIMA': 'STLARIMA'
    }, inplace=True)

    # Create time series plot using Plotly for all columns
    fig = go.Figure()
    for column in ['Actual', 'Naive Seasonal (baseline)', 'ARIMA', 'SARIMA', 'STLARIMA']:
        fig.add_trace(go.Scatter(x=merged_data['day'], y=merged_data[column], mode='lines', name=column))

    fig.update_layout(title=f'Daily Energy Consumption Forecast for ACORN Group: {selected_acorn_name}',
                    xaxis_title='Day',
                    yaxis_title='Energy Consumption',
                    legend=dict(x=1, y=0.5),
                    width=1000)

    # Convert the Plotly figure to JSON
    plot_json = fig.to_json()

    return jsonify({'plot_json': plot_json})


def clean_up_txt_file(txt_file_path):
    # Read the content of the TXT file
    with open(txt_file_path, 'r') as f:
        lines = f.readlines()

    # Initialize an empty string to store the HTML table content
    html_table = '<table class="table table-bordered">'
    
    # Loop through each line in the TXT file content
    for line in lines:
        # Split each line into key and value based on the colon ':'
        key, value = line.strip().split(':')

        # Convert the value to a float, round it to two decimal places, and format it back into a string
        rounded_value = '{:.2f}'.format(float(value))

        # Add a new row to the HTML table with the key and value
        html_table += f'<tr><td>{key}</td><td>{rounded_value}</td></tr>'
    
    # Close the HTML table
    html_table += '</table>'
    
    return html_table

@app.route('/forecast_table_data', methods=['POST'])
def forecast_table_data():
    # Get selected ACORN group from the form
    selected_acorn_name = request.form['acorn']
    
    # Clean up the TXT file content
    html_table_content = clean_up_txt_file(f'data/Gen_data/forecast/MAEs_{selected_acorn_name}.txt')

    # Return the HTML table content
    return html_table_content





if __name__ == '__main__':
    app.run(debug=True)
