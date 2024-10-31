# app.py
from flask import Flask, render_template, jsonify
import pandas as pd
from MLBStatsAnalyzer import MLBStatsAnalyzer

app = Flask(__name__)

# Initialize the analyzer with the CSV path
analyzer = MLBStatsAnalyzer('hitting_stats.csv')
analyzer.load_data()
analyzer.process_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/top_players')
def top_players():
    top_data = analyzer.data_sorted[analyzer.selected_columns].head(15).to_dict(orient='records')
    return jsonify(top_data)

@app.route('/api/correlation_matrix')
def correlation_matrix():
    numeric_columns = [
        'WeightedTotal', 'BA', 'HR', 'RBI', 'OBP', 
        'SLG', 'OPS', 'SB', 'TB', 'R', 'BB'
    ]
    correlation_matrix = analyzer.data_sorted[numeric_columns].corr().to_dict()
    return jsonify(correlation_matrix)

if __name__ == '__main__':
    app.run(debug=True)
