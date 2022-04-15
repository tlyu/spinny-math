# %%
#%matplotlib widget
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from scipy import signal

# %%
# Sine wave inscribed in a circle
plt.style.use('default')
fig, ax = plt.subplots()
ax.set_aspect(1)
t = np.linspace(0, 2*np.pi, 1000)
x = np.cos(t)
y = np.sin(t) * np.sin(20*t) * 0.5 * (1 + signal.square(t))
ax.add_patch(mpl.patches.Circle((0,0), 1, fc='none', ec='0.5', ls='--'))
plt.plot(x, y)
# plt.savefig('circle-sine.png')
plt.show()

# %%
# Spherical spring

# Figure setup for animation
plt.style.use('dark_background')
fig, ax = plt.subplots()
fig.set_size_inches(3, 3)
plt.subplots_adjust(0, 0, 1, 1)
ax.set_axis_off()
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect(1)

# Use a list of Lines2D objects to draw curve segments with different alpha,
# to simulate phosphor decay on a CRT.
ncycles = 3
nsamp = 2000
t = np.linspace(0, 2*np.pi, nsamp)

# Set up the Lines2D objects
l = []
for i in range(ncycles):
    alpha = 0.5 ** (ncycles - i - 1)
    zorder = 2 + 0.1 * i/ncycles
    l.extend(ax.plot([], [], color='#3fcfff', alpha=alpha, zorder=zorder, animated=True))

def get_data(th, fnum):
    # The actual math: two quadrature sine waves (`circ` and `fill`)
    # along with a quadrature sine wave each for y-axis and z-axis rotation.
    # Also a square wave to cut off the "retrace" to avoid a crowded mess
    # when the sphere envelope sine wave goes into its negative half-cycle.

    # Fundamental frequency (excluding slow rotations)
    f0 = 1.00
    # Frequency of "fill" waveform
    f = 20 * f0
    # Y-axis rotation
    fy = 0.005
    # Use discrete rotation steps, so the figure closes during each frame
    yrot = np.exp(1j*2*np.pi * fy * fnum)
    # Outer circle of sphere to create an envelope
    circ = np.exp(1j*f0*th)
    # Modulate x-axis to get y-axis rotation
    circ.real *= yrot.real
    # "Fill" waveform, modulated by sphere envelope
    fill = np.exp(1j*f*th) * circ.imag
    # Modulate x-axis to get y-axis rotation
    fill.real *= yrot.imag
    # Replace the above line with the following to see a failed attempt
    # fill.real *= yrot.real
    # Offset of square wave
    sqo = 0.5
    # Square wave to cut off "retrace"
    sq = sqo + (1 - sqo) * signal.square(f0*th)
    z = fill * sq + circ.real
    # Offset for z-axis rotation, to orbit instead of spinning in place
    zroff = 0.4
    # Z-axis rotation
    fz = 0.005
    # Use discrete rotation steps, so the figure closes during each frame
    zrot = np.exp(1j*2*np.pi * fz * fnum)
    z = zrot*(zroff + (1 - zroff) * z)
    return (z.real, z.imag)

def init_data():
    # Pre-fill "negative" time, so looping the animation looks a bit better
    for i in range(ncycles):
        fnum = i - ncycles + 1
        x, y = get_data(t + 2*np.pi * fnum, fnum)
        l[i].set_data(x, y)
    return l

def update(data):
    if data == 0:
        # Initialization is a little tricky and gets its own function
        return init_data()
    # Shift existing data points to lower alpha segments
    for i in range(ncycles - 1):
        l[i].set_data(l[i+1].get_data())
    offset = 2*np.pi*(data)
    x, y = get_data(t+offset, data)
    l[-1].set_data(x, y)
    return l

# anim = FuncAnimation(fig, update, 200, interval=50, blit=True)
anim = FuncAnimation(fig, update, interval=50, blit=True)
# anim.save('boing-opt.gif', dpi=100, extra_args=['-filter_complex','split[a][b];[a] palettegen=max_colors=16 [p];[b][p] paletteuse'])
# anim.save('boing.gif')
# anim.save('boing.mp4')
plt.show()

# Comment out the plt.show() and uncomment the following to embed the
# animation in a Jupyter notebook

# plt.close()
# from IPython.display import HTML
# HTML(anim.to_jshtml())

# %%
