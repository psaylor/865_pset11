865_pset11
==========

Schedule root:
Harrris took:  8.22174715996  seconds
30085.43311 ms per megapixel (8221.7471600 ms for 0 megapixels)

Schedule
========
xo, yo, xi, yi = Var('xo'), Var('yo'), Var('xi'), Var('yi')

clamped_lumi.compute_root()
finalBlur.compute_root()
temp_ix2.compute_root()
temp_iy2.compute_root()
temp_ixiy.compute_root()

locMax.tile(x, y, xo, yo, xi, yi, 128, 128)
locMax.parallel(yo)
M.compute_at(locMax, xo)

Times
=====
Harrris took:  4.581346035  seconds
16764.29316 ms per megapixel (4581.3460350 ms for 0 megapixels)

Schedule:
==========
xo, yo, xi, yi = Var('xo'), Var('yo'), Var('xi'), Var('yi')

clamped_lumi.compute_root()
finalBlur.compute_root()
temp_ix2.compute_root()
temp_iy2.compute_root()
temp_ixiy.compute_root()

M.tile(x, y, xo, yo, xi, yi, 128, 128)
M.parallel(yo)
M.compute_root()

Time:
=====
Harrris took:  5.10623002052  seconds
18684.97519 ms per megapixel (5106.2300205 ms for 0 megapixels)

Compiling took...  2.30617189407  seconds
     Harrris took:  511.315901041  seconds
14301.21657 ms per megapixel (511315.9010410 ms for 35 megapixels)


==========
Schedule:
==========
        xo, yo, xi, yi = Var('xo'), Var('yo'), Var('xi'), Var('yi')

        locMax.tile(x, y, xo, yo, xi, yi, 128, 128)
        locMax.parallel(yo)
        M.compute_at(locMax, xo)

        clamped_lumi.compute_at(locMax, xo)
        finalBlur.compute_at(locMax, xo)
        temp_ix2.compute_at(locMax, xo)
        temp_iy2.compute_at(locMax, xo)
        temp_ixiy.compute_at(locMax, xo)

Time:
=====

On ATHENA
schedule
clamped_lumi.compute_at(locMax, yo)
        finalBlur.compute_at(locMax, xo)
        temp_ix2.compute_at(locMax, xo)
        temp_iy2.compute_at(locMax, xo)
        temp_ixiy.compute_at(locMax, xo)
        
        locMax.tile(x,y,xo,yo,xi,yi,128,64)
        locMax.parallel(yo)
        M.compute_at(locMax, xo)
        blurX.compute_at(locMax, xo)
        blurIx2X.compute_at(locMax, xo)
        blurIy2X.compute_at(locMax, xo)
        blurIxIyX.compute_at(locMax, xo)
time:  Harrris took:  296.089745045  seconds
8281.46271 ms per megapixel (296089.7450447 ms for 35 megapixels)

psaylor@W20-575-54:~/Desktop/6.865/865_pset11$ python harris-numpy.py 
took  110.85048604 seconds
3100.42540 ms per megapixel (110850.4860401 ms for 35 megapixels)
 python harris-numpy.py 
took  87.7264151573 seconds
2453.65822 ms per megapixel (87726.4151573 ms for 35 megapixels)
Schedule
clamped_lumi.compute_at(locMax, yo)
        finalBlur.compute_at(locMax, xo)
        temp_ix2.compute_at(locMax, xo)
        temp_iy2.compute_at(locMax, xo)
        temp_ixiy.compute_at(locMax, xo)
        
        locMax.tile(x,y,xo,yo,xi,yi,128,64)
        locMax.parallel(yo)
        M.compute_at(locMax, xo)
        blurX.compute_at(locMax, xo)
        blurIx2X.compute_at(locMax, xo)
        blurIy2X.compute_at(locMax, xo)
        blurIxIyX.compute_at(locMax, xo)
        gKern.compute_at(locMax, xo)
Harrris took:  47.6152210236  seconds
1331.77080 ms per megapixel (47615.2210236 ms for 35 megapixels)


