import matplotlib.pyplot as plt
import numpy as np

DRAW_LABELS = True

# define coordinates, phase (x) and height (z)
x = np.arange(0, 4 * np.pi + 1e-3, 1e-3)
z = np.arange(-0.5, 0 + 1e-3, 1e-3)
U = 2 * np.pi * np.exp(6 * z)

# effective depths and currents
zeff = [0, -0.2, -0.4]
Ueff = [np.mean(U[z >= zeff[n]]) for n in range(len(zeff))]

# compute interface
eta_no_waves = np.zeros((x.size))
eta_windsea = 0.01 * np.sin(8 * x)
eta_swell = 0.02 * np.sin(2 * x)
modulation = 0.5 * (np.sin(2 * x - 0.25 * np.pi) + 1) 
eta_mixed = eta_swell + modulation * eta_windsea

fig = plt.figure(figsize=(14, 4))
ax1 = plt.subplot2grid((1, 3), (0, 0))
ax2 = plt.subplot2grid((1, 3), (0, 1))
ax3 = plt.subplot2grid((1, 3), (0, 2))
axes = [ax1, ax2, ax3]

# water interface
for n, eta in enumerate([eta_no_waves, eta_windsea, eta_mixed]):
    axes[n].plot(x, eta, lw=2, color='tab:blue', zorder=1)

# current vectors
for ax in axes:
    for zz in np.linspace(0, z[0], 20):
        ax.arrow(np.pi, zz, U[np.argmin((z - zz)**2)], 0, color='k',
                 width=0.001, head_width=0.01, head_length=0.2, zorder=2)

def draw_arrow(ax, zeff, dx):
    arrow_start_x = np.pi
    width = np.abs(0.5 * zeff)
    head_width = 2 * width
    head_length = 0.5 * dx
    ax.arrow(arrow_start_x, zeff / 2, 0.5 * dx, 0, facecolor='c', linewidth=2, edgecolor='k',
             width=width, head_width=head_width, head_length=head_length, zorder=3, alpha=0.7)

ax1.arrow(np.pi, 0, Ueff[0], 0, facecolor='c', linewidth=2, edgecolor='k',
          width=0.02, head_width=0.05, head_length=0.5, zorder=3, alpha=0.7)

for n in range(1, 3):
    draw_arrow(axes[n], zeff[n], Ueff[n])
    axes[n].plot(x, zeff[n] * np.ones(x.shape), 'k--')

if DRAW_LABELS:
    ax1.text(2 * np.pi, 0.02, r'$\mathcal{U}_0$', fontsize=20, ha='center', va='bottom', zorder=3)
    for n in range(1, 3):
        axes[n].text(0.1, zeff[n] - 0.02, r'$\mathcal{Z}(k)$', fontsize=20, ha='left', va='top')
        axes[n].text(0.9 * np.pi, zeff[n] / 2, r'$\mathcal{U}_{form}$', fontsize=20, ha='right', va='center', zorder=3)
    
    ax1.text(1.3 * np.pi, - 0.4, r'$\mathcal{U}(\mathit{z})$', fontsize=20, ha='left', va='center', zorder=3)
    ax2.text(1.3 * np.pi, - 0.4, r'$\mathcal{U}(\mathit{z})$', fontsize=20, ha='left', va='center', zorder=3)
    ax3.text(2.3 * np.pi, - 0.1, r'$\mathcal{U}(\mathit{z})$', fontsize=20, ha='left', va='top', zorder=3)

    titles = ['No waves', 'Young windsea', 'Mature windsea']
    panel_labels = ['A', 'B', 'C']
    for n, ax in enumerate(axes):
        ax.set_title(titles[n], fontsize=16)
        ax.text(0.02, 1.01, panel_labels[n], transform=ax.transAxes, ha='left', va='bottom', fontsize=16)

for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(z[0], 0.2)

for ax in axes[1:]:
    ax.plot([x[0], x[-1]], [0, 0], 'k:')

fig.tight_layout()

filename = 'Ueff_diagram'
if not DRAW_LABELS:
    filename += '_nolabels'

for ext in ['pdf', 'png', 'svg']:
    plt.savefig(filename + '.' + ext)
