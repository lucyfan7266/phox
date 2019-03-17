import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from neurophox.helpers import get_alpha_checkerboard

DARK_RED = (0.7, 0, 0)
DARK_ORANGE = (0.7, 0.35, 0)
DARK_BLUE = (0, 0.2, 0.6)
LIGHT_BLUE = (0.5, 0.6, 0.8)
DARK_GREEN = (0, 0.4, 0)
GRAY = (0.5, 0.5, 0.5)
DARK_PURPLE = (0.4, 0, 0.6)
LIGHT_PURPLE = (0.7, 0.5, 0.8)


def get_checkerboard_points(dim, rank):
    checkerboard = np.zeros((dim - 1, rank))
    checkerboard[::2, ::2] = checkerboard[1::2, 1::2] = 1
    return np.where(checkerboard == 1)


def get_triangular_mesh_points(dim):
    checkerboard = np.zeros((dim - 1, dim * 2))
    checkerboard[::2, ::2] = checkerboard[1::2, 1::2] = 1
    triangular_mask = np.hstack([
        np.fliplr(np.tril(np.ones((dim - 1, dim)))),
        np.tril(np.ones((dim - 1, dim)))
    ])
    return np.where((checkerboard == 1) * triangular_mask)


def get_triangular_mesh_alpha(dim):
    checkerboard = np.zeros((dim - 1, dim * 2))
    checkerboard[::2, ::2] = checkerboard[1::2, 1::2] = 1
    triangular_mask = np.hstack([
        np.fliplr(np.tril(np.ones((dim - 1, dim)))),
        np.tril(np.ones((dim - 1, dim)))
    ])
    alpha_rows = np.repeat(np.linspace(dim - 1, 1, dim - 1)[:, np.newaxis], dim * 2, axis=1)
    return alpha_rows * triangular_mask * checkerboard


def get_simulated_xi_histogram_from_theta(theta_samples: np.ndarray, alpha: int, num_bins: int, normed: bool=True):
    xi_freqs, xis = np.histogram(np.power(np.cos(theta_samples), 2 * alpha), bins=num_bins, normed=normed)
    return xis[1:], xi_freqs


def get_simulated_theta_histogram_from_xi(xi_samples: np.ndarray, alpha: int, num_bins: int, normed: bool=True):
    theta_freqs, thetas = np.histogram(np.power(np.cos(xi_samples), 2 * alpha), bins=num_bins, normed=normed)
    return np.asarray([0] + list(thetas[1:])), np.asarray([0] + list(theta_freqs))


def get_theta_distribution(alpha: int=1, num_thetas: int=10000, override_uniform: bool=False):
    thetas = np.linspace(0, np.pi / 2, num_thetas)
    theta_vals = np.linspace(0, np.pi, num_thetas)
    if not override_uniform:
        theta_freqs = alpha * np.sin(thetas) * np.power(np.cos(thetas), 2 * alpha - 1)
    else:
        theta_freqs = np.pad(np.ones(int(num_thetas - 2)), ((1, 1),), 'constant') * 1 / np.pi
    return theta_vals, theta_freqs


def get_xi_distribution(alpha: int=1, num_xis: int=10000, override_uniform: bool=False):
    xis = np.linspace(0, 1, num_xis)
    if not override_uniform:
        xi_freqs = 1 / np.sqrt(1 - np.power(xis, 1 / alpha)) * 1 / (2 * alpha) * np.power(xis, 1 / (2 * alpha) - 1)
    else:
        xi_freqs = np.pad(np.ones(int(num_xis - 2)), ((1, 1),), 'constant')
    return xis, xi_freqs


def get_simulated_uniform_phase_histogram(num_samples: int, num_bins: int, normed: bool=True, haar_phase: bool=False):
    max_value = 1 if haar_phase else np.pi / 2
    uniform_phase = max_value * np.random.rand(int(num_samples))
    phase_freqs, phases = np.histogram(uniform_phase, bins=num_bins, normed=normed)
    phase_freqs = [0] + list(phase_freqs) + [0]
    phases = [0] + list(phases[1:]) + [max_value]
    return phases, phase_freqs


