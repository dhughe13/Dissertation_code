from tvb.simulator.lab import *
#import tvb.simulator.lab
from tvb.simulator.plot.tools import *
#import tvb.simulator.plot.tools
import matplotlib.pyplot as plt
import numpy as np

#load connectivity data
sub = connectivity.Connectivity.from_file("/home/dhughe13/TVB_over_sixty/Sub-10136/structural_inputs-10136.zip")
sub.configure()
sub.summary_info

sim_len = 360000
sample = 3000
dim = int(sim_len/sample)

# G_val = 0.3
# N_val = 1e-4
# Ji_val = 1.0

def runsimJn(Jn):
    model = models.ReducedWongWangExcInh(G=np.array([0.3]),J_i=np.array([1.0]),J_N=np.array([Jn]))
    sim = simulator.Simulator(
        model=model,
        connectivity=sub,
        coupling=coupling.Linear(a=np.array([1.0])),
        integrator=integrators.HeunStochastic(noise=noise.Additive(nsig=numpy.array([1e-4]))),
        monitors=(monitors.Bold(variables_of_interest=numpy.array([0]),period=3000),),
        simulation_length=sim_len
    )
    sim.configure()
    data = sim.run()
    return data

from multiprocessing import Pool

Jn_val = np.array([0.025, 0.075, 0.125, 0.175, 0.225, 0.275, 0.325, 0.375, 0.425, 0.475, 0.5])

def f(Jn):
    Jn_search = np.zeros((dim,96))
    (_,y), = runsimJn(Jn)
    y_np = np.squeeze(y)
    Jn_search[:,:] = y_np

    np.save(f'Jn_search_full-{Jn}.npy',Jn_search)

with Pool(11) as p:
    print(p.map(f,Jn_val))

                    