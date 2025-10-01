from tvb.simulator.lab import *
#import tvb.simulator.lab
from tvb.simulator.plot.tools import *
#import tvb.simulator.plot.tools
import matplotlib.pyplot as plt
import numpy as np

#load connectivity data
sub = connectivity.Connectivity.from_file("/home/dhughe13/TVB_over_sixty/Sub-11017/structural_inputs-11017.zip")
sub.configure()
sub.summary_info

sim_len = 360000
sample = 3000
dim = int(sim_len/sample)

def runsimGN(G_j,N_i):
    model = models.ReducedWongWangExcInh(G=np.array([G_j]))
    sim = simulator.Simulator(
        model=model,
        connectivity=sub,
        coupling=coupling.Linear(a=np.array([1.0])),
        integrator=integrators.HeunStochastic(noise=noise.Additive(nsig=numpy.array([N_i]))),
        monitors=(monitors.Bold(variables_of_interest=numpy.array([0]),period=3000),),
        simulation_length=sim_len
    )
    sim.configure()
    data = sim.run()
    return data

from multiprocessing import Pool

G = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

def f(G):
    N = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    GN_search = np.zeros((len(N),dim,96))

    for i,N_i in enumerate(N):
        (_, y), = runsimGN(G,N_i)
        y_np = np.squeeze(y)
        GN_search[i,:,:] = y_np

    np.save(f'GN_search_full-{G}.npy',GN_search)

with Pool(20) as p:
    print(p.map(f, G))