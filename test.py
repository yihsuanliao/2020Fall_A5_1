import numpy as np
sculpture = [[1, 2]]
array = np.array(sculpture)

print(array)
array = np.nan_to_num(array, 0)
print(array)

#ch = ConvexHull(points=new_sculpture, incremental=True)

from scipy.ndimage import center_of_mass

from scipy.spatial import ConvexHull
print(ConvexHull.__version__)
center = center_of_mass(array)
print(center)

## 假設sculpture已經是ndarray (scuplture = np.array().reshape())
## if value is nAn -> needs to replace 0 so that center of mass works
sculpture = carve_sculpture_from_density_block ( shape_1, marble_block_1 )
sculpture = np.nan_to_num ( sculpture, 0 )  # convert nan to zero to make center_of_mass work
center = center_of_mass ( sculpture )

# use convexhull把3d轉成2d 看center of mass有沒有在base裡面
sculpture_base = ConvexHull. ( points=sculpture, incremental=True )  ## 2d或3d應該都可以用convex hull?因為上面sculpture的地方還沒出來
## ^ 出來的應該要是2d array
sculpture_base == center
if center in sculpture_base:
    result == True  # 還要看需不需要傳進dict裡面
else:
    result == False
sculpture = bool ( sculpture, result )
return result

# output #還要調一下固定寬度 跟tab一格
# print("Shape File: ", 傳進shapefile)
# print("Block File:", 傳進blockfile )
# print("Rotation: {} Mean density: {} {}".format(Rotation, Mean Density, is_stable?))


# sculpture_base = sculpture[0, :, :]

# ch1 = ConvexHull(points=sculpture_base, incremental=True)
# print("ch1:")
# summarize_hull_properties(ch1)


def is_stable(sculpture: np.ndarray) -> bool:
    """Given a 'sculpted' NDarray, where number values represent densities and
    NaN values represent the areas carved away, determine if, in the orientation
    given, whether it will sit stably upon its base.

    :param sculpture: NDarray representing a sculpture of variable density material.
    """
    # TODO: Complete this function.
    # TODO: Add a few good, working Doctests

    ## 假設sculpture已經是ndarray (scuplture = np.array().reshape())
    ## if value is nAn -> needs to replace 0 so that center of mass works
    sculpture = carve_sculpture_from_density_block(shape_1, marble_block_1)
    sculpture = np.nan_to_num(sculpture, 0)  # convert nan to zero to make center_of_mass work
    center = center_of_mass(sculpture)
    if center > 2:
        center = center[1:]

    ## slice the bottom layer ( last item in the array)
    sculpture_base = sculpture[-1]  # 3d -> 2d -> result a sqare
    # nan arrays
    sculpture_base = np.argwhere(sculpture_base > 0) # return array of points
    # np.transpose(sculpture_base) (?)

    # use convexhull 看center of mass有沒有在base裡面
    # get ch1
    ch1 = ConvexHull(points=sculpture_base, incremental=True)
    # summarize_hull_properties ( ch1 )
    ch2 = ch1.add_points(center)
    # summarize_hull_properties ( ch1 )
    # compare ch1 and ch2, if ch1 == ch2 return True, else False
    if ch1 == ch2:
        return True


    # output #還要調一下固定寬度 跟tab一格
    #print("Shape File: ", 傳進shapefile)
    #print("Block File:", 傳進blockfile )
    #print("Rotation: {} Mean density: {} {}".format(Rotation, Mean Density, is_stable?))
    # sculpture_base = sculpture[0, :, :]

import numpy as np
x = np.arange(27).reshape((3,3,3))
print(x)

bottomlayer = x[-1]  # 3d -> 2d -> result a sqare  [0,:,:]
print(bottomlayer)

from scipy.ndimage import center_of_mass
center = center_of_mass(x)
print(center)
print(len(center))
if len(center)>2:
    center2 = center[1:]
    print(center2)z
