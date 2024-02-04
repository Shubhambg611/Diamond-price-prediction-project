import numpy as np
import sys
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import pickle
from src.DimondPricePrediction.utils.utils import load_object
from src.DimondPricePrediction.exception import customexception
from src.DimondPricePrediction.logger import logging

class ModelEvaluation:
    def __init__(self):
        pass
    
    
    def eval_metrics(self, actual, pred):
        rmse= np.sqrt(mean_squared_error(actual, pred))
        mae= mean_absolute_error(actual,pred)
        r2= r2_score(actual,pred)
        return rmse, mae, r2

    def initiate_model_evaluation(self, train_array, test_array):
        try:
            x_test, y_test= (test_array[:,:-1],test_array[:,-1])

            model_path= os.path.join("artifact","model.pkl")
            model= load_object(model_path)

            mlflow.set_registry_uri("https://dagshub.com/Shubhambg611/Diamond-price-prediction-project.mlflow")

            tracking_url_type_store= urlparse(mlflow.get_tracking_uri()).scheme
            print(tracking_url_type_store)

            with mlflow.start_run():
                predicted_qualities= model.predict(x_test)

                rmse, mae, r2= self.eval_metrics(y_test, predicted_qualities)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("mae", mae)
                mlflow.log_metric("r2", r2)

                # This condition is for the DagsHub!

                if tracking_url_type_store != "file":
                    # Register the model
                    mlflow.sklearn.log_model(model, "model", registered_model_name= "ml_model")
                # This condition is for local
                else:
                    mlflow.sklearn.log_model(model, "model")
        except Exception as e:
            logging.info("Error occured in model evaluation")
            raise customexception (e, sys)