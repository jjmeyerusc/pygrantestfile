from pygran import simulation
from pygran.params import organic, glass

params = {
    # Define the system
    'boundary': ('f','f','f'),
    'box':  (-1e-3, 1e-3, -1e-3, 1e-3, 0, 4e-3),

    # Define component(s)
    'species': ({'material': organic, 'radius': ('constant', 5e-5)},),

    # Setup I/O params
    'traj': {'freq': 1000, 'style': 'vtk', 'pfile': 'particles*.vtk', 'mfile': 'mesh*.vtk'},


    # Output dir name
        'output': 'DEM_flow',

    # Define computational parameters
    'dt': 1e-6,

    # Apply a gravitional force in the negative direction along the z-axis
    'gravity': (9.81, 0, 0, -1),

    # Import hopper + impeller mesh
     'mesh': {
        'hopper': {'file': 'mesh/silo.stl', 'mtype': 'mesh/surface', 'material': glass, \
                   'args': {'scale': 1e-3}},
        'impeller': {'file': 'mesh/valve.stl', 'mtype': 'mesh/surface', 'material': glass, \
                     'args': {'move': (0, 0, 1.0), 'scale': 1e-3}},
    },

    # Stage runs
    'stages': {'insertion': 1e5, 'run': 1e5},
}




# STEP 2: SIMULATION
# The params dictionry is then used to create a DEM class and run the simulation. By default, the unit system used is S.I.

# Create an instance of the DEM class
sim = simulation.DEM(**params)

# Setup a primitive static wall (stopper) along the xoy plane at z=0 of material propreties defined in species 1
stopper = sim.setupWall(species=1, wtype='primitive', plane = 'zplane', peq = 0.0)

# Insert particles every 1e4 steps in a rectangular region of length/width 1e-3 m and height 1e-3 m. Insertion is done here based on region volume fraction approaching 1.0
insert = sim.insert(species=1, region=('block', -5e-4, 5e-4, -5e-4, 5e-4, 2e-3, 3e-3), mech='volumefraction_region', value=1, freq=1e2)

# Run simulation for 1e5 steps then stop insertion
sim.run(params['stages']['insertion'], params['dt'])
sim.remove(insert)

# Rotate the impeller along the z-axis around the origin and of period 5e-2 s.
rotImp = sim.moveMesh('impeller', rotate=('origin', 0, 0, 0), axis=(0, 0, 1), period=5e-2)

# Blend the system by running for 1e5 steps then stop impeller rotation
sim.run(params['stages']['run'], params['dt'])
sim.remove(rotImp)

# Remove stopper then run the system for another 1e5 steps (flow stage)
sim.remove(stopper)
sim.run(params['stages']['run'], params['dt'])




# OUTPUT/VISUALIZATION
# Play output video









# The following program prints "Hello World"\'94\"
print("Let's GO LAKERS!")
