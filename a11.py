import os, sys
from halide import *
import imageIO
import math
import time
# The only Halide module  you need is halide. It includes all of Halide


def smoothGradientNormalized():
    '''use Halide to compute a 512x512 smooth gradient equal to x+y divided by 1024
    Do not worry about the schedule. 
    Return a pair (outputNP, myFunc) where outputNP is a numpy array and myFunc is a Halide Func'''
    gradient = Func()

    x=Var()
    y=Var()

    e = x + y;
    e= cast(Float(32), e) / 1024

    gradient[x, y] = e
    output = gradient.realize(512, 512)    
    outputNP=numpy.array(Image(output))
    return (outputNP, gradient)

def wavyRGB():
    '''Use a Halide Func to compute a wavy RGB image like that obtained by the following 
    Python formula below. output[y, x, c]=(1-c)*cos(x)*cos(y)
    Do not worry about the schedule. 
    Hint : you need one more domain dimension than above
    Return a pair (outputNP, myFunc) where outputNP is a numpy array and myFunc is a Halide Func'''
    waveFunc = Func()
    x, y, c = Var(), Var(), Var()
    waveFunc[x, y, c] = cos(x)*cos(y)*(1-c)
    output = waveFunc.realize(400, 400, 3)    
    outputNP=numpy.array(Image(output))
    return (outputNP, waveFunc)


def luminance(im):
    '''input is assumed to be our usual numpy image representation with 3 channels. 
    Use Halide to compute a 1-channel image representing 0.3R+0.6G+0.1B
    Return a pair (outputNP, myFunc) where outputNP is a numpy array and myFunc is a Halide Func'''
    input = Image(Float(32), im)

    lumiFunc=Func()
    x, y = Var(), Var()

    lumiFunc[x, y] = 0.3*input[x,y,0] + 0.6*input[x,y,1] + 0.1*input[x,y,2]

    output = lumiFunc.realize(input.width(), input.height());
    outputNP=numpy.array(Image(output))
    return (outputNP, lumiFunc)


def  sobel(lumi):
    ''' lumi is assumed to be a 1-channel numpy array. 
    Use Halide to apply a Sobel filter and return the gradient magnitude. 
    Return a pair (outputNP, myFunc) where outputNP is a numpy array and myFunc is a Halide Func'''
    input = Image(Float(32), lumi)
    x, y = Var('x'), Var('y')
    
    gx = Func('gx') 
    gy = Func('gy') 
    gradientMagnitude=Func('gradientMagnitude') 

    clamped = Func('clamped') 
    clamped[x, y] = input[clamp(x, 0, input.width()-1), clamp(y, 0, input.height()-1)]
    height, width = lumi.shape[0:2]
    print 'height, width', height, width
    # clamped[x, y] = lumi[clamp(y, 0, height-1), clamp(x, 0, width-1)]

    gx[x,y]= (-clamped[x-1, y-1] + clamped[x+1, y-1]
            - 2*clamped[x-1, y] + 2*clamped[x+1, y] 
            - clamped[x-1, y+1] + clamped[x+1, y+1] )/4.0

    # Similarly define the vertical gradient. 
    gy[x,y]= (-clamped[x-1, y-1] + clamped[x-1, y+1]
            - 2*clamped[x, y-1] + 2*clamped[x, y+1] 
            - clamped[x+1, y-1] + clamped[x+1, y+1] )/4.0

    gradientMagnitude[x,y]= sqrt(gx[x,y]**2 + gy[x,y]**2)
    
    output = gradientMagnitude.realize(input.width(), input.height());
    outputNP=numpy.array(Image(output))

    return (outputNP, gradientMagnitude)

def sobel_x_y(clamped):
    x, y = Var('x'), Var('y')
    
    gx = Func('gx') 
    gy = Func('gy') 

    gx[x,y]= (-clamped[x-1, y-1] + clamped[x+1, y-1]
            - 2*clamped[x-1, y] + 2*clamped[x+1, y] 
            - clamped[x-1, y+1] + clamped[x+1, y+1] )/4.0

    # Similarly define the vertical gradient. 
    gy[x,y]= (-clamped[x-1, y-1] + clamped[x-1, y+1]
            - 2*clamped[x, y-1] + 2*clamped[x, y+1] 
            - clamped[x+1, y-1] + clamped[x+1, y+1] )/4.0

    
    return (gx, gy)


