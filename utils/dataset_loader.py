import pandas as pd

class DatasetLoader:
    def load(self, path):
        return pd.read_csv(path).to_dict('records')
