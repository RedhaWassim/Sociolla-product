import pandas as pd
from typing import Literal, Optional, List, Dict, Any, Tuple
from src.utils.logger import logging
from sklearn.model_selection import train_test_split
from src.utils.utils import get_from_dict_or_env
from pydantic import BaseModel, model_validator

class DataIngestionConfig(BaseModel):
    raw_data_path: str
    train_data_path: str
    test_data_path: str

    class ConfigDict:
        """pydantic forbidding extra parameters"""

        extra = "forbid"


class DataIngestion(BaseModel):
    config: DataIngestionConfig = DataIngestionConfig()
    """raw , train , test data paths"""

    ingestion_type: Literal["csv", "db"] = "csv"
    """either choose to ingest data from a csv or from a supabase table"""

    save_csv: bool = False
    """whether to save the csv files or not"""

    data_path: Optional[str] = None
    """path of the csv file to ingest"""

    supabase_key: Optional[str] = None
    supabase_url: Optional[str] = None
    """api keys to read data from database"""

    table_name: Optional[str] = None
    """table name in supabase database"""

    class ConfigDict:
        """pydantic forbidding extra parameters"""

        extra = "forbid"

    @model_validator(mode="after")
    def check_tablename(self) -> "DataIngestion":
        table = self.table_name
        path = self.data_path
        if self.ingestion_type == "csv" and path is None:
            raise ValueError("table_name cannot be None when ingestion_type is 'csv")
        elif self.ingestion_type == "db" and table is None:
            raise ValueError("table_name cannot be None when ingestion_type is 'db")

        return self

    @model_validator(mode="before")
    @classmethod
    def validate_environement(cls, values: Dict) -> Dict:
        if values["ingestion_type"] == "db":
            values["supabase_key"] = get_from_dict_or_env(
                values, "supabase_key", "SUPABASE_KEY"
            )
            values["supabase_url"] = get_from_dict_or_env(
                values, "supabase_url", "SUPABASE_URL"
            )
        return values

    def _read_from_db(self) -> tuple:
        pass

    def _split_data(self, df: pd.DataFrame) -> tuple:
        logging.info("Splitting data into train and test")
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

        if self.save_csv:
            logging.info("Saving train and test data")
            train_data.to_csv(self.config.train_data_path, index=False)
            test_data.to_csv(self.config.test_data_path, index=False)

        return train_data, test_data

    def _read_from_csv(self) -> tuple:
        """read data from csv file and return train and test data

        Returns:
            tuple containing train and test data in pandas dataframe
        """

        logging.info("Reading data from csv file")
        df = pd.read_csv(self.data_path)

        train_data, test_data = self._split_data(df)

        return train_data, test_data

    def run_ingestion(self) -> Tuple:
        try:
            logging.info("Starting data ingestion")
            if self.ingestion_type == "csv":
                train_data, test_data = self._read_from_csv(self.data_path)
            else:
                train_data, test_data = self._read_from_db()

            logging.info("data ingestion completed")

        except Exception as e:
            logging.error(f"Error while ingesting data : {e}")
            raise e


if __name__ == "__main__":
    obj = DataIngestion(
        ingestion_type="csv",
        data_path="/home/redha/Documents/projects/NLP/sociolla/data/archive/products_all_brands.csv",
        save_csv=True,
    )

    obj.run_ingestion()
