# Projective Geometry for mapping a virtual cube
Implementation of a mini-project to demonstrate the use of projective geometry in virtual reality applications. The project consists of a camera calibration script `opencv-calibrate.py` and a virtual cube reprojection script under the flashy `virtual-reality.py` name. Camera calibration script is based on the OpenCV camera calibration [tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).

### Camera calibration
---
Projective geometry is the mathematical framework that allows one to model the process of capturing 3D scenes into 2D images. Using this framework, the action of taking a photo with a camera may be modeled mathematically as a set of sequential linear transformations applied to spatial coordinates using a special vector representation, called homogeneous coordinates representation. That is,

$$
  p^{i} \propto K R p^{w}
$$

describes how any 3D point or object point $p^{w} =[x, y, z, 1]^\top$ gets mapped into image point $p^{i}=[u,v,1]^\top$. Matrix $K\in \mathbb{R}^{3\times4}$ is the so-called intrinsics matrix which contains internal physical properties that model how object points are mapped directly from the camera coordinate frame into image points. Since the camera frame is not aligned with the world frame in many real-life applications, the extrinsics camera matrix $R\in\mathbb{R}^{4\times4}$ maps object point coordinates into their camera frame representation, this transformation is simply a rigid transformation in homogeneous coordinates.

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

Now that we have our previously found camera matrix $K$ and camera poses $R$ for each of the valid frames in our calibration setting, we can start to ask ourselves: what if there was a virtual cube on top of the checkerboard? How would it look like in our valid calibration images? To answer this questions we use the projective camera model we described at the beginning and assume the cube is parameterized by its vertices. To project the virtual cube onto our images, we simply apply the linear mapping $KR$ to all the vertices and draw lines between them accordingly to draw the cube. We can do this because of the fact that 3D lines are mapped into 2D lines when using a distorsion-free camera model.

To project our virtual cube, just run `python virtual-reality.py` and check `out/projected/` folder where you should find a set of images like these:

<p align="center">
<img src="https://user-images.githubusercontent.com/95151624/226233373-ece48423-2b41-4dcb-ada0-1ba2cb87fa29.gif"/>
</p>

Pretty cool, isn't it? Now you have a small glimpse on how virtual reality applications may be created. Of course, this is a simple case where we conveniently chose our object and our set of images to make a small demonstration. In practice, you may add more complex objects with textures as long as you have a way to describe them geometrically in object coordinate frame.

Another important caveat is that we conveniently used our calibrated views as the target images since we already knew the camera pose for those frames. In more complex scenarios, you are likely to have to localize your camera to correctly project your virtual objects.
