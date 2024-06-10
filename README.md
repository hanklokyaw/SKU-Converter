# SKU-Converter

A Flask-based web application for converting and searching SKUs with advanced search capabilities.

## Demo
See the demo [here](https://www.htet.cloud/convert_sku).

## Features
- Convert and search SKUs using various query formats.
- Search options include exact match, starts with, ends with, and contains.
- Intuitive web interface for ease of use.
- Displays results in a tabular format for easy interpretation.

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Steps
1. **Clone the repository:**
    ```sh
    git clone https://github.com/hanklokyaw/SKU-Converter.git
    cd SKU-Converter
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Add your SKU data:**
    - Place your SKU data in the `sample_sku_data.xlsx` file.

6. **Run the application:**
    ```sh
    python main.py
    ```

7. **Open your browser and navigate to:**
    ```
    http://127.0.0.1:5003
    ```

## Usage
- Enter the SKU in the input field.
- Click the "Convert" button or press Enter.
- The application will display the converted SKUs and descriptions in a table format.
- The application supports the following search formats:
    - `CZ?` to search any information that starts with `CZ`.
    - `?1.25` to search any information that ends with `1.25`.
    - `?TOP?` to search any information that includes `TOP`.
 
## Note
In the sample dataset the SKU starts with CZ, GEN, and TIFFANY are included for testing.

## File Overview
- `main.py`: The main Flask application file.
- `templates/index.html`: The HTML template for the web interface.
- `requirements.txt`: The list of dependencies to install.
- `sample_sku_data.xlsx`: Sample SKU data file.

## Contributing
Contributions are welcome! Please create an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.