def transmittivity_haar_phase(xi, alpha):
    xi_shifted = xi - 1
    xi_periodic_2 = np.mod(xi_shifted, 2)
    xi_periodic_4 = np.mod(xi_shifted, 4)
    xi_periodic_centered_2 = xi_periodic_2 - 1
    # transmittivity = np.sign(xi_periodic_4 - 2) * np.sign(xi_periodic_centered_2) * \
    #     np.power(np.abs(xi_periodic_centered_2), 1 / (2 * alpha))
    transmittivity = np.abs(np.power(np.abs(xi_periodic_centered_2), 1 / (2 * alpha)))
    return transmittivity


def make_upright_diagonal_layer_labels(ax, dim: int, fontsize: int):
    for i in range(dim + 1):
        if i < int(dim / 2):
            ax.plot([0, i * 2 + 1 + dim % 2],
                    [dim - i * 2 - 1 - dim % 2, dim], color=DARK_GREEN, alpha=0.5)
        elif i <= int(dim / 2) * 2:
            ax.plot([i * 2 - dim + 1 + dim % 2, dim + 1],
                    [0, 2 * dim - i * 2 - dim % 2], color=DARK_GREEN, alpha=0.5)
        if -1 + dim % 2 < i < dim / 2:
            ax.annotate(
                f'${i + 1 - dim % 2}$', (i * 2 + 2 - dim % 2, dim + 0.1),
                fontsize=fontsize,
                horizontalalignment='center', verticalalignment='top', color=DARK_GREEN
            )
        elif dim / 2 <= i < dim + dim % 2:
            ax.annotate(
                f'${i - dim % 2}$', (i * 2 - dim - dim % 2, -0.1), fontsize=fontsize,
                horizontalalignment='center', verticalalignment='bottom', color=DARK_GREEN
            )


def make_downright_diagonal_layer_labels(ax, dim: int, fontsize: int):
    for i in range(dim + 1):
        if i < int(dim / 2):
            ax.plot([0, i * 2 + 1 + dim % 2],
                    [dim - i * 2 - 1 - dim % 2, dim], color=DARK_GREEN, alpha=0.5)
        elif i <= int(dim / 2) * 2:
            ax.plot([i * 2 - dim + 1 + dim % 2, dim + 1],
                    [0, 2 * dim - i * 2 - dim % 2], color=DARK_GREEN, alpha=0.5)
        if -1 + dim % 2 < i < dim / 2:
            ax.annotate(
                f'${i + 1 - dim % 2}$', (i * 2 + 2 - dim % 2, dim + 0.1),
                fontsize=fontsize,
                horizontalalignment='center', verticalalignment='top', color=DARK_GREEN
            )
        elif dim / 2 <= i < dim + dim % 2:
            ax.annotate(
                f'${i - dim % 2}$', (i * 2 - dim - dim % 2, -0.1), fontsize=fontsize,
                horizontalalignment='center', verticalalignment='bottom', color=DARK_GREEN
            )


