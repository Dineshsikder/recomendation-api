# service.py
import logging
from surprise import Dataset, Reader, KNNBasic
import pandas as pd
from surprise.model_selection import train_test_split
from repository.repository import UserRepository

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_recommendations(self, user_id, request_data):
        try:
            data_source = request_data.get('data_source')
            filter_column_name = request_data.get('filte_column_name')
            filter_column_value = request_data.get('filte_column_value')
            data = self.load_data(data_source, request_data, filter_column_name, filter_column_value)
            data_fields = eval(request_data.get('sorting_fields'))
            # final_data = data[data_fields]
            logger.info(f"data_fields>>>>>>>>>>: {data_fields}")
            logger.info(f"data>>>>>>>>>>: {data}")
             # Convert the list of tuples into a DataFrame
            df = pd.DataFrame(data)
            if 'timestamp' in df.columns:
                try:
                    # Convert timestamp to Unix timestamps (milliseconds)
                    df['timestamp'] = pd.to_datetime(df['timestamp']).astype('int64') // 10**9
                except (KeyError, ValueError):
                    # Handle potential errors (e.g., invalid data format)
                    print("Error converting 'timestamp' column. Skipping conversion.")
            # df['timestamp'] = pd.to_datetime(df['timestamp']).astype('int64') // 10**9

            trainset, testset = self.split_data(df, data_fields)
            algo = self.train_model(trainset)
            predictions = self.make_predictions(algo, testset)
            return self.process_predictions(predictions)
        except Exception as e:
            raise ValueError(f"An error occurred while generating recommendations in get_recommendations funtion of sevice class: {str(e)}")

    def load_data(self, data_source, request_data, filter_column_name, filter_column_value):
        if data_source == 'csv':
            csv_model = request_data.get('csv_model')
            return self.user_repository.load_data_from_csv(csv_model)
        elif data_source == 'database':
            db_model = request_data.get('db_model')
            db_engine = request_data.get('db_engine')
            return self.user_repository.load_data_from_database(db_model, db_engine, filter_column_name, filter_column_value)
        else:
            raise ValueError("Invalid data source. Use 'csv' or 'database'.")

    def split_data(self, data, data_fields):
        reader = Reader(rating_scale=(1, 5))
        if len(data_fields) < 3:
            raise ValueError("sorting_fields must contain at least three columns: user, item, and rating.")
        if len(data_fields) == 3:
            # If there are exactly three fields, use them as is
            dataset = Dataset.load_from_df(data[data_fields], reader)
            return train_test_split(dataset, test_size=0.2)
        else:
            # Otherwise, extract the first three columns as user, item, and rating
            new_data = data[data_fields[:3]]
            dataset = Dataset.load_from_df(new_data, reader)
            return train_test_split(dataset, test_size=0.2)

    def train_model(self, trainset):
        algo = KNNBasic()
        algo.fit(trainset)
        return algo

    def make_predictions(self, algo, testset):
        return algo.test(testset)

    def process_predictions(self, predictions):
        top_n = {}
        for uid, iid, true_r, est, _ in predictions:
            if uid not in top_n:
                top_n[uid] = []
            top_n[uid].append((iid, est))
        logger.info(f"top_n>>>>>>>>>>: {top_n}")
        return top_n