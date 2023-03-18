# standard library modules
import glob

# third-party modules
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# set termination criteria for calibration-related fns
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points
objp = np.zeros((7*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)

# create arrays to store object points and image points from all the images
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# keep only the first ten valid images
images = glob.glob('imgs/*.jpg')

count = 0 # this counter will keep track of how many valid images we have
valids = [] # list to store valid images
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (9,7), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        count = count + 1
        valids.append(fname)
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (9,7), corners2, ret)
        plt.figure(figsize=(9,9))
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        # Save image
        cv.imwrite('out/points/points_' + str(count) + ".jpg", img)
        # Keep only our first ten accepted images
        if count >= 10:
            break
print(f"Set of first ten valid images from input folder: {valids}")

# CALIBRATION

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints,
                                                  imgpoints, 
                                                  gray.shape[::-1], 
                                                  None, 
                                                  None)
print(f"Intrinsics camera matrix: \n\n{mtx}")
# save calibration data
np.savez('out/calibration_data.npz', ret=ret, mtx=mtx, 
         dist=dist, rvecs=rvec, tvecs=tvecs)

# REPROJECTION ERROR

mean_error = 0

for i in range(len(objpoints)):
    # project points with intrinsic matrix and compare with ground truth data
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print(f"Total reprojection error: {mean_error/len(objpoints)}")
