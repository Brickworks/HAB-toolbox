import logging
import matplotlib.pyplot as plt

log = logging.getLogger()


def show_figure(save_fig=None):
    ''' Show all plots.

    A simple wrapper for `matplotlib.pyplot.show()`

    Args:
        save_fig (string, optional): Filename to use for a saved figure.
            If not specified, the figure is not saved.
            If no file extension is given, the figure will be saved as a `.png`
    '''
    plt.show()
    if save_fig:
        plt.savefig(save_fig)
        log.warning(f'Plot saved to {save_fig}.png')


def plot_ascent(time,
                altitude,
                velocity,
                acceleration,
                title='',
                show=True,
                save_fig=None):
    ''' Create plots for altitude, velocity, and acceleration over time.

    Expects all input arrays to be the same length. Best results when used
    with `hab_toolbox.cli.simple_ascent` or `hab_toolbox.cli.plot_ascent`.

    Args:
        time (array): Array of time indices.
        altitude (array): Array of altitudes.
            One entry for each time index.
        velocity (array): Array of ascent velocities.
            One entry for each time index. Positive up.
        acceleration (array): Array of ascent accelerations.
            One entry for each time index. Positive up.
        title (string, optional): Plot title. Defaults to `''`.
        show (bool, optional): Whether to display the plots (`True`, default)
            or just create the plot objects and return them (`False`).
        save_fig (string, optional): Filename to use for a saved figure.
            If not specified, the figure is not saved.
            If no file extension is given, the figure will be saved as a `.png`

    Returns:
        tuple: Figure and Axis plot objects.
    '''
    fig, axs = plt.subplots(3, 1)
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
        show_figure(save_fig=save_fig)

    return fig, axs
