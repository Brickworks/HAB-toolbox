import logging
import matplotlib.pyplot as plt


def show_figure():
    plt.show()


def plot_ascent(time, altitude, velocity, acceleration, title='', show=True):
    fig, axs = plt.subplots(3,1)
    fig.tight_layout()
    if title:
        fig.suptitle(title)

    axs[0].plot(time, altitude)
    axs[0].set_ylabel('Altitude (m)')

    axs[1].plot(time, velocity)
    axs[1].set_ylabel('Velocity (m/s)')

    axs[2].plot(time, acceleration)
    axs[2].set_ylabel('Acceleration (m/s^2)')

    for ax in axs:
        ax.set_xlabel('Time (s)')
        ax.grid(True)
        ax.set_frame_on(False)

    if show:
        show_figure()

    return fig, axs