def pythonCodeForBoxSchedule5(lumi):    
    ''' lumi is assumed to be a 1-channel numpy array. 
    Write the python nested loops corresponding to the 3x3 box schedule 5
    and return a list representing the order of evaluation. 
    Each time you perform a computation of blur_x or blur_y, put a triplet with the name 
    of the function (string 'blur_x' or 'blur_y') and the output coordinates x and y. 
    e.g. [('blur_x', 0, 0), ('blur_y', 0,0), ('blur_x', 0, 1), ...] '''

    # schedule 5:
    # blur_y.compute_root() 
    # blur_x.compute_at(blur_y, x)

    height, width = lumi.shape[0:2]
    # compute blur_y at root
    evals = []
    for y in xrange(height):
        for x in xrange(width):
            # first compute blur_x
            evals.append( ('blur_x',x,y) )
            evals.append( ('blur_x',x,y+1) )
            evals.append( ('blur_x',x,y+2) )
            # then compute blur_y
            evals.append( ('blur_y',x,y) )
    return evals

def pythonCodeForBoxSchedule6(lumi):    
    ''' lumi is assumed to be a 1-channel numpy array. 
    Write the python nested loops corresponding to the 3x3 box schedule 5
    and return a list representing the order of evaluation. 
    Each time you perform a computation of blur_x or blur_y, put a triplet with the name 
    of the function (string 'blur_x' or 'blur_y') and the output coordinates x and y. 
    e.g. [('blur_x', 0, 0), ('blur_y', 0,0), ('blur_x', 0, 1), ...] '''

    # schedule 6:
    # blur_y.tile(x, y, xo, yo, xi, yi, 2, 2)
    # blur_x.compute_at(blur_y, yo)
    height, width = lumi.shape[0:2]
    evals = []

    for yo in xrange((height+1)/2): #+1 is here to get the ceiling
        # first compute blur_x inside yo loop
        for yi in xrange(2+2):
            y = yo*2+yi
            if y>= height: y=height-1
            for xi in xrange(width):
                # compute blur_x
                evals.append( ('blur_x', xi, y) )
        for xo in xrange((width+1)/2):
            # then compute blur_y
            for yi in xrange(2):
                y = yo*2+yi
                if y>= height: y=height-1
                for xi in xrange(2):
                    x = xo*2+xi
                    if x>= width: x=width-1
                    evals.append( ('blur_y', x, y) )
    return evals

def pythonCodeForBoxSchedule7(lumi):    
    ''' lumi is assumed to be a 1-channel numpy array. 
    Write the python nested loops corresponding to the 3x3 box schedule 5
    and return a list representing the order of evaluation. 
    Each time you perform a computation of blur_x or blur_y, put a triplet with the name 
    of the function (string 'blur_x' or 'blur_y') and the output coordinates x and y. 
    e.g. [('blur_x', 0, 0), ('blur_y', 0,0), ('blur_x', 0, 1), ...] '''

    # schedule 7
    # blur_y.split(x, xo, xi, 2)
    # blur_x.compute_at(blur_y, y)
    height, width = lumi.shape[0:2]
    factor = 2
    evals = []

    for y in xrange(height):
        # compute blur_x
        for x in xrange(width):
            evals.append( ('blur_x',x,y) )

        for xo in xrange((width+(factor-1))/factor):
            for xi in xrange(factor):
                #compute blur_y
                x = xo*factor + xi
                if x>=width: x=width-1
                evals.append( ('blur_y',x,y) )
            
    return evals


########### PART 2 ##################

def localMax(lumi):
    ''' the input is assumed to be a 1-channel image
    for each pixel, return 1.0 if it's a local maximum and 0.0 otherwise
    Don't forget to handle pixels at the boundary.
    Return a pair (outputNP, myFunc) where outputNP is a numpy array and myFunc is a Halide Func'''
    input = Image(Float(32), lumi)
    x, y = Var('x'), Var('y')
    locMax = Func('localMax')

    clamped = Func('clamped') 
    clamped[x, y] = input[clamp(x, 0, input.width()-1), clamp(y, 0, input.height()-1)]

    localMaxCondition = (input[x,y]>clamped[x,y+1]) & (input[x,y]>clamped[x+1,y+1]) & (input[x,y]>clamped[x,y-1]) & (input[x,y]>clamped[x-1,y-1])
    locMax[x,y] = select(localMaxCondition , 1.0, 0.0)

    output = locMax.realize(input.width(), input.height())
    outputNP=numpy.array(Image(output))
    
    return (outputNP, locMax)


