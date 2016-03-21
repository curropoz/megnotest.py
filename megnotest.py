def simulation(par):
    a, i = par # unpack parameters
    sim = rebound.Simulation()
    sim.integrator = "whfast"
    sim.integrator_whfast_safe_mode = 0
    sim.dt = 5.
    sim.add(m=1.) # Star
    sim.add(m=0.000954, a=5.204, M=0.600, omega=0.257, e=0.048)
    sim.add(m=0.000285, a=a, M=0.871, omega=1.616, e=0.065,i=i)
    sim.move_to_com()

    sim.init_megno(1e-8)
    sim.exit_max_distance = 20.
    try:
        sim.integrate(5e2*2.*np.pi, exact_finish_time=0) # integrate for 500 years, integrating to the nearest
        #timestep for each output to keep the timestep constant and preserve WHFast's symplectic nature
        megno = sim.calculate_megno()
        return megno
    except rebound.Escape:
        return 10. # At least one particle got ejected, returning large MEGNO.

import rebound
import numpy as np
print simulation((7,0.1))

Ngrid = 10
par_a = np.linspace(7.,10.,Ngrid)
par_i = np.linspace(0.,0.5,Ngrid)
parameters = []
for e in par_i:
    for a in par_a:
        parameters.append((a,i))
from rebound.interruptible_pool import InterruptiblePool
pool = InterruptiblePool()
results = pool.map(simulation,parameters)


results2d = np.array(results).reshape(Ngrid,Ngrid)
#%matplotlib inline
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,5))
ax = plt.subplot(111)
extent = [min(par_a),max(par_a),min(par_i),max(par_i)]
ax.set_xlim(extent[0],extent[1])
ax.set_xlabel("semi-major axis $a$")
ax.set_ylim(extent[2],extent[3])
ax.set_ylabel("inclination $i$")
im = ax.imshow(results2d, interpolation="none", vmin=1.9, vmax=4, cmap="jet", origin="lower", aspect='auto', extent=extent)
cb = plt.colorbar(im, ax=ax)
cb.set_label("MEGNO $\\langle Y \\rangle$")


plt.savefig('megnoai.png',
                  bbox_inches='tight', # Elimina margenes en blanco
                  dpi=200)             # DPI = puntos por pulgada




