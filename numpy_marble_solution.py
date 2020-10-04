"""
590PR Spring 2020.
Instructor: John Weible  jweible@illinois.edu
Assignment on Numpy: "High-Tech Sculptures"

Author: Yi Hsuan Liao (yhliao4); De Zhou Chen (dezhouc2)
See assignment instructions in the README.md document AND in the
TO DO comments below.
"""

import numpy as np
from scipy.ndimage import center_of_mass
from typing import List
from scipy.spatial import ConvexHull


def get_orientations_possible(block: np.ndarray) -> List[List[dict]]:
    """Given a 3D numpy array, look at its shape to determine how many ways it
    can be rotated in each axis to end up with a (theoretically) different array
    that still has the SAME shape.

    if all three dimensions are different sizes, then we have 3 more
    orientations, excluding the original, which are all 180-degree rotations.

    if just two dimensions match size, we have 7 plus original. 90-degree
    rotations are around the unique-length axis.

    if all three dimensions match (a cube), then we have 23 plus original.

    :param block: a numpy array of 3 dimensions.
    :return: a list of the ways we can rotate the block. Each is a list of dicts containing parameters for np.rot90()

    >>> a = np.arange(64, dtype=int).reshape(4, 4, 4)  # a cube
    >>> rotations = get_orientations_possible(a)
    >>> len(rotations)
    23
    >>> rotations  # doctest: +ELLIPSIS
    [[{'k': 1, 'axes': (0, 1)}], ... [{'k': 3, 'axes': (1, 2)}, {'k': 3, 'axes': (0, 2)}]]
    >>> a = a.reshape(2, 4, 8)
    >>> len(get_orientations_possible(a))
    3
    >>> a = a.reshape(16, 2, 2)
    >>> len(get_orientations_possible(a))
    7
    >>> get_orientations_possible(np.array([[1, 2], [3, 4]]))
    Traceback (most recent call last):
    ValueError: array parameter block must have exactly 3 dimensions.
    >>> marble_block_1 = np.load(file='data/marble_block_1.npy')
    >>> len(get_orientations_possible(marble_block_1))
    7
    """

    if len(block.shape) != 3:
        raise ValueError('array parameter block must have exactly 3 dimensions.')

    # Create list of the 23 possible 90-degree rotation combinations -- params to call rot90():
    poss = [
        [{'k': 1, 'axes': (0, 1)}],  # 1-axis rotations:
        [{'k': 2, 'axes': (0, 1)}],
        [{'k': 3, 'axes': (0, 1)}],
        [{'k': 1, 'axes': (0, 2)}],
        [{'k': 2, 'axes': (0, 2)}],
        [{'k': 3, 'axes': (0, 2)}],
        [{'k': 1, 'axes': (1, 2)}],
        [{'k': 2, 'axes': (1, 2)}],
        [{'k': 3, 'axes': (1, 2)}],
        [{'k': 1, 'axes': (0, 1)}, {'k': 1, 'axes': (0, 2)}],  # 2-axis rotations:
        [{'k': 1, 'axes': (0, 1)}, {'k': 2, 'axes': (0, 2)}],
        [{'k': 1, 'axes': (0, 1)}, {'k': 3, 'axes': (0, 2)}],
        [{'k': 2, 'axes': (0, 1)}, {'k': 1, 'axes': (0, 2)}],
        [{'k': 2, 'axes': (0, 1)}, {'k': 3, 'axes': (0, 2)}],
        [{'k': 3, 'axes': (0, 1)}, {'k': 1, 'axes': (0, 2)}],
        [{'k': 3, 'axes': (0, 1)}, {'k': 2, 'axes': (0, 2)}],
        [{'k': 3, 'axes': (0, 1)}, {'k': 3, 'axes': (0, 2)}],
        [{'k': 1, 'axes': (1, 2)}, {'k': 1, 'axes': (0, 2)}],
        [{'k': 1, 'axes': (1, 2)}, {'k': 2, 'axes': (0, 2)}],
        [{'k': 1, 'axes': (1, 2)}, {'k': 3, 'axes': (0, 2)}],
        [{'k': 3, 'axes': (1, 2)}, {'k': 1, 'axes': (0, 2)}],
        [{'k': 3, 'axes': (1, 2)}, {'k': 2, 'axes': (0, 2)}],
        [{'k': 3, 'axes': (1, 2)}, {'k': 3, 'axes': (0, 2)}],
    ]

    # consider the 3-tuple shape of axes numbered 0, 1, 2 to represent (height, depth, width)
    (height, depth, width) = block.shape

    if height == depth == width:
        return poss  # return all possibilities, it's a cube

    # TODO: Complete this function for the other situations...
    # Hint, the results will be parts of the 23-item list above, read the Docstring!
    ## doctest passed:)

    # Create list of the 7 possible 90-degree rotation combinations -- params to call rot90():
    poss2 = [
        [{'k': 2, 'axes': (0, 1)}],  # 1-axis rotations:
        [{'k': 2, 'axes': (0, 2)}],
        [{'k': 1, 'axes': (1, 2)}],
        [{'k': 2, 'axes': (1, 2)}],
        [{'k': 3, 'axes': (1, 2)}],
        [{'k': 3, 'axes': (1, 2)}, {'k': 2, 'axes': (0, 2)}],
        [{'k': 1, 'axes': (1, 2)}, {'k': 2, 'axes': (0, 2)}],
    ]
    if height == depth != width or height != depth == width or height == depth != width:  # 其中兩個條件相等就return poss2
        return poss2

    # Create list of the 3 possible 180-degree rotation combinations -- params to call rot180():
    poss3 = [
        [{'k': 2, 'axes': (0, 1)}],  # 1-axis rotations:
        [{'k': 2, 'axes': (1, 2)}],
        [{'k': 2, 'axes': (0, 2)}],
    ]
    # all three dimensions are different sizes
    if height != depth != width:
        return poss3


