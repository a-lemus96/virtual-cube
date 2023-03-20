# standard library modules
import glob
import os
from typing import Tuple

# third-party modules
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def draw_cube(
        proj_vertices: np.ndarray,
        target: np.ndarray,
        target_dir: str) -> None:
    """Draw a virtual cube over the chessboard pattern for a particular image
    as if it were part of the scene. This kind of toy function illustrates the
    basic principles of virtual reality. Saves image into target_dir folder.
    ----------------------------------------------------------------------------
    Args:
        proj_vertices: set of projected vertices of the cube in image
                       coordinates
        target: scene where to draw the projected cube
        target_dir: target directory where to store result
    Returns:
        None"""

    # lower vertices (touching the chessboard)
    vertex2_11 = projected_vertices[0].astype(np.int32)
    vertex2_21 = projected_vertices[1].astype(np.int32)
    vertex2_12 = projected_vertices[2].astype(np.int32)
    vertex2_22 = projected_vertices[3].astype(np.int32)
    
    # draw lower face of the cube
    target = cv.line(target, vertex2_11, vertex2_21, (0, 165, 255), 18)
    target = cv.line(target, vertex2_12, vertex2_22, (0, 165, 255), 18)
    target = cv.line(target, vertex2_11, vertex2_12, (0, 165, 255), 18)
    target = cv.line(target, vertex2_21, vertex2_22, (0, 165, 255), 18)
    
    # upper vertices (above the chessboard)
    vertex1_11 = projected_vertices[4].astype(np.int32)
    vertex1_21 = projected_vertices[5].astype(np.int32)
    vertex1_12 = projected_vertices[6].astype(np.int32)
    vertex1_22 = projected_vertices[7].astype(np.int32)
    
    # draw upper face of the cube
    target = cv.line(target, vertex1_11, vertex1_21, (0, 165, 255), 18)
    target = cv.line(target, vertex1_12, vertex1_22, (0, 165, 255), 18)
    target = cv.line(target, vertex1_11, vertex1_12, (0, 165, 255), 18)
    target = cv.line(target, vertex1_21, vertex1_22, (0, 165, 255), 18)
     
    # sonnect both faces
    target = cv.line(target, vertex1_11, vertex2_11, (0, 165, 255), 18)
    target = cv.line(target, vertex1_12, vertex2_12, (0, 165, 255), 18)
    target = cv.line(target, vertex1_21, vertex2_21, (0, 165, 255), 18)
    target = cv.line(target, vertex1_22, vertex2_22, (0, 165, 255), 18)
    
    plt.imshow(cv.cvtColor(target, cv.COLOR_BGR2RGB))
    # save image
    cv.imwrite(f'{target_dir}/cube_' + str(i) + ".jpg", target)

# create directories
os.makedirs('out/projected', exist_ok=True)

# load camera calibration data
calibration_data = np.load('out/calibration_data.npz')
valids = calibration_data['valids'] # set of first ten valid images
rvecs = calibration_data['rvecs']
tvecs = calibration_data['tvecs']
mtx = calibration_data['mtx']
dist = calibration_data['dist']

# set vertices of the cube a priori based on world-frame coordinates
vertices = np.array([[2., 1., 0.], [2., 5., 0.],
                     [6., 1., 0.], [6., 5., 0.],
                     [2., 1., -4.], [2., 5., -4.],
                     [6., 1., -4.], [6., 5., -4.]])

for i in range(len(valids)):
    target = cv.imread(valids[i])
    # project 3D points into the image
    projected_vertices, _ = cv.projectPoints(vertices,
                                             rvecs[i],
                                             tvecs[i],
                                             mtx,
                                             dist)
    projected_vertices = projected_vertices.reshape(16).reshape(8,2)

    # draw projected cube using projected vertices
    draw_cube(projected_vertices, target, 'out/projected')