def GaussianSingleChannel(input, sigma, trunc=3):
    '''takes a single-channel image or Func IN HALIDE FORMAT as input 
        and returns a Gaussian blurred Func with standard 
        deviation sigma, truncated at trunc*sigma on both sides
        return two Funcs corresponding to the two stages blurX, blurY. This will be
        useful later for scheduling. 
        We advise you use the sum() sugar
        We also advise that you first generate the kernel as a Halide Func
        You can assume that input is a clamped image and you don't need to worry about
        boundary conditions here. See calling example in test file. '''

    blurX = Func('blurX')
    blurY = Func('blurY')
    x = Var('x')
    y = Var('y')
    r = Var('r')

    gaussKernel = Func('gaussianKernel')
    gaussKernel[r] = exp((-1.0 * (r**2) )/ (2.0 * sigma**2))/ ( sigma * sqrt(2* math.pi) )

    half_kernel_width = int( sigma*trunc )

    red = RDom(-half_kernel_width, 2*half_kernel_width +1, 'red_x')
    blurX[x,y] = sum(input[x+red.x, y] * gaussKernel[red.x])
    blurY[x,y] = sum(blurX[x, y+red.x] * gaussKernel[red.x])
    return (blurX, blurY)

def GaussianSingleChannelWithKernel(input, sigma, gaussKernel=0, trunc=3):
    '''takes a single-channel image or Func IN HALIDE FORMAT as input 
        and returns a Gaussian blurred Func with standard 
        deviation sigma, truncated at trunc*sigma on both sides
        return two Funcs corresponding to the two stages blurX, blurY. This will be
        useful later for scheduling. 
        We advise you use the sum() sugar
        We also advise that you first generate the kernel as a Halide Func
        You can assume that input is a clamped image and you don't need to worry about
        boundary conditions here. See calling example in test file. '''

    blurX = Func('blurX')
    blurY = Func('blurY')
    x = Var('x')
    y = Var('y')
    r = Var('r')

    if gaussKernel==0:
        gaussKernel = Func('gaussianKernel')
        gaussKernel[r] = exp((-1.0 * (r**2) )/ (2.0 * sigma**2))/ ( sigma * sqrt(2* math.pi) )

    half_kernel_width = int( sigma*trunc )

    red = RDom(-half_kernel_width, 2*half_kernel_width +1, 'red_x')
    blurX[x,y] = sum(input[x+red.x, y] * gaussKernel[red.x])
    blurY[x,y] = sum(blurX[x, y+red.x] * gaussKernel[red.x])
    return (blurX, blurY, gaussKernel)

