# SKU Converter App

This is a Flask application that converts and searches SKUs (Stock Keeping Units) from a given dataset. The application supports exact match, starts with, ends with, and contains search queries.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/sku-converter.git
    cd sku-converter
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Place your `sample_sku_data.xlsx` file in the root directory of the project. This file should include 'Old SKU', 'New SKU', and 'Description' columns.

## Running the Application

1. Start the Flask server:

    ```bash
    python main.py
    ```

2. Open your web browser and go to `http://localhost:5003` to access the SKU Converter.

## Usage

- Enter an SKU in the input field and click the "Convert" button to see the matching results.
- The application supports the following search formats:
    - `Fanfare3?` to search any information that starts with `Fanfare3`.
    - `?1.25` to search any information that ends with `1.25`.
    - `?TOP?` to search any information that includes `TOP`.

## Note

In the new SKU format, the letter "l" is used instead of "/". For example, "3/4" becomes "3l4".

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
