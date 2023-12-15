import pandas as pd
from typing import Literal, Optional, List, Dict, Any, Tuple
from sociolla.utils.logger import logging
from sklearn.model_selection import train_test_split
from sociolla.utils.utils import get_from_dict_or_env, retreive_base_path
from pathlib import Path 
from pydantic import BaseModel, model_validator
import os

class DataIngestionConfig(BaseModel):
    base_path: str = retreive_base_path()
    raw_data_path: str = str(Path(base_path, f"artifacts/raw/raw_data.csv"))

    class ConfigDict:
        """pydantic forbidding extra parameters"""

        extra = "forbid"


class DataIngestion(BaseModel):
    ingestion_config: DataIngestionConfig = DataIngestionConfig()
    """where to save data"""

    ingestion_type: Literal["csv", "db"] = "csv"
    """either choose to ingest data from a csv or from a supabase table"""

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
        logging.info("Reading data from database")
        pass


    def _read_from_csv(self) -> tuple:
        """read data from csv file and return train and test data

        Returns:
            tuple containing train and test data in pandas dataframe
        """

        logging.info("Reading data from csv file")
        df = pd.read_csv(self.data_path)

        logging.info("Saving data to csv file")
        df.to_csv(self.ingestion_config.raw_data_path, index=False)

        return self.ingestion_config.raw_data_path

    def run_ingestion(self) -> str:
        try:
            logging.info("Starting data ingestion")
            if self.ingestion_type == "csv":
                os.makedirs(
                    os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True
                )
                raw_data_path = self._read_from_csv()
                return raw_data_path
            else:
                df = self._read_from_db()

            logging.info("data ingestion completed")


        except Exception as e:
            logging.error(f"Error while ingesting data : {e}")
            raise e