def harris(im, scheduleIndex):
    ''' im is a numpy RGB array. 
    return the location of Harris corners like the reference Python code, but computed
    using Halide. 
    when scheduleIndex is zero, just schedule all the producers of non-local consumers as root. 
        (producers for localmax and blur)
    when scheduleIndex is 1, use a smart schedule that makes use of parallelism and 
    has decent locality (tiles are often a good option). Do not worry about vectorization. 
    Note that the local maximum criterion is simplified compared to our original Harris
    You might want to reuse or copy-paste some of the code you wrote above        
    Return a pair (outputNP, myFunc) where outputNP is a numpy array and myFunc is a Halide Func'''
    (locMax, threshold, M, trace, det, ixiy, blurIxIyX, iy2, blurIy2X, ix2, blurIx2X, temp_ixiy, temp_iy2, temp_ix2, gx, gy, blurX, finalBlur, gKern, clamped_lumi, lumi, input) = harris_algorithm(im)

    if (scheduleIndex == 0):
        print "Compute_root scheduling..."
        # just schedule all the producers of non-local consumers as root
        clamped_lumi.compute_root()
        blurX.compute_root()
        blurIx2X.compute_root()
        blurIy2X.compute_root()
        blurIxIyX.compute_root()
        finalBlur.compute_root()
        temp_ix2.compute_root()
        temp_iy2.compute_root()
        temp_ixiy.compute_root()
        M.compute_root()
        gKern.compute_root()

    else:
        print "Fast Scheduling..."
        # use a smart schedule that makes use of parallelism and  has decent locality (tiles are often a good option)
        x, y, xo, yo, xi, yi = Var('x'), Var('y'), Var('xo'), Var('yo'), Var('xi'), Var('yi')

        finalBlur.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64) \
            .parallel(yo)
        
        ix2.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64) \
            .parallel(yo)
        iy2.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64) \
            .parallel(yo)
        ixiy.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64) \
            .parallel(yo)

        blurIx2X.compute_at(ix2, xo)
        blurIy2X.compute_at(iy2, xo)
        blurIxIyX.compute_at(ixiy, xo)
        blurX.compute_at(finalBlur, xo)
        
        temp_ix2.compute_at(ix2, xo)
        temp_iy2.compute_at(iy2, xo)
        temp_ixiy.compute_at(ixiy, xo)

        clamped_lumi.compute_root()
        
        locMax.tile(x,y,xo,yo,xi,yi,128,64)
        locMax.parallel(yo)
        M.compute_at(locMax, xo)
       
        gKern.compute_root()
    
    print "Compiling Halide Code..."
    compstart = time.time()
    locMax.compile_jit()
    t=time.time()
    print "Compiling took... ", t - compstart, " seconds"
    output = locMax.realize(input.width(), input.height())
    dt = time.time() - t
    print '     Harrris took: ', dt , ' seconds'
    mpix=input.width()*input.height()/1e6
    print  '%.5f ms per megapixel (%.7f ms for %d megapixels)' % (dt/mpix*1e3, dt*1e3, mpix) 
    outputNP=numpy.array(Image(output))

    return (outputNP, locMax)


def harris_algorithm(im):
    ''' Return a pair (outputNP, myFunc) '''
    input = Image(Float(32), im)
    sigmaG = 1.0
    factor = 4
    k = 0.15
    thr = 0.0

    x, y, c = Var('x'), Var('y'), Var('c')
    lumi = Func('luminance')
    clamped_lumi = Func('clamped') 
    temp_ix2 = Func('temp_ix2')
    temp_iy2 = Func('temp_iy2')
    temp_ixiy= Func('temp_ixiy')
    det = Func('determinant')
    trace = Func('trace')
    M = Func('M')
    threshold = Func('threshold')
    locMax = Func('localMaximum')

    # print "compute luminance and blur"
    lumi[x,y] = input[x,y,0]*0.3 + input[x,y,1]*0.6 + input[x,y,2]*0.1
    clamped_lumi[x, y] = lumi[clamp(x, 0, input.width()-1), clamp(y, 0, input.height()-1)]
    blurX, finalBlur, gKern = GaussianSingleChannelWithKernel(clamped_lumi, sigmaG)

    # print "compute gradient"
    (gx, gy) = sobel_x_y(finalBlur)

    # print 'form tensor'
    temp_ix2[x,y] = gx[x,y]**2
    temp_iy2[x,y] = gy[x,y]**2
    temp_ixiy[x,y] = gx[x,y] * gy[x,y]

    # print 'blur tensor'
    (blurIx2X, ix2, throw) = GaussianSingleChannelWithKernel(temp_ix2, sigmaG*factor, gKern)
    (blurIy2X, iy2, throw) = GaussianSingleChannelWithKernel(temp_iy2, sigmaG*factor, gKern)
    (blurIxIyX, ixiy, throw) = GaussianSingleChannelWithKernel(temp_ixiy, sigmaG*factor, gKern)

    # print 'determinant of tensor'
    det[x,y] = (ix2[x,y]*iy2[x,y]) - ixiy[x,y]**2
    # trace of tensor
    trace[x,y] = ix2[x,y] + iy2[x,y]

    # print 'Harris response'
    M[x,y] = det[x,y] - k*trace[x,y]**2

    # print 'threshold'
    threshold[x,y] = select(M[x,y] > thr, 1.0, 0.0)

    # print 'local maximum'
    localMaxCondition = (M[x,y]>M[x,y+1]) & (M[x,y]>M[x+1,y+1]) & (M[x,y]>M[x,y-1]) & (M[x,y]>M[x-1,y-1])
    locMax[x,y] = select(localMaxCondition , threshold[x,y], 0.0)

    return (locMax, threshold, M, trace, det, ixiy, blurIxIyX, iy2, blurIy2X, ix2, blurIx2X, temp_ixiy, temp_iy2, temp_ix2, gx, gy, blurX, finalBlur, gKern, clamped_lumi, lumi, input)

