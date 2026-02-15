import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class CalabiYauVisualizer:
    def __init__(self, n=5):
        self.n = n
    def u1(self, a, b): return np.cosh(a + 1j * b)
    def u2(self, a, b): return np.sinh(a + 1j * b)
    def z1k(self, a, b, k):
        u1_val = self.u1(a, b)
        return np.exp(2j * np.pi * k / self.n) * np.power(u1_val, 2.0 / self.n)
    def z2k(self, a, b, k):
        u2_val = self.u2(a, b)
        return np.exp(2j * np.pi * k / self.n) * np.power(u2_val, 2.0 / self.n)
    def surface(self, k1, k2, alpha, a_range=(-1, 1), b_range=(0, np.pi/2), resolution=200):
        a = np.linspace(a_range[0], a_range[1], resolution)
        b = np.linspace(b_range[0], b_range[1], resolution)
        A, B = np.meshgrid(a, b)
        Z1 = self.z1k(A, B, k1)
        Z2 = self.z2k(A, B, k2)
        X = Z1.real
        Y = Z2.real
        Z = np.cos(alpha) * Z1.imag + np.sin(alpha) * Z2.imag
        return X, Y, Z

def overlay_colored(alpha=np.pi/4, resolution=100):
    vis = CalabiYauVisualizer()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for k1 in range(vis.n):
        for k2 in range(vis.n):
            X, Y, Z = vis.surface(k1, k2, alpha, resolution=resolution)

            # HSV 色调映射
            hue = ((k1 + k2) % vis.n) / vis.n  # 取值 0~1
            rgb_color = mcolors.hsv_to_rgb((hue, 1.0, 1.0))

            ax.plot_surface(
                X, Y, Z,
                rstride=1, cstride=1,
                facecolors=np.full(X.shape + (3,), rgb_color),
                linewidth=0.1, antialiased=False, shade=False
            )

    ax.set_axis_off()
    ax.view_init(elev=30, azim=-45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    overlay_colored()
