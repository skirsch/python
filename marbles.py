# code by mike deskevich
# 15 draws where you get at least 3 reds and no greens
import numpy as np

#create the marbles
green=1875
red=31
blue=5595
total=green+red+blue

#fraction that are green
green_test=green/total 

#fraction that are green or red
red_test=(green+red)/total

#how many trials to do
trials=10000000

#how many draws per trial
draws=15 

#get some random numbers for the trials
sample=np.random.random((draws,trials)) 

#if the random number is less than green_test, then we know it's green
green_ct=np.sum(sample<green_test,axis=0) 

#if the random number is less than red_test, then it's either green or red
#so we subtract off the green ones from above and are left with only red
red_ct=np.sum(sample<red_test,axis=0)-green_ct 

#everything else is blue, but we're not using it, so let's not caluclate it now
#blue_ct=draws-green_ct-red_ct

#sum up how many times we had both no greens and at least three reds
test=np.sum((green_ct==0)*(red_ct>=3))
print(test,test/trials)
