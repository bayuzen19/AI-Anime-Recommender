import pandas as pd

class AnimeDataLoader:
    def __init__(self,original_path:str, processed_path:str):
        self.original_path = original_path
        self.processed_path = processed_path
    
    def load_and_process(self):
        df = pd.read_csv(self.original_path,encoding="utf-8",on_bad_lines='skip').dropna()
        df.columns = [x.lower() for x in df.columns] #lower case pada colomn

        df["combined_info"] = (
            "Title: " + df["name"] + " overview: " + df["sypnopsis"] + " genres " + df["genres"]
        )

        df[["combined_info"]].to_csv(self.processed_path,index=False,encoding="utf-8")

        return self.processed_path


