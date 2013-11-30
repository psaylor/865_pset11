import os, sys
from halide import *
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

def harris(im, scheduleIndex):
    ''' im is a numpy RGB array. 
    return the location of Harris corners like the reference Python code, but computed
    using Halide. 
    when scheduleIndex is zero, just schedule all the producers of non-local consumers as root.
    when scheduleIndex is 1, use a smart schedule that makes use of parallelism and 
    has decent locality (tiles are often a good option). Do not worry about vectorization. 
    Note that the local maximum criterion is simplified compared to our original Harris
    You might want to reuse or copy-paste some of the code you wrote above        
    Return a pair (outputNP, myFunc) where outputNP is a numpy array and myFunc is a Halide Func'''


## HELPERS ##
def clamp(a, mini, maxi):
    if a<mini: a=mini
    if a>maxi: a=maxi
    return a