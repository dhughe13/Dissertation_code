from tvb.simulator.lab import *
#import tvb.simulator.lab
from tvb.simulator.plot.tools import *
#import tvb.simulator.plot.tools
import matplotlib.pyplot as plt
import numpy as np

#load connectivity data
sub = connectivity.Connectivity.from_file("/home/dhughe13/TVB_over_sixty/Sub-10019/structural_inputs-10019.zip")
sub.configure()
sub.summary_info

sim_len = 360000
sample = 3000
dim = int(sim_len/sample)

# G_val = 0.7
# N_val = 1e-3
# Ji_val = 1.1
# JN_val = 0.175

def runsimwp(wp):
    model = models.ReducedWongWangExcInh(G=np.array([0.7]),J_i=np.array([1.1]),J_N=np.array([0.175]),w_p=np.array([wp]))
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

wp_val = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])/0.175

def f(wp):
    wp_search = np.zeros((dim,96))
    (_,y), = runsimwp(wp)
    y_np = np.squeeze(y)
    wp_search[:,:] = y_np

    np.save(f'wp_search_full-{wp}.npy',wp_search)

with Pool(16) as p:
    print(p.map(f,wp_val))

                    