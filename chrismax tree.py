"""
    Reference from::
    (1)
Link: http://codegolf.stackexchange.com/questions/15860/make-a-scalable-christmas-tree/16358#16358
Author: Franz Navarro - CAChemE.org 
    (2)
Link: https://www.wongwonggoods.com/python/opencv-make-video/
Author: Howard Weng

    My version::
Author:John Blue 
Dependencies: Python, NumPy, matplotlib, math, io, os, cv2, glob
"""

import io
import os
import math
import glob
import cv2
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# time const
Tm = 180

def ind_pic(ind):
    # Calculate spiral coordinates for the Xmas tree
    #rto = (ind + 1) / Tm
    #rto = math.log10((ind + 3) * 10 / Tm)
    rv = (ind + 1) / Tm
    rto = rv * rv * rv
    Den = 300
    theta = np.linspace(- 6 * np.pi, - 6 * np.pi + 12 * np.pi * rto, Den)
    #theta = np.linspace(- 3 * np.pi, - 3 * np.pi + 6 * np.pi * rto, Den) 
    z = np.linspace(- 3, -3 + 3 * rto, Den)
    r = 5
    x = r * np.sin(theta) * z
    y = r * np.cos(theta) * z
     
    # Use matplotib and its OOP interface to draw it 
    fig = plt.figure() # Create figure
    ax = fig.gca(projection='3d') # It's a 3D Xmas tree!
    ax.view_init(15, 0) # Set a nice view angle
    ax._axis3don = False # Hide the 3d axes
    ax.set_facecolor((0.0, 0.0, 0.3))

    # Plot the Xmas tree as a line
    ax.plot(x, y, z, c='green', linewidth=2.5)

    # Every Xmas tree needs a star
    if ind > Tm * 0.99:
        ax.scatter(0, 0, 0.2, c='#9467bd', s=1800, marker='*')
        ax.scatter(0, 0, 0.2, c='yellow', s=1200, marker='*')
        #'#9467bd', '#8c564b', '#e377c2', '#17becf'

    # Star
    np.random.seed(19680801)
    N = 333
    xs = (np.random.rand(N) - 0.5) * 33
    ys = (np.random.rand(N) - 0.5) * 33
    zs = np.random.rand(N) * (- 5) + 2
    colors = np.random.rand(N)
    colorset = []
    for i in colors:
        colorset.append(1 - math.exp(- 3 * i))
    ax.scatter(xs, ys, zs, c=colorset, alpha=0.5, marker='*')

    # Set axis range
    ax.set_xlim3d(- 10, 10)
    ax.set_ylim3d(- 10, 10)
    ax.set_zlim3d(- 2.7, - 0.3)

    # Type here your best whishes
    ax.set_title(u"Merry Chrixmas")
    
    # Save
    if ind < 100:
        plt.savefig('0' + str(ind) + '.png')
        return
    plt.savefig(str(ind) + '.png')
    
    # Show
    #plt.show()
    
    # Close
    ax.cla()
    fig.clf()
    plt.clf()
    plt.close('all')
    
    
    
def film():
    path = "*.png" 
    result_name = 'CMTree.mp4'

    frame_list = sorted(glob.glob(path))
    print("frame count: ",len(frame_list))

    fps = 30
    shape = cv2.imread(frame_list[0]).shape # delete dimension 3
    size = (shape[1], shape[0])
    print("frame size: ",size)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_name, fourcc, fps, size)

    for idx, path in enumerate(frame_list):
        frame = cv2.imread(path)
        print("\rMaking videos: {}/{}".format(idx+1, len(frame_list)), end = "")
        current_frame = idx+1
        total_frame_count = len(frame_list)
        percentage = int(current_frame*30 / (total_frame_count+1))
        print("\rProcess: [{}{}] {:06d} / {:06d}".format("#"*percentage, "."*(30-1-percentage), current_frame, total_frame_count), end ='')
        out.write(frame)

    out.release()



if __name__ == '__main__':
    # Making list of png
    for i in range(Tm):
        ind_pic(i)
    
    # Making film
    film()
    
    # Delete png
    for file in os.listdir():
        if file.endswith('.png'):
            os.remove(file)