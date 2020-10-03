# check function 3 line by line
import numpy as np
from scipy.ndimage import center_of_mass
from typing import List
from scipy.spatial import ConvexHull
x = np.array([[[1,2], [4,5], [np.nan, np.nan], [np.nan, np.nan], [np.nan, -1]]])
print ( x )

sculpture = np.nan_to_num(x, 0)  # convert nan to zero to make center_of_mass work
print(sculpture)
center = list(center_of_mass(x)) # (z, y, x)
print(center)
#if len(center) > 2:
#    center = center[1:]

# slice the bottom layer ( last item in the array) 3d -> 2d -> result a square
sculpture_base = sculpture[-1]
print("1",sculpture_base)
    # nan arrays
sculpture_base = np.argwhere(sculpture_base).tolist()  # return array of points
print("2", sculpture_base)
    # np.transpose(sculpture_base) (?)

    # use convexhull to calculate area and check if its stable or not
    # get area1
hull = ConvexHull(points=sculpture_base, incremental=True)
area1 = hull.area
print(area1)
del center[0]
    # add points to calculate new area
sculpture_base.append(center)
print("sb", sculpture_base)
    # area2 -> after adding center points to hull
hull2 = ConvexHull(points=sculpture_base, incremental=True)
area2 = hull2.area
print(area2)
    # compare area1 and area2, if ch1 == ch2 return True, else False
if area1 == area2:
    print("t")
else:
    print("f")


"""
import numpy as np
x = np.arange(27).reshape((3,3,3))
x = x[-1]
print(x)
x[0] = 0
print(x)
sculpture_base = np.argwhere(x)
print(sculpture_base)

sb = np.argwhere(x>0)
print(sb)


## 假設sculpture已經是ndarray (scuplture = np.array().reshape())
    ## if value is nAn -> needs to replace 0 so that center of mass works
    #sculpture = np.nan_to_num(sculpture, nan = 0)  ## sculpture是不是要從上一個function拿下來啊？
    #center = center_of_mass(sculpture)

    # use convexhull把3d轉成2d 看center of mass有沒有在base裡面
    #ch = ConvexHull(points=sculpture, incremental=True) ## 2d或3d應該都可以用convex hull? ## 這裡還沒弄完 因為上面sculpture的地方還沒出來
    #sculpture_base =   ## 這個應該要是二維
    #print("ch")


    #if center in sculpture_base:
    #    print("Stable")  # 還要看需不需要傳進dict裡面
    #else:
    #    print("Unstable")


    # output #還要調一下固定寬度 跟tab一格
    #print("Shape File: ", 傳進shapefile)
    #print("Block File:", 傳進blockfile )
    #print("Rotation: {} Mean density: {} {}".format(Rotation, Mean Density, is_stable?))
    #return




    # sculpture_base = sculpture[0, :, :]

    # ch1 = ConvexHull(points=sculpture_base, incremental=True)
    # print("ch1:")
    # summarize_hull_properties

    ##我是分割线——————————————————————————————————————————————————————————
"""
"""
import numpy as np
from scipy.ndimage import center_of_mass
from typing import List
from scipy.spatial import ConvexHull

x = np.array([[[1,np.nan,np.nan], [np.nan,np.nan,6],[np.nan, np.nan, np.nan]]])
print(x)
sculpture = np.nan_to_num ( x, 0 )  # convert nan to zero to make center_of_mass work
print(sculpture)
center = list ( center_of_mass ( sculpture ) )
#if len(center) > 2:
#    center = center[1:]
print("centerofmass",center)
sculpture_base = sculpture[-1]  # 3d -> 2d -> result a square
    # nan arrays
print(sculpture_base)
sculpture_base = np.argwhere ( sculpture_base ).tolist ()
print(sculpture_base)
    # np.transpose(sculpture_base) (?)

    # use convexhull to calculate area and check if its stable or not
    # get area1

hull = ConvexHull ( sculpture_base, incremental=True )
area1 = hull.area
print(area1)

if len ( center ) > 2:
    center = center[1:]
    print("new center",center)


sculpture_base.append ( center )
# area2 -> after adding center points to hull
hull2 = ConvexHull ( points=sculpture_base )
area2 = hull2.area
print(area2)
# compare area1 and area2, if ch1 == ch2 return True, else False
if area1 == area2:
    print('True')
else:
    print('False')
"""