def autotuneHarris(im):
    height, width = im.shape[0:2]
    tile_dims = [32, 64, 128, 256]
    best_time = -1
    best_schedule = -1
    best_params = dict()
        
    # Schedule 1: Tile locMax and schedule everything at xo
    for y_tile_size in tile_dims:
        for x_tile_size in tile_dims:
            # Get the Algorithm
            print "Tuning Schedule 1 | y_tile_size=",y_tile_size, ", x_tile_size=", x_tile_size
            (locMax, threshold, M, trace, det, ixiy, blurIxIyX, iy2, blurIy2X, ix2, blurIx2X, temp_ixiy, temp_iy2, temp_ix2, gx, gy, blurX, finalBlur, gKern, clamped_lumi, lumi, input) = harris_algorithm(im)
            
            # Set the schedule
            x, y, xo, yo, xi, yi = Var('x'), Var('y'), Var('xo'), Var('yo'), Var('xi'), Var('yi')   
            locMax.tile(x,y,xo,yo,xi,yi, y_tile_size, x_tile_size)
            locMax.parallel(yo)
            clamped_lumi.compute_at(locMax, yo)
            gKern.compute_at(locMax, xo)
            finalBlur.compute_at(locMax, xo)
            temp_ix2.compute_at(locMax, xo)
            temp_iy2.compute_at(locMax, xo)
            temp_ixiy.compute_at(locMax, xo)
            
            blurX.compute_at(locMax, xo)
            blurIx2X.compute_at(locMax, xo)
            blurIy2X.compute_at(locMax, xo)
            blurIxIyX.compute_at(locMax, xo)
            
            M.compute_at(locMax, xo)
            
            # Time it
            runTime = runAndMeasure(locMax, input.width(), input.height())
            
            # Check if best
            if runTime < best_time or (best_time == -1):
                best_time = runTime
                best_schedule = 1
                best_params = { "y_tile_size": y_tile_size, "x_tile_size": x_tile_size }
    
    # Schedule 2: Compute Blurs at root in tiles
    for y_tile_size in tile_dims:
        for x_tile_size in tile_dims:
            print "Tuning Schedule 1 | y_tile_size=",y_tile_size, ", x_tile_size=", x_tile_size
            (locMax, threshold, M, trace, det, ixiy, blurIxIyX, iy2, blurIy2X, ix2, blurIx2X, temp_ixiy, temp_iy2, temp_ix2, gx, gy, blurX, finalBlur, gKern, clamped_lumi, lumi, input) = harris_algorithm(im)
            
            clamped_lumi.compute_root()
            gKern.compute_root()
            finalBlur.compute_root() \
                .tile(x, y, xo, yo, xi, yi, 128, 64) \
                .parallel(yo)
            ix2.compute_root() \
                .tile(x, y, xo, yo, xi, yi, 128, 64) \
                .parallel(yo)
            iy2.compute_root() \
                .tile(x, y, xo, yo, xi, yi, 128, 64) \
                .parallel(yo)
            ixiy.compute_root() \
                .tile(x, y, xo, yo, xi, yi, 128, 64) \
                .parallel(yo)

            blurIx2X.compute_at(ix2, xo)
            blurIy2X.compute_at(iy2, xo)
            blurIxIyX.compute_at(ixiy, xo)
            blurX.compute_at(finalBlur, xo)
        
            temp_ix2.compute_at(ix2, xo)
            temp_iy2.compute_at(iy2, xo)
            temp_ixiy.compute_at(ixiy, xo)

            locMax.tile(x,y,xo,yo,xi,yi,128,64)
            locMax.parallel(yo)
            M.compute_at(locMax, xo)
        
            
                   
    return best_schedule, best_params, best_time
            
def runAndMeasure(myFunc, w, h):
    myFunc.compile_jit()    
    
    t=time.time()
    output = myFunc.realize(w,h)
    dt = time.time() - t
    
    hIm=Image(output)
    mpix=hIm.width()*hIm.height()/1e6
    print 'best: ', dt
    print  '%.5f ms per megapixel (%.7f ms for %d megapixels)' % (dt/mpix*1e3, dt*1e3, mpix)
    return dt            
    

