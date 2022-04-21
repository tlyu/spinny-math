import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

from matplotlib.animation import FuncAnimation

class VectorScope:
    def __init__(self, get_data, ncycles=3):
        self.ncycles = ncycles
        self.get_data = get_data
        self._fig_setup()
        self._anim()
 
    def _fig_setup(self):
        with mpl.style.context('dark_background'):
            fig = plt.figure(figsize=(3, 3))
            ax = fig.add_axes((0,0,1,1), aspect=1)
            ax.set_axis_off()
            ax.axis((-1.1, 1.1, -1.1, 1.1))
            self._fig, self._ax = fig, ax
            self._lines_setup()

    def _lines_setup(self):
        # Use a list of Lines2D objects to draw curve segments with different
        # alpha value, to simulate phosphor decay on a CRT.
        lines = []
        alphas = []
        zorders = []
        ax, ncycles = self._ax, self.ncycles
        # Compute a base for exponential to produce a target lowest alpha
        b = math.exp(math.log(0.1)/(ncycles-1))
        for i in range(ncycles):
            alpha = b ** (ncycles - i - 1)
            alphas.append(alpha)
            zorder = 2 + 0.2 * i/ncycles
            zorders.append(zorder)
            plines = ax.plot([], [], color='#3fcfff',
                alpha=alpha, zorder=zorder)
            lines.extend(plines)
        self._lines = lines
        self._alphas = alphas
        self._zorders = zorders

    def _init_data(self):
        # Pre-fill "negative" time, so looping the animation looks a bit better
        lines, ncycles = self._lines, self.ncycles
        for i in range(ncycles):
            fnum = i - ncycles + 1
            x, y = self.get_data(fnum)
            lines[i].set_data(x, y)
        return lines

    def _update(self, data):
        if (data == 0):
            return self._init_data()
        # Shift existing data points to lower alpha segments
        lines = self._lines
        alphas, zorders = self._alphas, self._zorders
        lines.append(lines.pop(0))
        for i in range(self.ncycles):
            lines[i].set(alpha=alphas[i], zorder=zorders[i])
        x, y = self.get_data(data)
        lines[-1].set_data(x, y)
        self._fig.canvas.toolbar.set_message("%.3g FPS" % (self._cnt/(time.time()-self._tstart)))
        self._cnt += 1
        return lines

    def _init_func(self):
        self._tstart = time.time()
        self._cnt = 0
        return []

    def _anim(self):
        self.anim = FuncAnimation(self._fig, self._update, init_func=self._init_func, interval=50, blit=True)

if __name__ == '__main__':
    import numpy as np

    nsamp = 300
    t = np.linspace(0, 2*np.pi, nsamp)
    def get_data_rose(fnum):
        bend = 1.005
        th = t + 2*np.pi * fnum
        f0 = 1.008
        f = 3 * f0 * bend
        fm = 0.01
        r = 0.5 + 0.5 * np.sin(fm*th)
        z = np.exp(1j*f0*th) * (r + (1-r) * np.exp(1j*f*th))
        return (np.real(z), np.imag(z))

    vs = VectorScope(get_data_rose)
    plt.show()
