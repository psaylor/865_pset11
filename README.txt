Name: Patricia Saylor
MIT Email: psaylor@mit.edu

Q1:How long did the assignment take?:
{A1: Too long. 20+ hours.}

Q2:Potential issues with your solution and explanation of partial completion (for partial credit):
{A2: None that I know of. }

Q3:Anything extra you may have implemented:
{A3: Nope}

Q4:Collaboration acknowledgement (but again, you must write your own code):
{A4: Marcel Polanco, Divya Bajekal }

Q5:What was most unclear/difficult?:
{A5: There are so many possible schedules, it was hard to think of the best way to reorganize the scheduling to optimize it.}

Q6:What was most exciting?:
{A6: The first time I got a major speedup in Harris by writing a smarter schedule. }

Q7: How long did it take for the 2 schedules for the smooth gradient? 
{A7: The default schedule took 1.38568711281 seconds, and the final schedule took 0.0415740013123 seconds, giving an acceleration factor of 33.}
 
Q8: Speeds are averages in ms per megapixel for the 4 schedules (1 per line)
{A8: 
Schedule 1: 7.37683
Schedule 2: 5.13037 (speedup: 1.45)
Schedule 3: 6.34286 (speedup: 1.14)
Schedule 4: 3.01079 (speedup: 2.64)
}

Q9: What machine did you use (CPU type, speed, number of cores, memory)
{A9: I used the same athena machine for all the timings.
Release 12.04 64-bit Linux
Memory: 3.6 GiB
Processor: Intel Core 2 Duo CPU E8400 @ 3.00GHz × 2 }

Q10: Speed for the box schedules, and best tile size
{A10: 
default schedule
           took  4.85651779175 seconds
root first stage
           took  3.49677319527 seconds
tile  256 x 256  + interleave
           took  1.36110138893 seconds
tile  256 x 256 + parallel
           took  0.766900634766 seconds
tile  256 x 256  + parallel+vector without interleaving
           took  0.883076810837 seconds
tile  64 x 128 + parallel
           took  0.725087404251 seconds
tile  128 x 128 + parallel
           took  0.715808820724 seconds
tile  256 x 128 + parallel
           took  0.711972618103 seconds
tile  512 x 128 + parallel
           took  0.738884019852 seconds
tile  1024 x 128 + parallel
           took  0.795348167419 second
The best tile size was 256 x 128           
}

Q11: How fast did Fredo’s Harris and your two schedules were on your machine?
{A11: 
Fredo's Harris: took  169.827005863 seconds
4749.96531 ms per megapixel (169827.0058632 ms for 35 megapixels)

Root Schedule:
Harrris took:  75.1292579174  seconds
2101.32285 ms per megapixel (75129.2579174 ms for 35 megapixels)

Faster Schedule:
Harrris took:  45.9269530773  seconds
1284.55090 ms per megapixel (45926.9530773 ms for 35 megapixels)
}

Q12: Describe your auto tuner in one paragraph
{A12: The autotuner tries many tile size configurations for 3 different schedules (which are built in to the autotuner) : Schedules 1 and 2 were pretty good and had beaten the python code, and Schedule 3 was less good for the tile sizes I had tried but seemed like a reasonable attempt at localizing computations. For each of these three schedules, the autotuner loops over the various combinations of tile dimensions for that schedule (x and y dimensions are varied for a given tile), calls harris_algorithm (a helper method I wrote that abstracts the algorithm from the schedule and returns a tuple of all the funcs in the algorithm), and sets the schedule using the varied tile dimensions. The first schedule was the most straightforward since there was only one tile. The second schedule (and third schedule, too) has 5 tiles (4 for blurs and 1 for locMax), but the computational complexity of optimizing this schedule is reduced by giving all 4 of the blurs the same tile dimensions; this seemed reasonable since 3 of the blurs which have large sigmas are symmetric in their span, and the other blur has a pretty small span so it should not incur much redundancy and might not need to have its tile size optimized separately. The computational complexity of the autotuner is such that I could not run the whole thing before this pset was due, since it would need to run for a day or two (at least with this size image on this athena machine); for this reason the autotuner also does not compute averages, though it would be easy to add it would take even longer to finish running. }

Q13: What is the best schedule you found for Harris. 
{A13: The best schedule I found for harris tiles locMax into 128*256 tiles and computes all producers of non-local consumers at xo inside of the locMax tiling loops. The exact schedule can be seen as schedule 1 in the autotuner.
Tuning Schedule 1 | y_tile_size= 128 , x_tile_size= 256
best:  42.3012759686
1183.14277 ms per megapixel (42301.2759686 ms for 35 megapixels)}


compute-root 
Harrris took:  1052.92845607  seconds
29449.81342 ms per megapixel (1052928.4560680 ms for 35 megapixels)



