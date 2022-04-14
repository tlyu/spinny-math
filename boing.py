# %%
#%matplotlib widget
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from scipy import signal

plt.style.use('dark_background')
fig, ax = plt.subplots()
#fig.patch.set_alpha(0)
fig.set_size_inches(4, 4)
plt.subplots_adjust(0, 0, 1, 1)
#ax.patch.set_alpha(0)
ax.set_axis_off()
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect(1)


ncycles = 20
nsamp = 200
t = np.linspace(0, 2*np.pi, nsamp)

l = []
for i in range(ncycles):
    # Cheap phosphor decay simulation
    alpha = 0.1 + (0.8 * i/ncycles)
    zorder = 2+0.1*i/ncycles
    l.extend(ax.plot([], [], color='#3fcfff', alpha=alpha, zorder=zorder, animated=True))


def get_data1(th):
    bend = 1.000
    f0 = .2001
    f = 20*f0*bend
    fy = .005*f0
    yrot = np.exp(1j*fy*th)
    fill = np.exp(1j*f*th)
    fill.real *= yrot.imag
    saw = signal.sawtooth(f0*th, .5) * yrot.real
    sq = .5 + .5*signal.square(f0*th)
    z = .3*fill*sq + .7*saw
    fz = .002*f0
    zro = .2
    zrot = np.exp(1j*fz*th)
    z = zrot*(zro + (1-zro)*z)
    return (z.real, z.imag)

def get_data(th):
    bend = 1.000
    f0 = .2001
    f = 20*f0*bend
    # Y-axis "rotation"
    fy = .004*f0
    yrot = np.exp(1j*fy*th)
    # "Fill" waveform
    fill = np.exp(1j*f*th)
    fill.real *= yrot.imag
    # Outer circle
    circ = np.exp(1j*f0*th)
    circ.real *= yrot.real
    # Offset of square wave
    sqo = .5
    # Square wave to cut off "retrace"
    sq = sqo+(1-sqo)*signal.square(f0*th)
    z = fill * circ.imag * sq
    #z += fill.conjugate() * circ.imag * (1-sq)
    z += circ.real
    fz = .002*f0
    zro = 0.4
    zrot = np.exp(1j*fz*th)
    z = zrot*(zro + (1-zro)*z)
    return (z.real, z.imag)

def update(data):
    for i in range(ncycles):
        offset = 2*np.pi*(data*(ncycles//2)+i)
        x, y = get_data(t+offset)
        l[i].set_data(x, y)
    return l

#anim = FuncAnimation(fig, update, 250, interval=50, blit=True)
anim = FuncAnimation(fig, update, interval=50, blit=True)
plt.show()
#plt.close()
#anim.save('boing.webp', codec='webp')
#from IPython.display import HTML
#HTML(anim.to_jshtml())
# %%