def make_xy_diagonal_labels(ax, dim: int, fontsize: int, padding: int=1):
    for i in range(dim + dim % 2):
        if i < int(dim / 2):
            ax.plot([0, i * 2 + 1 + padding + dim % 2],
                    [dim - i * 2 - 1 - dim % 2, dim + padding], linewidth=1, color=GRAY, alpha=0.5)
        elif i <= int(dim / 2) * 2:
            if i == int(dim / 2):
                ax.plot([i * 2 - dim + 1 + dim % 2, i * 2 + 1],
                        [0, dim - dim % 2], linewidth=2,
                        color=DARK_GREEN, alpha=0.8)
                ax.plot([i * 2 + 1, 1 + i * 2 + padding + dim % 2],
                        [dim - dim % 2, dim + padding], linewidth=1,
                        color=GRAY, alpha=0.5)
            else:
                ax.plot([i * 2 - dim + 1 + dim % 2, 1 + i * 2 + padding + dim % 2],
                        [0, dim + padding], linewidth=1,
                        color=GRAY, alpha=0.5)
        if 0 < i < dim:
            ax.annotate(
                f'${i}$', (i * 2 + 1.5 + dim % 2 - 1, dim + 0.1),
                fontsize=fontsize,
                horizontalalignment='center', verticalalignment='top',
                color=GRAY
            )
    ax.annotate(
        f'$y =$', (1.5 + dim % 2 - 1, dim + 0.1),
        fontsize=fontsize,
        horizontalalignment='center', verticalalignment='top',
        color=GRAY
    )
    for i in range(dim + dim % 2):
        if i < int(dim / 2):
            ax.plot([0, i * 2 + 1 + padding],
                    [i * 2 + 1, -padding], linewidth=1,
                    color=GRAY, alpha=0.5)
        elif i <= int(dim / 2) * 2:
            if i == int(dim / 2):
                ax.plot([1, i * 2 + 1],
                        [i * 2, 0], linewidth=2,
                        color=DARK_GREEN, alpha=0.8)
                ax.plot([i * 2 + 1, i * 2 + 1 + padding],
                        [0, -padding], linewidth=1,
                        color=GRAY, alpha=0.5)
            else:
                ax.plot([i * 2 - dim + 1, 1 + i * 2 + padding],
                        [dim, -padding], linewidth=1,
                        color=GRAY, alpha=0.5)
        if 0 < i < dim:
            ax.annotate(
                f'${i}$', (i * 2 + 0.5, -0.1),
                fontsize=fontsize,
                horizontalalignment='center', verticalalignment='bottom',
                color=GRAY
            )
    ax.annotate(
        f'$x =$', (0.5, -0.1),
        fontsize=fontsize,
        horizontalalignment='center', verticalalignment='bottom',
        color=GRAY
    )


def make_input_output_labels(ax, dim: int, fontsize: int, include_laser_symbol: bool=False):
    for i in range(dim):
        ax.annotate(
            f'${i + 1}$', xy=(-2 if include_laser_symbol else -1.5, i + 0.5), fontsize=fontsize,
            horizontalalignment='right', verticalalignment='center', color=DARK_BLUE
        )
        if include_laser_symbol:
            ax.plot([-1.75, -1], [i + 0.5, i + 0.5], color=DARK_BLUE)
            ax.scatter([-1.75], [i + 0.5], color=DARK_BLUE, marker='x')
            ax.scatter([-1.75], [i + 0.5], color=DARK_BLUE, marker='+')


def make_vertical_layer_labels(ax, dim: int, fontsize: int):
    for i in range(dim + 1):
        ax.plot([i + 0.5, i + 0.5], [0, dim], color=DARK_GREEN, alpha=0.5)
        if i < dim:
            ax.annotate(
                f'${i + 1}$', xy=(i + 1, -0.25), fontsize=fontsize,
                horizontalalignment='center', verticalalignment='bottom', color=DARK_GREEN
            )
            ax.annotate(
                f'${i + 1}$', xy=(i + 1, dim + 0.25), fontsize=fontsize,
                horizontalalignment='center', verticalalignment='top', color=DARK_GREEN
            )


def make_givens_rotation_tmn_labels(ax, dim: int, fontsize: int):
    for i in range(dim - 1):
        ax.plot([1 + i % 2, dim + 3], [i + 1, i + 1], color=DARK_ORANGE, linestyle='--', alpha=0.5, zorder=1)
        idx_str = f'{i + 1}'
        ax.annotate(
            '$U_{' + idx_str + '}$', xy=(dim + 3.25, i + 1), fontsize=fontsize,
            horizontalalignment='left', verticalalignment='center', color=DARK_ORANGE
        )


def make_tri_vertical_layer_labels(ax, dim: int, fontsize: int):
    width = dim * 2 - 3
    for i in range(width + 1):
        ax.plot([i + 0.5, i + 0.5], [0, dim], color=DARK_GREEN, alpha=0.5)
        if i < width:
            ax.annotate(
                f'${i + 1}$', xy=(i + 1, -0.25), fontsize=fontsize,
                horizontalalignment='center', verticalalignment='bottom', color=DARK_GREEN
            )
            ax.annotate(
                f'${i + 1}$', xy=(i + 1, dim + 0.25), fontsize=fontsize,
                horizontalalignment='center', verticalalignment='top', color=DARK_GREEN
            )


