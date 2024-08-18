# Recommendation Service

This project provides a recommendation system using the `surprise` library, capable of loading data from CSV files or a database. It includes a service layer for handling recommendation logic and a repository layer for data retrieval.

## Project Structure

- **`app.py`**: Entry point for the application. It sets up the Flask app and routes requests to the appropriate controller.
- **`service.py`**: Contains the `RecommendationService` class for processing recommendations.
- **`repository.py`**: Handles data retrieval from CSV files or databases.

## Installation

### 1. Set Up Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

Install Flask

```
pip install Flask
```

Install SQLAlchemy

```
pip install SQLAlchemy
```

Install pandas

```
pip install pandas
```

Install scikit-surprise

```
pip install scikit-surprise
```

### 3. Create requirements.txt

Alternatively, you can create a requirements.txt file with the following content:

```
Flask
SQLAlchemy
pandas
scikit-surprise
```
And install all dependencies at once:
```
pip install -r requirements.txt
```

### Configuration

`app.py`

This file is the entry point of the application. It sets up the Flask app and routes requests to the appropriate controller.

`service.py`

Contains the RecommendationService class, which processes recommendations based on the provided data.

`repository.py`

Includes methods for loading data from CSV files or databases.

## Usage

Starting the Application
Run the Flask app with the following command:

```
python app.py
```

## API Endpoints

`/recommendations`

Method: POST

Description: Retrieves recommendations based on the provided data source and fields.

Request Body:
```
{
    "data_source": "csv",
    "csv_model": "path_to_csv_file",
    "data_fields": ["user_id", "item_id", "rating"],
    "db_model": null,
    "db_engine": null
}
```
Response:
```
{
    "user_id_1": [
        ["item_id_1", estimated_rating_1],
        ["item_id_2", estimated_rating_2]
    ],
    "user_id_2": [
        ["item_id_3", estimated_rating_3]
    ]
}
```

## Example `curl` Commands

To get recommendations using a CSV file, use the following `curl` command:
```
curl -X POST http://127.0.0.1:5000/recommendations \
-H "Content-Type: application/json" \
-d '{
    "data_source": "csv",
    "csv_model": "path_to_csv_file",
    "data_fields": ["user_id", "item_id", "rating"],
    "db_model": null,
    "db_engine": null
}'
```
To get recommendations from a database, modify the data_source, csv_model, and db_model fields accordingly:
```
curl -X POST http://127.0.0.1:5000/recommendations \
-H "Content-Type: application/json" \
-d '{
    "data_source": "database",
    "csv_model": null,
    "db_model": "your_table_name",
    "db_engine": "mysql://username:password@localhost/dbname",
    "data_fields": ["user_id", "item_id", "rating"]
}'
```

## Development

To modify the service or add features, edit the service.py and repository.py files. The app.py file is used to set up routes and should not require frequent changes.

## Contributing

Feel free to submit issues or pull requests for improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
