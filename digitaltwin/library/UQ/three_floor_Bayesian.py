"""
author: Xiaoxue Shen

Bayesian calibration
"""
import arviz as az
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pymc as pm
import pytensor
import pytensor.tensor as pt

from pymc import Interpolated
from numba import njit
from pymc.ode import DifferentialEquation
from pytensor.compile.ops import as_op
from scipy.integrate import odeint
from scipy.optimize import least_squares

from scipy import stats
from scipy.signal import savgol_filter
from scipy import signal

print(f"Running on PyMC v{pm.__version__}")

def Bayesian_output():
    az.style.use("arviz-darkgrid")
    rng = np.random.default_rng(1234)
    # load the data -  please change the path
    path = "./digitaltwin/Data/ODE/"
    # M = np.load(path+"M.npy")
    # K = np.load(path+"K.npy")
    # C = np.load(path+"C.npy")
    tt = np.load(path+"tt.npy")
    xx = np.load(path+"displacements.npy")

    #  Cut the zero values as these may biase the Bayesian approach
    tt_ = tt[int(len(tt)/2)-1:]
    xx_ = xx[:,:,int(len(tt)/2)-1:]

    tt_.shape, xx_.shape

    noise_ = np.array([0.001, 0.001, 0.001])
    for i in range(0, 3):
        xx_[0,i,:] += np.random.normal(loc=0, scale=noise_[i], size=int(len(tt)/2)+1)


    data = pd.DataFrame(dict(time = tt_))

    data.head()