def make_tri_diagonal_layer_labels(ax, dim: int, fontsize: int, upright=False):
    for i in range(dim):
        if upright:
            ax.plot([dim - 2 * i + 5, dim - i + 6], [dim, dim - i - 1], color=DARK_GREEN, alpha=0.5)
        else:
            ax.plot([2 * i + 1, i], [dim, dim - i - 1], color=DARK_GREEN, alpha=0.5)
        if i < dim:
            ax.annotate(
                f'${dim - i}$', xy=(dim - 2 * i + 6 - 2 * upright, dim + 0.25), fontsize=fontsize,
                horizontalalignment='center', verticalalignment='top', color=DARK_GREEN
            )


def make_tri_givens_rotation_tmn_labels(ax, dim: int, fontsize: int):
    width = 2 * dim - 3
    for i in range(dim - 1):
        ax.plot([-1 + dim - i, width + 3], [i + 1, i + 1], color=DARK_ORANGE, linestyle='--', alpha=0.5, zorder=1)
        idx_str = f'{i + 1}'
        ax.annotate(
            '$U_{' + idx_str + '}$', xy=(width + 3.25, i + 1), fontsize=fontsize,
            horizontalalignment='left', verticalalignment='center', color=DARK_ORANGE
        )


def upper_bounce(point, dim):
    layer = point[0]
    return [layer, layer + 0.5, layer + 1.5, layer + 2], [dim - 1, dim - 0.5, dim - 0.5, dim - 1]


def lower_bounce(point):
    layer = point[0]
    return [layer, layer + 0.5, layer + 1.5, layer + 2], [1, 0.5, 0.5, 1]


def forward_connect(point, upper):
    return [point[0], point[0] + 1], [point[1], point[1] - 1 + 2 * upper]


def input_piece(point, upper):
    layer = point[0]
    input_y = point[1] - 0.5 + upper
    return [layer, layer - 0.5, -1], [point[1], input_y, input_y]


def output_piece(point, upper, rank):
    layer = point[0]
    output_y = point[1] - 0.5 + upper
    return [layer, layer + 0.5, rank + 2], [point[1], output_y, output_y]


def make_transmission_mzi_labels(ax, dim, marker_size, mean=False):
    checkerboard_points = get_checkerboard_points(dim, dim)
    alpha_checkerboard = get_alpha_checkerboard(dim, dim)
    expected_theta = np.arcsin(np.power(0.5 if mean else np.random.rand(*alpha_checkerboard.shape), 0.5 / alpha_checkerboard))
    h = ax.scatter(
        checkerboard_points[1] + 1, checkerboard_points[0] + 1,
        c=np.sin(expected_theta[checkerboard_points]) ** 2,
        cmap='hot', zorder=2, s=int(2.5 * marker_size), edgecolor=DARK_RED, linewidth=1)
    h.set_clim((0, 1))


def make_theta_mzi_labels(ax, dim, marker_size, mean=False):
    checkerboard_points = get_checkerboard_points(dim, dim)
    alpha_checkerboard = get_alpha_checkerboard(dim, dim)
    expected_theta = np.arcsin(np.power(0.5 if mean else np.random.rand(*alpha_checkerboard.shape), 0.5 / alpha_checkerboard))
    h = ax.scatter(
        checkerboard_points[1] + 1, checkerboard_points[0] + 1,
        c=expected_theta[checkerboard_points],
        cmap='hot', zorder=2, s=int(2.5 * marker_size), edgecolor=DARK_RED, linewidth=1)
    h.set_clim((0, np.pi / 2))


