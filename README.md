# Virtual cube mini-project
Implementation of a mini-project to demonstrate the use of projective geometry in virtual reality applications. The project consists of a camera calibration script `opencv-calibrate.py` and a virtual cube reprojection script under the flashy `virtual-reality.py` name. Camera calibration script is based on the OpenCV camera calibration [tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).

### Camera calibration
---
Projective geometry is the mathematical framework that allows one to model the process of capturing 3D scenes into 2D images. Using this framework, the action of taking a photo with a camera may be modeled mathematically as a set of sequential linear transformations applied to spatial coordinates using a special vector representation, called homogeneous coordinates representation. That is,

$$
  p^{i} \propto K R p^{w}
$$

describes how any 3D point or object point $p^{w} =[x, y, z, 1]^\top$ gets mapped into image point $p^{i}=[u,v,1]^\top$. Matrix $K\in \mathbb{R}^{3\times4}$ is the so-called intrinsics matrix which contains internal physical properties that model how object points are mapped directly from the camera coordinate frame into image points. Since camera frame is not aligned is not the case for many real-life applications, the extrinsics camera matrix $R\in\mathbb{R}^{4\times4}$ maps object point coordinates into their camera frame representation, this transformation is simply a rigid transformation in homogeneous coordinates.

In a nutshell, camera calibration consists any algorithm for computing or estimating camera matrix $K$ parameters using small pieces of information from the real-world. In this case, we consider those pieces of information to be prior object points coordinates lying over a planar surface. We use a set of images containing a checkerboard pattern and assume the world coordinate frame to be at one of the vertices of board.

We use OpenCV functionalities to compute $K$ from the set of images available in `imgs/` folder. To perform camera calibration simply run `python opencv-calibrate.py`. The script takes the first 10 valid images for running the calibration algorithm:

<p align="center">
<img src="https://user-images.githubusercontent.com/95151624/226233127-4dad33a6-d060-44f4-92e2-0f115a178cb1.gif"/>
</p>

As the script filters input images, it stores the set of object points drawed on the input images in the `out/points/` folder. Once it finishes filtering and plotting points, performs camera calibration, displays camera matrix, stores the calibration data into `out/calibration_data.npz` and computes average reprojection error in pixels.

![image](https://user-images.githubusercontent.com/95151624/226421438-273ee959-ee4a-4ca5-b250-245cc1210cab.png)

It is important to note that camera calibration also stores extrinsic information for all valid views. Now that we have an internal and external mathematical modelling for each of the valid frames, it is time to use this information to create something cool!

### Projecting a virtual cube onto the calibration images
---
<p align="center">
<img src="https://user-images.githubusercontent.com/95151624/226233373-ece48423-2b41-4dcb-ada0-1ba2cb87fa29.gif"/>
</p>

$$
  K = \frac{1}{2}
$$
