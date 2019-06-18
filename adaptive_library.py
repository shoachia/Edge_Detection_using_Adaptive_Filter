import matplotlib
from skimage.io import imread
from skimage import filters
from skimage.color import rgb2gray
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt


def rgb2edge(img,Gaussian = True):
    grayImage = rgb2gray(img)
    if Gaussian == True:
        img = filters.gaussian(grayImage)
    edges = filters.sobel(grayImage)
    #plt.figure()
    plt.imshow(edges,cmap = 'gray')
    return edges

def normalize(arr):
    arr -= arr.min()
    if arr.max() == 0:
        return arr
    arr /= arr.max()
    return arr

def psnr(x,x0):
    n1, n2 = x.shape[:2]
    c = x.shape[2] if x.ndim == 3 else 1
    return 10*np.log10(n1*n2*c/(np.linalg.norm(x-x0)**2))

def adaptive_denoise(correct,y,it = 7):# usually the number of iters is 1 ~ 10
    img = y
    row = img.shape[0]
    col = img.shape[1]
    err = 0
    rec = []
    rec2 = []
    for cnt in range(it):
        prev = np.copy(img)
        prev_err = err
        R = img[:,:,0]
        G = img[:,:,1]
        B = img[:,:,2]
        for i in range(1,row-1):
            for j in range(1,col-1):
                ## loop the kernel
                d =np.zeros((3,3))
                for n1 in range(-1,2):
                    for n2 in range(-1,2):
                
                        d[n1+1][n2+1] = (np.abs(R[i][j]-R[i+n1][j+n2]) + np.abs(G[i][j]-G[i+n1][j+n2]) 
                                         + np.abs(B[i][j]-B[i+n1][j+n2]))/3
                c = (1-d)**10 ## 10 has the best peformance
                R[i,j] = (c * R[i-1:i+2,j-1:j+2]).sum()/c.sum()
                G[i,j] = (c * G[i-1:i+2,j-1:j+2]).sum()/c.sum()
                B[i,j] = (c * B[i-1:i+2,j-1:j+2]).sum()/c.sum()
                
        img[:,:,0] = R
        img[:,:,1] = G
        img[:,:,2] = B        
        
        cnt += 1
        err = psnr(correct[1:row-1,1:col-1,:],img[1:row-1,1:col-1,:])
        rec.append(psnr(img,prev))
        rec2.append(err)
        print("SNR = " + str(err))
        if psnr(img,prev) >= 35:
            return prev,prev_err,rec,rec2
    return img,prev_err,rec,rec2
                    