def make_tri_transmission_mzi_labels(ax, dim, marker_size, mean=False):
    checkerboard_points = get_triangular_mesh_points(dim)
    alpha_checkerboard = get_triangular_mesh_alpha(dim)
    theta = np.arcsin(np.power(0.5 if mean else np.random.rand(*alpha_checkerboard.shape), 0.5 / alpha_checkerboard))
    h = ax.scatter(
        checkerboard_points[1] - 1, checkerboard_points[0] + 1,
        c=np.sin(theta[checkerboard_points]) ** 2,
        cmap='hot', zorder=3, s=int(2.5 * marker_size), edgecolor=DARK_RED, linewidth=1)
    h.set_clim((0, 1))


def make_tri_theta_mzi_labels(ax, dim, marker_size, mean=False):
    checkerboard_points = get_triangular_mesh_points(dim)
    alpha_checkerboard = get_triangular_mesh_alpha(dim)
    theta = np.arcsin(np.power(0.5 if mean else np.random.rand(*alpha_checkerboard.shape), 0.5 / alpha_checkerboard))
    h = ax.scatter(
        checkerboard_points[1] - 1, checkerboard_points[0] + 1,
        c=theta[checkerboard_points],
        cmap='hot', zorder=3, s=int(2.5 * marker_size), edgecolor=DARK_RED, linewidth=1)
    h.set_clim((0, np.pi / 2))


def cmap_map(function, cmap):
    """ Applies function (which should operate on vectors of shape 3: [r, g, b]), on colormap cmap.
    This routine will break any discontinuous points in a colormap.
    """
    cdict = cmap._segmentdata
    step_dict = {}
    # Firt get the list of points where the segments start or end
    for key in ('red', 'green', 'blue'):
        step_dict[key] = list(map(lambda x: x[0], cdict[key]))
    step_list = sum(step_dict.values(), [])
    step_list = np.array(list(set(step_list)))
    # Then compute the LUT, and apply the function to the LUT
    reduced_cmap = lambda step: np.array(cmap(step)[0:3])
    old_LUT = np.array(list(map(reduced_cmap, step_list)))
    new_LUT = np.array(list(map(function, old_LUT)))
    # Now try to make a minimal segment definition of the new LUT
    cdict = {}
    for i, key in enumerate(['red', 'green', 'blue']):
        this_cdict = {}
        for j, step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j, i]
            elif new_LUT[j, i] != old_LUT[j, i]:
                this_cdict[step] = new_LUT[j, i]
        colorvector = list(map(lambda x: x + (x[1],), this_cdict.items()))
        colorvector.sort()
        cdict[key] = colorvector

    return matplotlib.colors.LinearSegmentedColormap('colormap', cdict, 1024)


light_rdbu = cmap_map(lambda x: 0.75 * x + 0.25, plt.cm.RdBu)


def plot_planar_boundary(X, Y, model, grid_points=50):


    x_min, y_min = -2, -2
    x_max, y_max = 2, 2
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, grid_points), np.linspace(x_min, x_max, grid_points))

    # Predict the function value for the whole grid
    N = 2
    inputs = []
    for x, y in zip(xx.flatten(), yy.flatten()):
        inputs.append([x, y])
    inputs = np_to_k_complex(add_bias(np.asarray(inputs)).astype(np.float32))

    Y_hat = model.predict(inputs)
    Y_hat = [yhat[0] for yhat in Y_hat]
    Z = np.array(Y_hat)
    Z = Z.reshape(xx.shape)

    # Plot the contour and training examples
    plt.figure(figsize=(6, 6), dpi=200)
    plt.contourf(xx, yy, Z, 50, cmap=light_rdbu)
    plt.clim((0, 1))
    plt.colorbar(ticks=[0, 0.2, 0.4, 0.6, 0.8, 1])

    points_x = X.T[0, :]
    points_y = X.T[1, :]
    labels = np.array([1 if yi[0] > yi[1] else 0 for yi in np.abs(Y)]).flatten()

    plt.ylabel(r'$x_2$', fontsize=16)
    plt.xlabel(r'$x_1$', fontsize=16)

    plt.scatter(points_x, points_y, c=labels, s=6, cmap=plt.cm.RdBu)

    plt.show()
