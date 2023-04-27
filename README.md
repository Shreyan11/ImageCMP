# ImageCMP
A simple application for finding the flawed products in a factory line
What it can do: Take an image,compare it with the images(of a product) in a particular database,and then segregate them in 2 seperate folders as good or bad. 
The main algorithm chosen for this application is the structural similarity index. Here's why I chose it:
 
1)Most Image quality assessment techniques rely on quantifying errors between a reference and a sample image. A common metric is to quantify the difference in the values of each of the corresponding pixels between the sample and the reference images (By using, for example, Mean Squared Error).

2)The Human visual perception system is highly capable of identifying structural information from a scene and hence identifying the differences between the information extracted from a reference and a sample scene. Hence, a metric that replicates this behavior will perform better on tasks that involve differentiating between a sample and a reference image.

The Structural Similarity Index (SSIM) metric extracts 3 key features from an image:

    1.Luminance,measured by averaging over all the pixel values.
    2.Contrast,measured by taking the standard deviation (square root of variance) of all the pixel values.
    3.Structure,done by using a consolidated formula that divides the input signal with its standard deviation so that the result has unit standard deviation which allows for       more robust comparison.

The comparison between the two images is performed on the basis of these 3 features.

In simple words,it's like a ruler for comparing pictures, but instead of just measuring the length and width, it looks at the pattern of colors in the pictures.
Most importantly,SSIM is better than other image comparison algorithms because it's designed to take into account how humans perceive images. It's more sensitive to small differences in patterns and colors, and it's better at predicting how people will perceive the quality of an image. Other algorithms like Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR) just look at the overall brightness and color of the images, but they don't consider the patterns in the pictures. So they might miss some important details that SSIM can pick up on.

That being said,in order to test it and ,please select ref.jpg as your reference image and select the test folder in order to test it out.

Run it by using python mainapp.py

I'm open to all the pull requests,thanks for visiting this repo
