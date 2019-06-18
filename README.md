# Edge Detection using Adaptive Filter
---
### 1. Introduction
Edge detection is one of the most common used technique in image analysis. It is also a critical element in image processing since edge contains lots of useful information. An edge can be describe as as a boundary between two regions separated by distinction in strong intensity values of the pixels. Edge detection can be define as a process of finding and tracing sharp discontinuities in the image. It has been widely used in object recognition, feature extraction, and image analysis. For example, most features extracted by algorithms are based on corners which have high correlation with edges. There are several kinds of edge detection methods such as Sobel, Perwitt , and the most popular one – Canny detector. However, all of the among detectors have encountered artifacts that caused by noise.Therefore, noise reduction becomes an important issue in edge detection.
### 2. Dataset 
In this paper, we performed our algorithm on **Color BSD68 dataset(CBSD68)**. This benchmark dataset is widely used for measuring image denoising algorithms performance. It includes the original .jpg files, converted to lossless .png, and noisy with Additive White Gaussian Noise of different levels.

### 3. Noise Reduction
The Adaptive smoothing is a class of typical nonlinear smoothing technique. The edge preserve smoothing algorithm is applied independently to every image pixel using different coefficients. To calculate the coefficients of the convolution mask for every pixels, Manhattan color distances ![](https://i.imgur.com/Q0iXp3s.png) are extracted between the central pixel and the eight neighboring pixels in a 3x3 sliding window, which are normalized in the range [0,1].

That is, 

![](https://i.imgur.com/60lLZGf.png)

where ![](https://i.imgur.com/zlpQsoR.png) is the central pixel value in the current sliding window.

After calculating the color distance between its neighborhoods, we can evaluate the weights based on these values(kernel coefficients). The following equation is used:

![](https://i.imgur.com/AaKJa8A.png)

In words, ![](https://i.imgur.com/PAR4Bqs.png) receives larger values for smaller color distance so pixels
having small color distance from the central pixel receive large weights. This concludes to the following convolution mask:

![](https://i.imgur.com/5RIDyS1.png)

The filtering of the image is achieved by applying the above convolution mask on RGB channels respectively. Factor p in equation(2) scales exponentially the color distance which means that it controls the blur effect on the edges.

The next step is filter the image iteratively. In each iteration, the image is filtered by a convolution mask with different coefficients which means the filter process is based on image itself. That's why we called it adaptive filtering. 

When the adaptive filter is applied to boundary pixels of an object, the color distances $d_i$ take large values for the neighboring pixels that do not belong to the object, and hence the colors of these neighboring pixels have a small weights on the final color received by the central pixel. For this reason, the proposed adaptive filter can be considered as edge preserving filter. **In other words, you can also consider the convolution kernel as a process of checking whether the central pixel belongs to its surrounding neighboring pixels.**

* **p-degree Parameter Tuning**
  p plays an important role in this algorithm since it controls how blurry should the edge becomes. If p = 1, the filter is approximate to the box kernel which means that the blurry effect is very large and the information on edges can be ignored. As p gets larger, coefficients with small color distance from the central pixel increase their relative value difference from coefficients with large color distance, so the blurring effect decreases. A fixed value p = 10 is used for all of our experiments because this resulted in very good performance. The central pixel of the convolution mask is set to zero to remove impulsive noise.
* **Number of Iterations Selection**
    Numbers of iteration is another critical factor. It reduces number of color levels in the image. As the it gets larger, the clear edge will be enhanced but implicit edge(subtle features) in the object will be ignored. Therefore, the more the number of iteration does not means to get better SNR. To solve this problem, we terminate the iteration when the variation between two iterations are sufficient small. Although we cannot use gradient descent to calculate loss function since we do not include clean image in our algorithm, we can still compare the SNR between current output and previous to see whether the variation is small enough.
### 4. Result
**Example Image 1 (noisy35)**
![](https://i.imgur.com/iKZwJlL.png)
**1. Using Gaussian Blur**
![](https://i.imgur.com/VB2JGJ1.png)
**2. Using Adaptive Filter**
![](https://i.imgur.com/17lGcE9.png)
**Example Image 2 (noisy35)**
![](https://i.imgur.com/vJsDIQ2.png)

**1. Using Gaussian Blur**
![](https://i.imgur.com/4VP8kxD.png)

**2. Using Adaptive Filter**
![](https://i.imgur.com/VjVb7Tx.png)

**Curve of SNR**
Use to terminate the iterations
The left image is the SNR between current output an the clean image, while the left one is the SNR between current output and the previous output
![](https://i.imgur.com/TIIxeni.png)
