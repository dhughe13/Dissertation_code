from tvb.simulator.lab import *
#import tvb.simulator.lab
from tvb.simulator.plot.tools import *
#import tvb.simulator.plot.tools
import matplotlib.pyplot as plt
import numpy as np

#load connectivity data
sub = connectivity.Connectivity.from_file("/home/dhughe13/TVB_over_sixty/Sub-11039/structural_inputs-11039.zip")
sub.configure()
sub.summary_info

sim_len = 360000
sample = 3000
dim = int(sim_len/sample)

def runsimJi(Ji):
    model = models.ReducedWongWangExcInh(G=np.array([0.5]),J_i=np.array([Ji]))
    sim = simulator.Simulator(
        model=model,
        connectivity=sub,
        coupling=coupling.Linear(a=np.array([1.0])),
        integrator=integrators.HeunStochastic(noise=noise.Additive(nsig=numpy.array([1e-3]))),
        monitors=(monitors.Bold(variables_of_interest=numpy.array([0]),period=3000),),
        simulation_length=sim_len
    )
    sim.configure()
    data = sim.run()
    return data

from multiprocessing import Pool

Ji_val = np.array([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6])

def f(Ji):
    Ji_search = np.zeros((dim,96))
    (_,y), = runsimJi(Ji)
    y_np = np.squeeze(y)
    Ji_search[:,:] = y_np

    np.save(f'Ji_search_full-{Ji}.npy',Ji_search)

with Pool(23) as p:
    print(p.map(f,Ji_val))

                    