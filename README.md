# Buddhabrot - a ghostly probability distribution related to the Mandelbrot set

![Buddhabrot False-colour](./examples/FalseColour.png)

The Buddhabrot is a beautiful fractal shape, generated through similar iterations to Mandelbrot set images. A brief description can be found below and more details can be found at https://en.wikipedia.org/wiki/Buddhabrot.

Buddhabrot visualises a probability distribution over the complex numbers. We start by paritioning the complex plane into bins. Complex numbers are sampled uniformly from a circular region around the origin of the complex plane, then iterated according to the same rule as the Mandelbrot set: Z(n) = Z(n-1)^2 + c, where c is the sampled point and Z(0) = 0. If the point remains close to the origin after a predefined number of iterations k, we discard the sample, however if the point diverges then we increment each bin associated with a point in {Z(0),...,Z(k)}. By sampling many points this gives us a tally accross all the bins. Then, by normalising these bin frequencies to values between 0 and 1, we can turn this into a greyscale image. 

Further, by creating 3 different tallies with a different number of iterations, we can create a false colour image whose colours come from the 3 tallies (one for red, green and blue, giving an RGB pixel). The image at the top of the page is composed of the following three greyscale images: red with k = 5000, green with k = 500 and blue with k = 50
![Buddhabrot False-colour-red](./examples/FalseColourRed.png) ![Buddhabrot False-colour-green](./examples/FalseColourGreen.png) ![Buddhabrot False-colour-blue](./examples/FalseColourBlue.png)

These differences mean that the only real parameters to the images are the samplesize, the max number of iteraions and the resolution of the image. As each pixel is a bin, resolution doesn't actually increase compute time (unlike for Mandelbrot images) but the samplesize and max number of iterations do.

To generate your own images, you can run `generate_greyscale.py` or `generate_rgb.py`. Adding a `-h` flag will show options for customising the output image. Note that these scrips will look for existing tallies stored in the `csvs` directory with the specified resolution and iterlimit. The number of new points specified will then be sampled and either added to an existing tally (if it exists) or to a zero-matrix. You can force a fresh start with the flag `--fresh`.
