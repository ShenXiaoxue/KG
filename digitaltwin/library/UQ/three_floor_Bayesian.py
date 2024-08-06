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

import sys
sys.stdout.flush()

print(f"Running on PyMC v{pm.__version__}")

def plot_data(ax, data, xx_, lw=2, title="Displacement (m)"):
    ax.plot(data.time, xx_[0,0,:],'.', color="b", lw=lw, markersize=6, label="Floor 1")
    ax.plot(data.time, xx_[0,1,:],'.', color="g", lw=lw, markersize=6, label="Floor 2")
    ax.plot(data.time, xx_[0,2,:],'.', color="r", lw=lw, markersize=6, label="Floor 3")
    
    ax.legend(fontsize=14, loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_xlim([0.5, 1])
    ax.set_xlabel("Time (s)", fontsize=14)
    ax.set_ylabel("Displacement (m)", fontsize=14)
    return ax


class HFORCE():
    def __repr__(self): # return
        return "%s: %f %s"%(self.__kind,self.__amp,self.units)  
    def __str__(self): # print
        return "%s: %f %s"%(self.__kind,self.__amp,self.units)  
    def __init__(self,x=300.0,at_time=0.5,duration=0.05,kind="Hammer"):
        self.__amp = x
        self.__dur = duration
        self.__att = at_time
        self.__kind= kind
        self.units = "N"
    def value(self,t=None):
        if t is None: t = self.__att
        else: t = np.asarray(t,dtype=float)
        return self.__amp * np.exp(-np.power(t - self.__att, 2.) / (2 * np.power(self.__dur, 2.)))
    def toplot(self,N=30,s=5):
        t = np.linspace(self.__att-s*self.__dur,self.__att+s*self.__dur, num=N)
        x = self.value(t=t)
        return t,x


@njit
def rhs(X, t, theta):
    
    x1, x2, x3, xdot1, xdot2, xdot3 = X
    k0, k1, k2 = theta
    # f = HFORCE(duration=1e-2)
    # t = np.linspace(0, 30, 30*2048)
    # equations
    xdotdot1 = -(c0 / m0) * (xdot1) -(c1 / m0) * (xdot1 - xdot2) -(k0 / m0) * x1 -(k1 / m0) * (x1 - x2) + f_[int(t*2048)] / m0 #f.value(t=t)
    xdotdot2 = -(c1 / m1) * (xdot2 - xdot1) -(c2 / m1) * (xdot2 - xdot3) -(k1 / m1) * (x2 - x1) -(k2 / m1) * (x2 - x3)
    xdotdot3 = -(c2 / m2) * (xdot3 - xdot2) -(k2 / m2) * (x3 - x2)  
    return [xdot1, xdot2, xdot3, xdotdot1, xdotdot2, xdotdot3]


# Run the model and make sure the equations are working correctly.
# plot model function
# def plot_model(
#     ax,
#     x_y,
#     time=tt_,
#     alpha=1,
#     lw=3,
#     title="Floor response and\nExample Model Run",
# ):
#     ax.plot(time, x_y[int(len(tt)/2)-1:, 0], color="b", alpha=alpha, lw=lw, label="Floor 1 (Model)")
#     ax.plot(time, x_y[int(len(tt)/2)-1:, 1], color="g", alpha=alpha, lw=lw, label="Floor 2 (Model)")
#     ax.plot(time, x_y[int(len(tt)/2)-1:, 2], color="r", alpha=alpha, lw=lw, label="Floor 3 (Model)")
#     ax.legend(fontsize=14, loc="center left", bbox_to_anchor=(1, 0.5))
#     ax.set_title(title, fontsize=16)
#     return ax


init0 = [0, 0, 0, 0, 0, 0]
f = HFORCE(duration=1e-2)
ts = np.linspace(0, 1, 1*2048) 

f_ = np.zeros(2048)
for i in range(0, 2048):
    f_[i] = f.value(t=i/2048)

# Note here only c1, and c2 are the variables
# m0, m1, m2, k0, k1, k2, c0, c1, c2 = 5.0394, 4.9919, 4.9693, 34958.3691, 43195.1237, 43295.9086,7.8963, 4.0129, 5.4905
m0, m1, m2, c0, c1, c2 = 5.0394, 4.9919, 4.9693, 7.8963, 4.0129, 5.4905

# load the data -  please change the path
path = "./digitaltwin/Data/ODE/"
#path = "/home/shen/KG/KG/digitaltwin/Data/ODE/"
# M = np.load(path+"M.npy")
# K = np.load(path+"K.npy")
# C = np.load(path+"C.npy")
tt = np.load(path+"tt.npy")
xx = np.load(path+"displacements.npy")
#  Cut the zero values as these may biase the Bayesian approach
tt_ = tt[int(len(tt)/2)-1:]
xx_ = xx[:,:,int(len(tt)/2)-1:]

tt_.shape, xx_.shape

    
#decorator with input and output types a Pytensor double float tensors
# @as_op(itypes=[pt.dvector], otypes=[pt.dmatrix])
@as_op(itypes=[pt.dvector], otypes=[pt.dmatrix])
def pytensor_forward_model_matrix(theta):
    results = odeint(func=rhs, y0=init0, t=ts, args=(theta,))
    return np.transpose(results[int(len(tt)/2)-1:,0:3])



def Bayesian_output():
    az.style.use("arviz-darkgrid")
    rng = np.random.default_rng(1234)

    noise_ = np.array([0.001, 0.001, 0.001])
    for i in range(0, 3):
        xx_[0,i,:] += np.random.normal(loc=0, scale=noise_[i], size=int(len(tt)/2)+1)


    data = pd.DataFrame(dict(time = tt_))

    print(data.head())

    # _, ax = plt.subplots(figsize=(12, 4))
    # plot_data(ax, data, xx_)
    # # plt.savefig(path+"Observation.png", dpi=300)
    # plt.show()

    ##############################
    k0, k1, k2 = 34958.3691, 43195.1237, 43295.9086
    theta = np.array([k0, k1, k2])  # m0, m1, m2, k0, k1, k2, c0, c1, c2

    basic_model = pm.Model()
    with basic_model:
        # Priors for unknown model parameters
        k0 = pm.Uniform('k0', lower=30000., upper=50000.)
        k1 = pm.Uniform('k1', lower=30000., upper=50000.)
        k2 = pm.Uniform('k2', lower=30000., upper=50000.)
        sigma = pm.HalfNormal("sigma", 0.1)
        # convert m and c to a tensor vector
        ode_solution  = pytensor_forward_model_matrix(pm.math.stack([k0, k1, k2]))
        # Likelihood 
        pm.Normal("Y_obs", mu=ode_solution, sigma=sigma, observed=xx_[0,:,:])


    #############
    vars_list = list(basic_model.values_to_rvs.keys())[:-1]
    # Specify the sampler
    sampler = "Slice Sampler"
    tune = draws = 2000
    # Inference!
    print("Bayesian inference is running.. wait until it is done!")
    print('\n' * 5)
    with basic_model:
        print("Estimate time: 25 mins..")
        trace = pm.sample(step=[pm.Slice(vars_list)], tune=tune, draws=draws, chains=4, cores=4)

    print("Sampling done.")
    #traces = [trace]



Bayesian_output()
