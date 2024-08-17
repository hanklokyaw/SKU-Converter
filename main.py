from flask import Flask, request, jsonify, render_template
import pandas as pd
import re

# Load the DataFrame with SKU information
df_sage = pd.read_excel('sage_sku_all.xlsx')
df_netsuite = pd.read_csv('sku_convert_db.csv')

# Subset Net Suite SKU prepare to merge
df_in_netsuite = df_netsuite[(df_netsuite['OLD SAGE SKU'].isin(df_sage['Item Code']))]
df_in_netsuite.rename(columns={'Name' : 'New SKU', 'OLD SAGE SKU': 'Old SKU'}, inplace=True)
df_in_netsuite = df_in_netsuite[['Old SKU', 'New SKU', 'Description']]
print(df_in_netsuite[['Old SKU', 'New SKU']])

# Remove Inactive SKU
df_sage = df_sage[df_sage['InactiveItem'] == 'N']
# print(df_sage)

# Subset SKU not in Net Suite and prepare to Merge
df_not_in_netsuite = df_sage[~df_sage['Item Code'].isin(df_netsuite['OLD SAGE SKU'])]
df_not_in_netsuite = df_not_in_netsuite[['Item Code', 'Description']]
df_not_in_netsuite.loc[:,'New SKU'] = '*** NO NEW SKU ***'
df_not_in_netsuite.rename(columns={'Item Code': 'Old SKU'}, inplace=True)
df_not_in_netsuite = df_not_in_netsuite[['Old SKU', 'New SKU', 'Description']]
print(df_not_in_netsuite)

# Subset SKU not in Sage and prepare to Merge
df_not_in_sage = df_netsuite[(~df_netsuite['OLD SAGE SKU'].isin(df_sage['Item Code']))]
df_not_in_sage.loc[:,'Old SKU'] = '*** NO OLD SKU ***'
df_not_in_sage.rename(columns={'Name':'New SKU'}, inplace=True)
df_not_in_sage = df_not_in_sage[['Old SKU', 'New SKU', 'Description']]
print(df_not_in_sage[['Old SKU','New SKU']])

merge_df = pd.concat([df_in_netsuite, df_not_in_netsuite, df_not_in_sage])
print(merge_df)


def search_sku(sku, df):
    print(sku)
    # Determine the type of search based on the presence of '?'
    if sku.startswith('?') and sku.endswith('?'):
        search_term = sku[1:-1]  # Remove '?' from the SKU
        result = df[(df['Old SKU'].str.strip().str.lower().str.contains(search_term)) | (
            df['New SKU'].str.strip().str.lower().str.contains(search_term))]
    elif sku.startswith('?'):
        search_term = sku[1:]  # Remove '?' from the SKU
        result = df[(df['Old SKU'].str.strip().str.lower().str.endswith(search_term)) | (
            df['New SKU'].str.strip().str.lower().str.endswith(search_term))]
    elif sku.endswith('?'):
        search_term = sku[:-1]  # Remove '?' from the SKU
        result = df[(df['Old SKU'].str.strip().str.lower().str.startswith(search_term)) | (
            df['New SKU'].str.strip().str.lower().str.startswith(search_term))]
    elif sku.startswith('desc:'): # Search in description
        search_term = sku[5:].strip()  # Remove '?' from the SKU
        print(search_term)
        result = df[(df['Description'].str.strip().str.lower().str.contains(search_term, na=False))]
    else:
        result = df[(df['Old SKU'].str.lower() == sku) | (
            df['New SKU'].str.lower() == sku)]

    return result

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

    # # Determine the type of search based on the presence of '?'
    # if cleaned_sku.startswith('?') and cleaned_sku.endswith('?'):
    #     search_term = cleaned_sku[1:-1]  # Remove '?' from the SKU
    #     result = df[(df['Old SKU'].str.strip().str.lower().str.contains(search_term)) | (
    #         df['New SKU'].str.strip().str.lower().str.contains(search_term))]
    # elif cleaned_sku.startswith('?'):
    #     search_term = cleaned_sku[1:]  # Remove '?' from the SKU
    #     result = df[(df['Old SKU'].str.strip().str.lower().str.endswith(search_term)) | (
    #         df['New SKU'].str.strip().str.lower().str.endswith(search_term))]
    # elif cleaned_sku.endswith('?'):
    #     search_term = cleaned_sku[:-1]  # Remove '?' from the SKU
    #     result = df[(df['Old SKU'].str.strip().str.lower().str.startswith(search_term)) | (
    #         df['New SKU'].str.strip().str.lower().str.startswith(search_term))]
    # else:
    #     result = df[(df['Old SKU'].str.strip().str.lower() == cleaned_sku) | (
    #                 df['New SKU'].str.strip().str.lower() == cleaned_sku)]

    result = search_sku(cleaned_sku, merge_df)

    # if result.empty:
    #     # Search in Description if no matches found
    #     result = merge_df[merge_df['Description'].fillna('').str.lower().str.contains(
    #         re.escape(cleaned_sku))]

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

