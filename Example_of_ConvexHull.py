"""
A simple example using ConvexHull and its properties.  You can adapt the
technique shown here to help solve part of this week's assignment.

Pay particular attention to the fact that when you use ConvexHull with
2-dimensional coordinates, the resulting "hull" is a polygon within a plane.
That is what you need for the assignment!

If you were to supply it 3-D coordinates, the "hull" represents a more
complex geometric solid.

jweible@illinois.edu
"""

from scipy.spatial import ConvexHull


def summarize_hull_properties(ch, max_items=10) -> None:
    """
	Prints a few useful properties of the ConvexHull object.

	:param ch: a scipy.spatial.ConvexHull
	:param max_items: Allows truncating the output when there are many points, vertices, etc.
	"""
    print("area: ", ch.area)
    print("points:\n", ch.points[:max_items])
    print("vertices: ", ch.vertices[:max_items])
    print("simplices:\n", ch.simplices[:max_items])
    print()
    return

box1 = [[0, 0],
        [1, 0],
        [1, 1],
        [0, 1]]

box2 = [[0, 0],
        [1, 0],
        [1, 1],
        [0.5, 0.5],  # this point is in the center of the square
        [0, 1]]

ch1 = ConvexHull(points=box1, incremental=True)
print("ch1:")
summarize_hull_properties(ch1)

print('''\n\nCompared to the above, the following hull contains an extra point at 
0.5, 0.5. We can tell it is INSIDE the hull but not on its boundary, by any
of these:
A) adding that point did not increase the area.
B) That point is not included in the vertices.
C) Therefore, that point is also not an endpoint of any simplices.
''')
ch2 = ConvexHull(points=box2, incremental=True)
print("ch2:")
summarize_hull_properties(ch2)

print('\nNext, we add some outside points to the previous ConvexHulls and notice things change:')
ch1.add_points([[1.99, 0], [0, 2.0]])
print("ch1 is now:")
summarize_hull_properties(ch1)

ch2.add_points([[2.0, 0], [0, 2.000000001]])
print("ch2 is now:")
summarize_hull_properties(ch1)

