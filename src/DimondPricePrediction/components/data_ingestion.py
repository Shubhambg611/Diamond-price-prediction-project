import pandas as pd
import numpy as np
from src.DimondPricePrediction.logger import logging
from src.DimondPricePrediction.exception import customexception 

import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path 

class DataIngestionConfig:
    raw_data_path:str=os.path.join("artifact","raw.csv")
    train_data_path:str=os.path.join("artifact","train.csv")
    test_data_path:str=os.path.join("artifact","test.csv")

class DataIngestion:
    def __init__(self):
        self.injection_config=DataIngestionConfig()
    
    def initiate_data_injection(self):
        logging.info("Data injection started")
        
        try:
            data = pd.read_csv(Path(os.path.join("notebooks/data","train.csv")))
            logging.info("read the data set as data frame ")
            
            os.makedirs(os.path.dirname(os.path.join(self.injection_config.raw_data_path)),exist_ok=True)
            data.to_csv(self.injection_config.raw_data_path,index=False)
            logging.info("I have saved the raw data in artifact folder")
            
            
            logging.info("I have now performed train test split")
            
            train_data,test_data = train_test_split(data,test_size=0.25) 
            logging.info("train test split completed")  
            
            train_data.to_csv(self.injection_config.train_data_path,index=False)
            test_data.to_csv(self.injection_config.test_data_path,index=False)
            
            logging.info("Data ingesion part is completed")
            
            return (
                
                self.injection_config.train_data_path,
                self.injection_config.test_data_path
            )
            
        except Exception as e:
            logging.info("excpetion during occured ")
            raise customexception(e,sys)
        
        