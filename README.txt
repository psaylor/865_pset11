Name: Patricia Saylor
MIT Email: psaylor@mit.edu

Q1:How long did the assignment take?:
{A1: your answer}

Q2:Potential issues with your solution and explanation of partial completion (for partial credit):
{A2: your answer}

Q3:Anything extra you may have implemented:
{A3: your answer}

Q4:Collaboration acknowledgement (but again, you must write your own code):
{A4: Marcel Polanco }

Q5:What was most unclear/difficult?:
{A5: your answer}

Q6:What was most exciting?:
{A6: your answer}

Q7: How long did it take for the 2 schedules for the smooth gradient? 
{A7: The default schedule took 0.0340030193329 seconds, and the final schedule took 0.0636739730835 seconds. Instead of a speedup, I observed a slow-down of about 2x.}

Q8: Speed in ms per megapixel for the 4 schedules (1 per line)
{A8: 
Schedule 1: 0.238843870163
Schedule 2: 0.141817712784
Schedule 3: 0.177475786209
Schedule 4: 0.104720830917
}

Q9: What machine did you use (CPU type, speed, number of cores, memory)
{A9: your answer}

Q10: Speed for the box schedules, and best tile size
{A10: your answer}

Q11: How fast did Fredo’s Harris and your two schedules were on your machine?
{A11: your answer }

Q12: Describe your auto tuner in one paragraph
{A12: your answer }

Q13: What is the best schedule you found for Harris. 
{A13: your answer}


compute-root 
Harrris took:  1052.92845607  seconds
29449.81342 ms per megapixel (1052928.4560680 ms for 35 megapixels)

Athena results for tutorial 10:
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

