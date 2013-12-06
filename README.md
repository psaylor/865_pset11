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