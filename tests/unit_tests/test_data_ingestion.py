from sociolla.data_pipeline.components.data_ingestion import DataIngestion


def test_data_ingestion():
    tester = DataIngestion()
    path = "/home/redha/Documents/projects/NLP/sociolla_project/sociolla/data/products_all_brands.csv"
    results = tester.init_ingestion(path)
    assert results == '/home/redha/Documents/projects/NLP/sociolla_project/sociolla/artifacts/raw/raw_data.csv'