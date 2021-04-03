import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 4 * np.pi + 1e-3, 1e-3)

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

ax1.plot(x, eta_no_waves, lw=3, c='tab:blue')
ax2.plot(x, eta_windsea, lw=3, c='tab:blue')
ax3.plot(x, eta_swell, lw=3, c='tab:blue')
ax4.plot(x, eta_mixed, lw=3, c='tab:blue')

def draw_arrow(ax, zeff, dx):
    arrow_start_x = 3 / 2 * np.pi
    width = np.abs(0.5 * zeff)
    head_width = 2 * width
    head_length = 2 * head_width
    ax.arrow(arrow_start_x, zeff / 2, dx, 0, facecolor='c', linewidth=1, edgecolor='k',
             width=width, head_width=head_width, head_length=head_length, zorder=2)

zeff1 = -0.0
zeff2 = -0.4
zeff3 = -0.8
zeff4 = -0.6

ax1.arrow(np.pi, 0, 2 * np.pi, 0, facecolor='c', linewidth=2, edgecolor='k',
         width=0.04, head_width=0.1, head_length=0.5, zorder=3)

draw_arrow(ax2, zeff2, 1.0 * np.pi)
draw_arrow(ax3, zeff3, 0.5 * np.pi)
draw_arrow(ax4, zeff4, 0.8 * np.pi)

ax2.plot(x, zeff2 * np.ones(x.shape), 'k--')
ax3.plot(x, zeff3 * np.ones(x.shape), 'k--')
ax4.plot(x, zeff4 * np.ones(x.shape), 'k--')

ax1.text(0, zeff1, r'$\mathcal{Z}_{eff}$', fontsize=16, ha='right', va='center')
ax2.text(0, zeff2, r'$\mathcal{Z}_{eff}$', fontsize=16, ha='right', va='center')
ax3.text(0, zeff3, r'$\mathcal{Z}_{eff}$', fontsize=16, ha='right', va='center')
ax4.text(0, zeff4, r'$\mathcal{Z}_{eff}$', fontsize=16, ha='right', va='center')

ax1.text(2 * np.pi, zeff1 / 2, r'$\mathcal{U}_{eff}$', fontsize=16, ha='center', va='bottom', zorder=3)
ax2.text(2 * np.pi, zeff2 / 2, r'$\mathcal{U}_{eff}$', fontsize=16, ha='center', va='center', zorder=3)
ax3.text(2 * np.pi, zeff3 / 2, r'$\mathcal{U}_{eff}$', fontsize=16, ha='center', va='center', zorder=3)
ax4.text(2 * np.pi, zeff4 / 2, r'$\mathcal{U}_{eff}$', fontsize=16, ha='center', va='center', zorder=3)

ax1.set_title('No waves')
ax2.set_title('Young windsea')
ax3.set_title('Swell')
ax4.set_title('Mixed sea')

for ax in [ax1, ax2, ax3, ax4]:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(-1, 0.3)
    ax.plot([np.min(x), np.max(x)], [0, 0], 'k:')

plt.savefig('Ueff_diagram.svg')
plt.savefig('Ueff_diagram.png', dpi=200)
