import matplotlib.pyplot as plt
import numpy as np

DRAW_LABELS = True

# define coordinates, phase (x) and height (z)
x = np.arange(0, 4 * np.pi + 1e-3, 1e-3)
z = np.arange(-1, 0 + 1e-3, 1e-3)
U = 2 * np.pi * np.exp(6 * z)

# effective depths and currents
zeff = [0, -0.2, -0.8, -0.5]
Ueff = [np.mean(U[z >= zeff[n]]) for n in range(len(zeff))]

# compute interface
eta_no_waves = np.zeros((x.size))
eta_windsea = 0.02 * np.sin(8 * x)
eta_swell = 0.1 * np.sin(x)
modulation = 0.5 * (np.sin(x - 0.25 * np.pi) + 1) 
eta_mixed = eta_swell + modulation * eta_windsea

fig = plt.figure(figsize=(8, 6))
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax2 = plt.subplot2grid((2, 2), (0, 1))
ax3 = plt.subplot2grid((2, 2), (1, 0))
ax4 = plt.subplot2grid((2, 2), (1, 1))
axes = [ax1, ax2, ax3, ax4]

# water interface
for n, eta in enumerate([eta_no_waves, eta_windsea, eta_swell, eta_mixed]):
    axes[n].plot(x, eta, lw=2, color='tab:blue', zorder=1)

# current vectors
for ax in axes:
    for zz in np.arange(0, -1.05, -0.05):
        ax.arrow(np.pi, zz, U[np.argmin((z - zz)**2)], 0, color='k',
                 width=0.002, head_width=0.02, head_length=0.2, zorder=2)

def draw_arrow(ax, zeff, dx):
    arrow_start_x = np.pi
    width = np.abs(0.5 * zeff)
    head_width = 2 * width
    head_length = 0.5 * dx
    ax.arrow(arrow_start_x, zeff / 2, 0.5 * dx, 0, facecolor='c', linewidth=2, edgecolor='k',
             width=width, head_width=head_width, head_length=head_length, zorder=3)

ax1.arrow(np.pi, 0, Ueff[0], 0, facecolor='c', linewidth=2, edgecolor='k',
          width=0.04, head_width=0.1, head_length=0.5, zorder=3)

for n in range(1, 4):
    draw_arrow(axes[n], zeff[n], Ueff[n])
    axes[n].plot(x, zeff[n] * np.ones(x.shape), 'k--')

if DRAW_LABELS:
    for n in range(4):
        axes[n].text(0, zeff[n], r'$\mathcal{Z}_{eff}$', fontsize=16, ha='right', va='center')
        if n == 0:
            axes[n].text(2 * np.pi, 0.05, r'$\mathcal{U}_{eff}$', fontsize=16, ha='center', va='bottom', zorder=3)
        else:
            axes[n].text(0.9 * np.pi, zeff[n] / 2, r'$\mathcal{U}_{eff}$', fontsize=16, ha='right', va='center', zorder=3)
    
    ax1.text(1.3 * np.pi, - 0.4, r'$\mathcal{U}(\mathit{z})$', fontsize=16, ha='left', va='center', zorder=3)
    ax2.text(1.3 * np.pi, - 0.4, r'$\mathcal{U}(\mathit{z})$', fontsize=16, ha='left', va='center', zorder=3)
    ax3.text(2 * np.pi, - 0.15, r'$\mathcal{U}(\mathit{z})$', fontsize=16, ha='left', va='top', zorder=3)
    ax4.text(2 * np.pi, - 0.15, r'$\mathcal{U}(\mathit{z})$', fontsize=16, ha='left', va='top', zorder=3)

    ax1.set_title('No waves')
    ax2.set_title('Young windsea')
    ax3.set_title('Swell')
    ax4.set_title('Mixed sea')

for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(-1, 0.3)

plt.savefig('Ueff_diagram.svg')
plt.savefig('Ueff_diagram.png', dpi=200)
