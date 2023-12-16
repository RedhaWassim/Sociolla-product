from pydantic import BaseModel
from sociolla.utils.utils import retreive_base_path
from pathlib import Path
from typing import Optional
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sociolla.machine_learning.components.transformation import ColumnDropper, NullDropper, PriceRangeTransformer, CategoriesTransformer, RatingTransformer

class DataTransformationConfig(BaseModel):
    retreive_base_path: str = retreive_base_path()
    raw_data_path: str = str(Path(retreive_base_path, f"artifacts/transformed/raw_data.csv"))
    product_data_path: str = str(Path(retreive_base_path, f"artifacts/transformed/product_data.csv"))
    rating_data_path: str = str(Path(retreive_base_path, f"artifacts/transformed/rating_data.csv"))

    class ConfigDict:
        """pydantic forbidding extra parameters"""
        extra = "forbid"

class DataTransformation(BaseModel):
    pass