""" 
Author: Karthik Arumugam
Email: karthik131100@gmail.com
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib
import os
from matplotlib.colors import ListedColormap 
import logging 

plt.style.use('fivethirtyeight') # Style of graphs

 
def prepare_data(df):
  """It is used to seperate the dependant(y) and independent(x) labels/data        

  Args:
      df (pd.DataFrame): It is used to create a pandas dataframe

  Returns:
      tuple: returns the tuples of the dependent and independent labels/data/variables 
  """
  logging.info("Preparing the data by segregating the dependent and independent variables")
  X = df.drop("y",axis=1)

  y = df["y"] 

  return X,y



def save_model(model, filename):
  """It is used to save the trained model 

  Args:
      model (python object): It is a trained model
      filename (string/str ): Path to save the trained model
  """
  logging.info("Saving the trained model")
  model_dir = "models"
  os.makedirs(model_dir, exist_ok=True) # ONLY CREATE IF MODEL_DIR DOESN"T EXISTS
  filePath = os.path.join(model_dir, filename) # model/filename
  joblib.dump(model, filePath)
  logging.info(f"Svaed the model at {filePath}") #print(filePath) - using logging as an alterntaive to print
  


def save_plot(df, file_name, model):
  """
  :param df: It is pandas dataframe 
  :param file_name: It is the path to save the plot 
  :param model: It is the trained model

  """
  def _create_base_plot(df):
    logging.info("Creating the base plot")
    df.plot(kind="scatter", x="x1", y="x2", c="y", s=100, cmap="winter")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)
    plt.axvline(x=0, color="black", linestyle="--", linewidth=1)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(10, 8)

  def _plot_decision_regions(X, y, classfier, resolution=0.02):
    logging.info("Plotting the decision regions/boundaries")
    colors = ("red", "blue", "lightgreen", "gray", "cyan")
    cmap = ListedColormap(colors[: len(np.unique(y))])

    X = X.values # as a array
    x1 = X[:, 0] 
    x2 = X[:, 1]
    x1_min, x1_max = x1.min() -1 , x1.max() + 1
    x2_min, x2_max = x2.min() -1 , x2.max() + 1  

    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution), 
                           np.arange(x2_min, x2_max, resolution))
    Z = classfier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contourf(xx1, xx2, Z, alpha=0.2, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    plt.plot() 



  X, y = prepare_data(df)

  _create_base_plot(df)
  _plot_decision_regions(X, y, model)

  plot_dir = "plots"
  os.makedirs(plot_dir, exist_ok=True) # ONLY CREATE IF MODEL_DIR DOESN"T EXISTS
  plotPath = os.path.join(plot_dir, file_name) # model/filename
  plt.savefig(plotPath) 
  logging.info(f"Saving the plot at: {plotPath}")