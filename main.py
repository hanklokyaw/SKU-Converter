from flask import Flask, request, jsonify, render_template
import pandas as pd
import re

# Load the DataFrame with SKU information
df = pd.read_excel('sample_sku_data.xlsx')

# Initialize the Flask app
app = Flask(__name__)

@app.route('/convert_sku', methods=['GET'])
def convert_sku():
    """
    Route to handle SKU conversion queries.
    Supports exact, starts with, ends with, and contains search based on the SKU format.
    """
    sku = request.args.get('sku')  # Get the SKU parameter from the request

    if not sku:
        return jsonify({'error': 'SKU parameter is missing'}), 400  # Return error if SKU is not provided

    cleaned_sku = sku.strip().lower()  # Clean the SKU for comparison

    # Determine the type of search based on the presence of '?'
    if cleaned_sku.startswith('?') and cleaned_sku.endswith('?'):
        search_term = cleaned_sku[1:-1]  # Remove '?' from the SKU
        result = df[(df['Old SKU'].str.strip().str.lower().str.contains(search_term)) | (
            df['New SKU'].str.strip().str.lower().str.contains(search_term))]
    elif cleaned_sku.startswith('?'):
        search_term = cleaned_sku[1:]  # Remove '?' from the SKU
        result = df[(df['Old SKU'].str.strip().str.lower().str.endswith(search_term)) | (
            df['New SKU'].str.strip().str.lower().str.endswith(search_term))]
    elif cleaned_sku.endswith('?'):
        search_term = cleaned_sku[:-1]  # Remove '?' from the SKU
        result = df[(df['Old SKU'].str.strip().str.lower().str.startswith(search_term)) | (
            df['New SKU'].str.strip().str.lower().str.startswith(search_term))]
    else:
        result = df[(df['Old SKU'].str.strip().str.lower() == cleaned_sku) | (
                    df['New SKU'].str.strip().str.lower() == cleaned_sku)]

    if result.empty:
        # SKU not found in 'Old SKU' or 'New SKU'
        # Search in Description if no matches found
        result = df[df['Description'].fillna('').str.lower().str.contains(
            re.escape(cleaned_sku))]

        if result.empty:
            return jsonify({'error': 'SKU not found'}), 404

    result_dict = result.to_dict(orient='records')  # Convert the result to dictionary

    return jsonify(result_dict)

@app.route('/')
def index():
    """
    Route to serve the main HTML page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5003)
