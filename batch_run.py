
from multiprocessing import Pool
import os
import itertools
from argparse import ArgumentParser


import sys
import os



def run_task(nt, prp, conf, timeout, tidx):
    """
    conf is a dict with:
    abs_mth -   Abstraction method to use
    ref_mth -   Refine method to use
    2_class -   If true, use 2-class
    cl_vecs -   The clustering vector generation method to use
    """
    outname = "outs/Task_{}_net_{}_prp_{}_abs_{}_ref_{}_2c_{}_v_{}.out".format(
        tidx, nt, prp, 
        conf['abs_mth'], 
        conf['ref_mth'],
        conf['2_class'],
        conf['cl_vecs']
    )
    statsname = "stats/Task_{}_net_{}_prp_{}_abs_{}_ref_{}_2c_{}_v_{}.stat".format(
        tidx, nt, prp, 
        conf['abs_mth'], 
        conf['ref_mth'],
        conf['2_class'],
        conf['cl_vecs']
    )
    
    command = "timeout -k 1000s {} python3 complete_verifier/abcrown.py --onnx_path {} --vnnlib_path {} --batch_size {} 2>&1 | tee {}".format(
        timeout, nt, "mnist_relu_6_100_prop/"+prp, 2048, outname
    )
    print("In Thread {0} : {1}".format( tidx, command ))
    os.system(command)

def run_per_cpu( fargs ): 
    tasks, timeout, tidx = fargs
    for nt, prp, conf in tasks:
        run_task(nt, prp, conf, timeout, tidx)



 
if __name__ == '__main__':

    # Set number of cpus, and timeout here
    timeout = 2500
    n_cpu =  15

    # Collect names for all networks
    netnames = [ 
        n for n in os.listdir( "/home/testing/oct22/semantic-neuron-merge/alpha-beta-CROWN" ) if 'mnist_relu_6_100.onnx' in n 
    ]

    # Collect names for all properties
    properties = [ 
        p for p in os.listdir( "/home/testing/oct22/semantic-neuron-merge/alpha-beta-CROWN/mnist_relu_6_100_prop" ) if 'prop' in p and p.endswith('.vnnlib') 
    ]

    print("Network names", netnames)
    print("Properties",properties)

    # Collect configurations
    confs = [
            {
                'abs_mth' : 'saturation',  
                'ref_mth' : 'cegar-hcluster', 
                '2_class' : True,
                'cl_vecs' : 'simulation',
            }, 

    ]

    tasks = itertools.product(netnames, properties, confs)

    # Distribute
    task_per_cpu = [ [] for _ in range(n_cpu) ]
    cpu_idx = 0
    for task in tasks:
        task_per_cpu[ cpu_idx ].append( task )
        cpu_idx += 1
        if cpu_idx >= n_cpu:
            cpu_idx = 0

    #print(task_per_cpu)
    with Pool(processes=len(task_per_cpu)) as p:
        p.map(
            run_per_cpu, 
            ( (tasks, timeout, i) for i,tasks in enumerate(task_per_cpu) )
        )
    