def carve_sculpture_from_density_block(shape: np.ndarray, block: np.ndarray) -> np.ndarray:
    """The shape array guides our carving. It indicates which parts of the
    material block to keep (the 1 values) and which to carve away (the 0 values),
    producing a new array that defines a sculpture and its varying densities.
    It must have NaN values everywhere that was 'carved' away.

    :param shape: array to guide carving into some 3D shape
    :param block: array describing densities throughout the raw material block
    :return: array of densities in the resulting sculpture, in same orientation.
    :raises: ValueError if the input arrays don't match in size and shape.
    # TODO: write the code for this function, which could be as short as one line of code!
    # TODO: Add a few good, working Doctests
    >>> carve_sculpture_from_density_block(np.array([[[1,2], [3,4]]]), np.array([[[1,2], [5,6]]]))
    array([[[ 1., nan],
            [nan, nan]]])

    >>> carve_sculpture_from_density_block(np.array([[[1,2,3], [4,5,6]]]), np.array([[[1,2,3], [7,8,9]]]))
    array([[[ 1., nan, nan],
            [nan, nan, nan]]])

    >>> carve_sculpture_from_density_block(np.array([[[1,2,3]]]), np.array([[[10,11,12],[13,15,16]]]))
    Traceback (most recent call last):
    ValueError: The input arrays don't match in size and shape

    """

    #return array of densities for sculpture
    if shape.shape != block.shape:
        raise ValueError ("The input arrays don't match in size and shape")
    return np.where(shape == 1, block, np.nan)


