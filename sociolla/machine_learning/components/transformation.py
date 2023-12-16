from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop

    def fit(self, X, y=None):
        return self

    def transform(self, X, **transform_params):
        return X.drop(columns=self.columns_to_drop)

class NullDropper(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, **transform_params):
        X.dropna(subset=X.columns, inplace=True)
        X.reset_index(drop=True, inplace=True)
        return X
    

class PriceRangeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, price_column):
        self.price_column = price_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, **transform_params):
        X[self.price_column] = (
            X[self.price_column]
            .str.replace("Rp", "")
            .str.replace(".", "")
            .str.replace(" ", "")
            .apply(lambda x: sum(map(int, x.split("-"))) / len(x.split("-")))
        )
        return X


class CategoriesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, categories_column):
        self.categories_column = categories_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, **transform_params):
        category_columns = X[self.categories_column].str.split(";", expand=True).apply(lambda x: x.str.strip())

        category_columns[1].fillna(category_columns[0], inplace=True)
        category_columns[2].fillna(category_columns[0], inplace=True)

        category_columns.columns = [f"{self.categories_column}1", f"{self.categories_column}2", f"{self.categories_column}3"]

        X = pd.concat([X, category_columns], axis=1)
        X.drop(self.categories_column, axis=1, inplace=True)

        return X


class RatingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, rating_column):
        self.rating_column = rating_column

    def fit(self, X, y=None):
        return self

    def transform(self, X, **transform_params):
        def extract_ratings(value):
            try:
                elements = value.split(";")
                ratings = {}
                for element in elements:
                    sub_elements = element.split(":")
                    key = sub_elements[0].strip(' "')
                    value = float(sub_elements[1])
                    ratings[key] = value

                return ratings
            except:
                return {
                    "star_value_for_money": 0,
                    "star_long_wear": 0,
                    "star_texture": 0,
                    "star_quality": 0,
                    "star_eficiency": 0,
                    "star_durability": 0,
                    "star_scent": 0,
                    "star_pigmentation": 0,
                    "star_packaging": 0,
                    "star_effectiveness": 0,
                }

        default_values = {
            "star_value_for_money": 0,
            "star_long_wear": 0,
            "star_texture": 0,
            "star_quality": 0,
            "star_eficiency": 0,
            "star_durability": 0,
            "star_scent": 0,
            "star_pigmentation": 0,
            "star_packaging": 0,
            "star_effectiveness": 0,
        }
        X[self.rating_column] = X[self.rating_column].apply(lambda x: {**default_values, **extract_ratings(x)})

        X = pd.concat([X, X[self.rating_column].apply(pd.Series)], axis=1)
        X.drop(columns=[self.rating_column, "average_rating_by_types", "rating_types_str"], axis=1, inplace=True)

        return X
