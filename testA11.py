import imageIO
import numpy 
import a11
import time
from halide import *

def main():
    # im=imageIO.imread('rgb.png')
    # lumi=im[:,:,1] #I'm lazy, I'll just use green
    # smallLumi=numpy.transpose(lumi[0:5, 0:5])

    # im_small = imageIO.imread('rgb-small.png')
    # lumi_small = im_small[:,:,1]
    # smallLumi_small = numpy.transpose(lumi_small[0:5, 0:5])

    # Replace if False: by if True: once you have implement the required functions. 
    # Exercises:
    if False:
        print 'Running smoothGradientNormalized'
        outputNP, myFunc=a11.smoothGradientNormalized()
        print ' Dimensionality of Halide Func:', myFunc.dimensions()
        imageIO.imwrite(outputNP, 'normalizedGradient.png')
    if False:
        print 'Running wavyRGB'
        outputNP, myFunc=a11.wavyRGB()
        print ' Dimensionality of Halide Func:', myFunc.dimensions()
        imageIO.imwrite(outputNP, 'rgbWave.png')
    if False:
        print 'Running lumninance'
        outputNP, myFunc=a11.luminance(im)
        print ' Dimensionality of Halide Func:', myFunc.dimensions()
        imageIO.imwrite(outputNP, 'lumiRGB.png')
    if False: 
        outputNP, myFunc=a11.sobel(lumi)
        imageIO.imwrite(outputNP, 'sobelMag.png')
        print ' Dimensionality of Halide Func:', myFunc.dimensions()

    if False: 
        L=a11.pythonCodeForBoxSchedule5(smallLumi)
        print L
    if False: 
        L=a11.pythonCodeForBoxSchedule6(smallLumi)
        print L
    if False: 
        L=a11.pythonCodeForBoxSchedule7(smallLumi)
        print L

    if False: 
        outputNP, myFunc=a11.localMax(lumi_small)
        print ' Dimensionality of Halide Func:', myFunc.dimensions()
        imageIO.imwrite(outputNP, 'maxi.png')

    if False: 
        input=Image(Float(32), lumi_small)
        xp, yp = Var('xp'), Var('yp')
        clamped = Func('clamped') 
        clamped[xp, yp] = input[clamp(xp, 0, input.width()-1),
                             clamp(yp, 0, input.height()-1)]
        sigma = 1.0
        blurX, finalBlur= a11.GaussianSingleChannel(clamped , sigma, trunc=3)
        output = finalBlur.realize(input.width(), input.height())
        outputNP = numpy.array(Image(output))
        print outputNP[outputNP < 0]
        imageIO.imwriteGrey(outputNP, "gaussian_blur.png")

    if False: 
        print 'Running harris corner detector'
        readstart = time.time()
        
        filen = "hk"
        print "Reading in file ", filen + ".png"
        im=numpy.load('Input/hk.npy')
        # im = imageIO.imread( filen + ".png")
        print "Reading in file took ... ", time.time() - readstart
        print "Running harris..."
        scheduleIndex= 1
        outputNP, myFunc=a11.harris(im, scheduleIndex)
        print ' Dimensionality of Halide Func:', myFunc.dimensions()
        imageIO.imwrite(outputNP, filen+'-harris.png')
        
    if True:
        print "Running harris autotune"
        im=numpy.load('Input/hk.npy')
        best_sched, best_params, best_time = a11.autotuneHarris(im)
        print "Best Schedule: ", best_sched
        print "Best Time: ", best_time
        print "Best Parameters: ", best_params
        
 
#the usual Python module business
if __name__ == '__main__':
    main()