def is_stable(sculpture: np.ndarray) -> bool:
    """Given a 'sculpted' NDarray, where number values represent densities and
    NaN values represent the areas carved away, determine if, in the orientation
    given, whether it will sit stably upon its base.

    :param sculpture: NDarray representing a sculpture of variable density material.
    >>> is_stable(np.array([[[1,2], [4,5]]]))
    True
    >>> is_stable(np.array([[[1, np.nan, np.nan], [np.nan, np.nan, 6], [np.nan, np.nan, np.nan], [1, np.nan, np.nan]]]))
    True

    """
    sculpture = np.nan_to_num(sculpture, 0)  # convert nan to zero to make center_of_mass work
    center = list(center_of_mass(sculpture)) # (z, y, x)

    # slice the bottom layer ( last item in the array) 3d -> 2d -> result a square
    sculpture_base = sculpture[-1]
    # nan arrays
    sculpture_base = np.argwhere(sculpture_base).tolist()  # return array of points
    # np.transpose(sculpture_base) (?)

    # use convexhull to calculate area and check if its stable or not
    # get area1
    hull = ConvexHull(points=sculpture_base, incremental=True)
    area1 = hull.area

    del center[0]
    # add points to calculate new area
    sculpture_base.append(center)
    # area2 -> after adding center points to hull
    hull2 = ConvexHull(points=sculpture_base, incremental=True)
    area2 = hull2.area
    # compare area1 and area2, if ch1 == ch2 return True, else False
    if area1 == area2:
        return True
    else:
        return False




def analyze_sculptures(block_filenames: list, shape_filenames: list):
    """Given all the filenames of blocks and sculpture shapes to carve,
    analyze them in all usable block rotations to show their resulting
    densities and stabilities.  See the README.md file for an example
    output format.

    :param block_filenames: list as parameter to open block npy files
    :param shape_filenames: list as parameter to open shape npy files
    :return: for each shape file, output 5 block files along with rotation and mean density for each block file respectively
    >>> marble1 = ['marble_block_1.npy']
    >>> shape1 = ['shape_1.npy']
    >>> analyze_sculptures(marble1, shape1)


    >>> marble2 = ['markble_block_2.npy']
    >>> shape2 = ['shape_2.npy']
    >>> analyze_sculptures(marble2, shape2)


    """

    # TODO: Complete this function.
    # TODO: Add a few good, working Doctests


    for shapefile in shape_filenames:
        print("Shape File: ", shapefile)
        shapearrays = np.load(file='data/' + shapefile)

        for blockfile in block_filenames:
            print("    Block File:", blockfile)
            blockarrays = np.load(file = 'data/' + blockfile)
            statusdata = []
            meandensity = carve_sculpture_from_density_block(shapearrays, blockarrays)
            meandensity32 = np.nanmean(meandensity.astype('float32'))
            statusdata.append(["None", meandensity32, "Stable" if is_stable(meandensity) else "Unstable"])

            for i in get_orientations_possible(blockarrays):
                if len(i) == 1:
                    orient0 = np.rot90(blockarrays, k = i[0]['k'], axes = (i[0]['axes']))
                    meandensity = carve_sculpture_from_density_block(shapearrays, orient0)
                    meandensity32 = np.nanmean(meandensity.astype('float32'))
                    degree0 = (90 * i[0]['k'])
                    degree0str = str(degree0)
                    axes = i[0]['axes']
                    axestr = str(axes)
                    statusdata.append([degree0str + " axis " + axestr, meandensity32, "Stable" if is_stable(meandensity) else "Unstable"])


            else:
                orient1 = np.rot90(blockarrays, k = i[0]['k'], axes = i[0]['axes'])
                orient2 = np.rot90(orient1, k = i[1]['k'], axes = i[1]['axes'])
                meandensity = carve_sculpture_from_density_block(shapearrays, orient2)
                meandensity32 = np.nanmean(meandensity.astype('float32'))
                #90*k[0]
                degree0 = (90 * i[0]['k'])
                degree0str = str(degree0)
                #90*axes[0]
                axes = (90 * i[0]['axes'])
                axestr = str(axes)
                #90 * k[1]
                degree1 = (90 * i[1]['k'])
                degree1str = str(degree1)
                #90* axes[1]
                axes2 = (90 * i[1]['axes'])
                axes2str = str(axes2)

                #+ degree1str + " axis " + axes2str + " , "
                statusdata.append([degree0str + " axis " + axestr + " , " + degree1str + " axis " + axes2str, meandensity32,  "Stable" if is_stable(meandensity) else "Unstable"])
                #status = sorted?

            for lsp in statusdata:
                print("            Rotation: {0:32s}  Mean density: {1:<10f}   {2}".format(lsp[0], lsp[1], lsp[2]))




