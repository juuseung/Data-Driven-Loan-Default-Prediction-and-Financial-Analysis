from flask import Flask, flash, redirect, render_template, request, jsonify, send_file
import os

from sklearn.metrics import classification_report
from utils import *
from constants import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings

# Ignore FutureWarning across all modules
warnings.filterwarnings(action='ignore', category=FutureWarning)

app = Flask(__name__)

print("INFO: check for intended access paths")
print(f"\t{INPUT_FILE_PATH=}")
print(f"\t{MODELS_DIR_PATH=}")
NEG_SAMPLES_FILE_PATH = os.path.join(ROOT_DIR, "negative_samples.csv")
POS_SAMPLES_FILE_PATH = os.path.join(ROOT_DIR, "positive_samples.csv")
CLEAN_FILE_PATH = os.path.join(INPUT_DIR, "Loan_Default_cleaned_downsampled.csv")

@app.route('/')
def main():
    """
    This function returns landing Page and sample records.
    """
    neg_df = pd.read_csv(NEG_SAMPLES_FILE_PATH, index_col=0)
    pos_df = pd.read_csv(POS_SAMPLES_FILE_PATH, index_col=0)

    # Converting DataFrames to list of dicts
    neg_data = neg_df.to_dict(orient='records')
    pos_data = pos_df.to_dict(orient='records')
    
    # Rendering the main.html and send data
    return render_template('main.html', neg_data=neg_data, pos_data=pos_data)

@app.route('/submit', methods=['POST'])
def submit():
    """
    This function handles takes the user input and generates prediction.
    """
    submit_data = request.get_json()['data']
    y_pred, y_true = predict(submit_data)
    return jsonify({"predicted":list(y_pred), "actual": list(y_true)})

@app.route('/plot', methods=['POST'])
def plot():
    """
    This function generates a bar plot for Age and Loan Approvals status
    """
    loanDF = pd.read_csv(CLEAN_FILE_PATH)
    age_categories = {1: 'under25', 2: '25-34', 3: '35-44', 4: '45-54', 5: '55-64', 6: '65-74', 7: 'over74'}
    grouped_data = loanDF.groupby(['age', 'status']).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.35
    ages = list(age_categories.keys())

    for status in [0, 1]:
        ax.bar([int(age) - width/2 if status == 0 else int(age) + width/2 for age in ages],
            grouped_data[status], width, label=f'Status {status}')

    ax.set_xlabel('Age Group')
    ax.set_title('Age Distribution by Status')
    ax.set_xticks(range(1, len(age_categories) + 1))
    ax.set_xticklabels(age_categories.values())
    ax.legend()

    plt.tight_layout()
    plt.savefig('age_distribution_plot.png')
    
    plot_path = 'age_distribution_plot.png'
    return send_file(plot_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)