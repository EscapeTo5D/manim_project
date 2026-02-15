from manimlib import *
import numpy as np
class CalabiYauVisualization(ThreeDScene):
    def construct(self):
        # Calabi-Yau 参数
        n = 5  # quintic
        def u1(a, b):
            """u1 = cosh(a + ib)"""
            return np.cosh(a + 1j * b)
        def u2(a, b):
            """u2 = sinh(a + ib)"""
            return np.sinh(a + 1j * b)
        def z1k(a, b, k):
            """z1k = e^(2πik/n) * u1^(2/n)"""
            return np.exp(2j * np.pi * k / n) * np.power(u1(a, b), 2.0 / n)
        def z2k(a, b, k):
            """z2k = e^(2πik/n) * u2^(2/n)"""
            return np.exp(2j * np.pi * k / n) * np.power(u2(a, b), 2.0 / n)
        def calabi_yau_surface(a, b, g, k, alpha=0.785):
            z1 = z1k(a, b, k)
            z2 = z2k(a, b, g)
            x = np.real(z1)
            y = np.real(z2)
            z = np.cos(alpha) * np.imag(z1) + np.sin(alpha) * np.imag(z2)
            return x, y, z

        axes = ThreeDAxes()

        surfaces_group = Group()

        for k1 in range(n):
            for k2 in range(n):
                surface = ParametricSurface(
                    lambda u, v: axes.c2p(
                        *calabi_yau_surface(u, v, k1, k2)
                    ),
                    resolution=(51, 51),
                    u_range=(-1, 1),
                    v_range=(0, np.pi / 2),
                )
                surfaces_group.add(surface)
        self.add(surfaces_group.scale(1.5))
        self.wait(2)