def are_rotations_unique(list_of_rotations: List[List[dict]], verbose=False) -> bool:
    """Given a list of list of 3D rotation combinations suitable for using with np.rot90()
    and as returned from the get_orientations_possible() function, determine whether any
    of the rotations are equivalent, and discard the duplicates.

    The purpose is to detect situations where a combination of rotations would produce either
    the original unmodified array or the same orientation as any previous one in the list.

    NOTE: This function is already complete! It is provided as an example of rotation
    calculations, good Doctests, and it could be useful to you as part of your solution.

    :param list_of_rotations: a list, such as returned by get_orientations_possible()
    :param verbose: if True, will print details to console, otherwise silent.
    :return: True, if all listed rotation combinations produce distinct orientations.

    >>> x = [[{'k': 4, 'axes': (0, 1)}]]  # 4x90 degrees is a full rotation
    >>> are_rotations_unique(x)
    False
    >>> x = [[{'k': 2, 'axes': (0, 1)}, {'k': 2, 'axes': (0, 1)}]]  # also a full rotation
    >>> are_rotations_unique(x)
    False
    >>> y1 = [[{'k': 3, 'axes': (1, 2)}], [{'k': 1, 'axes': (0, 1)}, {'k': 1, 'axes': (2, 0)}]]
    >>> are_rotations_unique(y1)
    True
    >>> y2 = y1 + [[{'k': 1, 'axes': (1, 2)}, {'k': 3, 'axes': (1, 0)}]]  # equiv. to earlier
    >>> are_rotations_unique(y2, verbose=True)
    combination #1: [{'k': 3, 'axes': (1, 2)}] ok.
    combination #2: [{'k': 1, 'axes': (0, 1)}, {'k': 1, 'axes': (2, 0)}] ok.
    combination #3: [{'k': 1, 'axes': (1, 2)}, {'k': 3, 'axes': (1, 0)}] not unique.
    it results in the same array as combination 2
    False
    """
    # create a small cube to try all the input rotations. It has unique values so that
    #  no distinct rotations could create an equivalent array by accident.
    cube = np.arange(0, 27).reshape((3, 3, 3))

    # Note: In the code below, the arrays must be appended to the orientations_seen
    #  list in string form, because Numpy would otherwise misunderstand the intention
    #  of the if ... in orientations_seen expression.

    orientations_seen = [cube.tostring()]  # record the original

    count = 0
    for combo in list_of_rotations:
        count += 1
        if verbose:
            print('combination #{}: {}'.format(count, combo), end='')

        r = cube  # start with a view of cube unmodified for comparison
        for r90 in combo:  # apply all the rotations given in this combination
            r = np.rot90(r, k=r90['k'], axes=r90['axes'])
        if r.tostring() in orientations_seen:
            if verbose:
                print(' not unique.')
                if r.tostring() == cube.tostring():
                    print('it results in the original 3d array.')
                else:
                    print('it results in the same array as combination',
                            orientations_seen.index(r.tostring()))
            return False
        else:
            if verbose:
                print(' ok.')
        orientations_seen.append(r.tostring())
    return True


if __name__ == '__main__':
    # This section will need to be changed significantly. What's here are
    #  just some examples of loading and manipulating the arrays.
    import os
    files = os.listdir('data/')
    shape_filenames = []
    block_filenames = []
    for f in files:

        if f.startswith('m'):
            block_filenames.append(f)
        if f.startswith('s'):
            shape_filenames.append(f)

    block_filenames = sorted(block_filenames)
    shape_filenames = sorted(shape_filenames)

    analyze_sculptures(block_filenames, shape_filenames)




    # Load a "block" of variable-density marble:

    # Load one array describing the 3D shape of the sculpture we want to carve from marble:

