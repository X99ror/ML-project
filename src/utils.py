import os
import numpy as np
import sys
from src.exception import CustomException
import pandas as pd
import dill 
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
## it helps in creating pickle file 


def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        
    except Exception as e:
        raise CustomException(e,sys)
    

def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report={}
        
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=list(params.values())[i]
            
            grid=GridSearchCV(estimator=model,param_grid=para,cv=3,n_jobs=3)
            grid.fit(X_train,y_train)
            
            model.set_params(**grid.best_params_)
            model.fit(X_train,y_train)
            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)
            
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            report[list(models.keys())[i]]=test_model_score
            
            return report
            
    except Exception as e:
        raise CustomException(e,sys)             