Schedule
        xo, yo, xi, yi = Var('xo'), Var('yo'), Var('xi'), Var('yi')

        # blurX.compute_root()
        
        # locMax.tile(x, y, xo, yo, xi, yi, 128, 64)
        # locMax.parallel(yo)
        # M.compute_at(locMax, xo)

        finalBlur.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64)
        
        ix2.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64)
        iy2.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64)
        ixiy.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64)

        blurIx2X.compute_at(ix2, xo)
        blurIy2X.compute_at(iy2, xo)
        blurIxIyX.compute_at(ixiy, xo)
        blurX.compute_at(finalBlur, xo)
        
        temp_ix2.compute_at(ix2, xo)
        temp_iy2.compute_at(iy2, xo)
        temp_ixiy.compute_at(ixiy, xo)

        # clamped_lumi.compute_at(locMax, xo)
        # finalBlur.compute_at(locMax, xo)
        # temp_ix2.compute_at(locMax, xo)
        # temp_iy2.compute_at(locMax, xo)
        # temp_ixiy.compute_at(locMax, xo)

        clamped_lumi.compute_root()
        # finalBlur.compute_at(locMax, xo)
        
        locMax.tile(x,y,xo,yo,xi,yi,128,64)
        locMax.parallel(yo)
        M.compute_at(locMax, xo)
        
       
        #gKern.compute_at(locMax, xo)
        gKern.compute_root()
time: Harrris took:  89.8819320202  seconds
2513.94681 ms per megapixel (89881.9320202 ms for 35 megapixels)



Schedule w/ compute rooting tiled blurs and parallelism
========
      xo, yo, xi, yi = Var('xo'), Var('yo'), Var('xi'), Var('yi')

        # blurX.compute_root()
        
        # locMax.tile(x, y, xo, yo, xi, yi, 128, 64)
        # locMax.parallel(yo)
        # M.compute_at(locMax, xo)

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

        # clamped_lumi.compute_at(locMax, xo)
        # finalBlur.compute_at(locMax, xo)
        # temp_ix2.compute_at(locMax, xo)
        # temp_iy2.compute_at(locMax, xo)
        # temp_ixiy.compute_at(locMax, xo)

        clamped_lumi.compute_root()
        # finalBlur.compute_at(locMax, xo)
        
        locMax.tile(x,y,xo,yo,xi,yi,128,64)
        locMax.parallel(yo)
        M.compute_at(locMax, xo)
        
       
        #gKern.compute_at(locMax, xo)
        gKern.compute_root()
time:
 Harrris took:  46.3150889874  seconds
1295.40685 ms per megapixel (46315.0889874 ms for 35 megapixels)


Schedule not the best
========
        xo, yo, xi, yi = Var('xo'), Var('yo'), Var('xi'), Var('yi')

        # blurX.compute_root()
        
        # locMax.tile(x, y, xo, yo, xi, yi, 128, 64)
        # locMax.parallel(yo)
        # M.compute_at(locMax, xo)

        finalBlur.compute_root() \
            .tile(x, y, xo, yo, xi, yi, 128, 64) \
            .parallel(yo)
        
        ix2.compute_at(locMax, xo) \
            .tile(x, y, xo, yo, xi, yi, 32, 32) \
            .parallel(yo)
        iy2.compute_at(locMax, xo) \
            .tile(x, y, xo, yo, xi, yi, 32, 32) \
            .parallel(yo)
            
        ixiy.compute_at(locMax, xo) \
            .tile(x, y, xo, yo, xi, yi, 128, 64) \
            .parallel(yo)

        blurIx2X.compute_at(ix2, xo)
        blurIy2X.compute_at(iy2, xo)
        blurIxIyX.compute_at(ixiy, xo)
        blurX.compute_at(finalBlur, xo)
        
        temp_ix2.compute_at(ix2, xo)
        temp_iy2.compute_at(iy2, xo)
        temp_ixiy.compute_at(ixiy, xo)

        # clamped_lumi.compute_at(locMax, xo)
        # finalBlur.compute_at(locMax, xo)
        # temp_ix2.compute_at(locMax, xo)
        # temp_iy2.compute_at(locMax, xo)
        # temp_ixiy.compute_at(locMax, xo)

        clamped_lumi.compute_root()
        # finalBlur.compute_at(locMax, xo)
        
        locMax.tile(x,y,xo,yo,xi,yi,128,64)
        locMax.parallel(yo)
        M.compute_at(locMax, xo)
        
       
        #gKern.compute_at(locMax, xo)
        gKern.compute_root()
        
time: 2.5s /mpx
