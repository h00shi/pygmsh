# -*- coding: utf-8 -*-
"""Create several entities by extrusion, check that the expected
sub-entities are returned and the resulting mesh is correct.
"""
import pygmsh
import numpy as np


def test():
    kernels = [pygmsh.built_in, pygmsh.opencascade]
    for kernel in kernels:
        geom = kernel.Geometry()
        p = geom.add_point([0, 0, 0], 1)
        p_top, _, _ = geom.extrude(p, translation_axis=[1, 0, 0])

        # The mesh should now contain exactly two points,
        # the second one should be where the translation pointed.
        mesh = pygmsh.generate_mesh(geom)
        assert len(mesh.points) == 2
        assert np.array_equal(mesh.points[-1], [1, 0, 0])

        # Check that the top entity (a PointBase) can be extruded correctly
        # again.
        _, _, _ = geom.extrude(p_top, translation_axis=[1, 0, 0])
        mesh = pygmsh.generate_mesh(geom)
        assert len(mesh.points) == 3
        assert np.array_equal(mesh.points[-1], [2, 0, 0])

        # Set up new geometry with one line.
        geom = kernel.Geometry()
        p1 = geom.add_point([0, 0, 0], 1)
        p2 = geom.add_point([1, 0, 0], 1)
        line = geom.add_line(p1, p2)

        l_top, _, _ = geom.extrude(line, [0, 1, 0])
        mesh = pygmsh.generate_mesh(geom)
        assert len(mesh.points) == 5
        assert np.array_equal(mesh.points[-2], [1, 1, 0])

        # Check again for top entity (a LineBase).
        _, _, _ = geom.extrude(l_top, [0, 1, 0])
        mesh = pygmsh.generate_mesh(geom)
        assert len(mesh.points) == 8
        assert np.array_equal(mesh.points[-3], [1, 2, 0])
