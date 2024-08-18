# repository.py
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class UserRepository:
    def load_data_from_csv(self, csv_model):
        logger.info(f"Loading data from CSV: {csv_model}")
        return pd.read_csv(csv_model)

    def load_data_from_database(self, db_model, db_engine, filter_column_name=None, filter_column_value=None):
        logger.info(f"Loading data from database. Model: {db_model}, Engine: {db_engine}")
        engine = create_engine(db_engine)
        with engine.connect() as connection:
            # Modify the query to explicitly declare the textual column expression
            if filter_column_value:
                query = text(f"SELECT * FROM {db_model} WHERE {filter_column_name} = '{filter_column_value}'")
                # data = pd.read_sql_query(query, connection)
            else:
                query = text(f"SELECT * FROM {db_model}")
            data = pd.read_sql_query(query, connection)
        return data
