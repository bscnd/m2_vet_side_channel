import numpy as np

wordbits = [] 

#Allow to compute weight of any integer iff x <= 16 bits
#Hamming weight of every 16 bits
#Lookup table of hamming function of every 8 bits
def bitcount_16(x): #np.uint16 ?
    return wordbits[x & 0xFF] + wordbits[x >> 8]

#Init lookup table
def lookuptable_init():
    for i in range(256): # all 8 bits numbers in Lookup table
        x=i
        count=0
        while(x):
            x &= x-1
            count += 1
        wordbits.append(count)

#Use direct weight calculations to find hamming dist
#Easiest method
def hamming_dist(x1, x2):
    return bitcount_16(x1) - bitcount_16(x2)

#Use precomputed hamming lookup table to find hamming dist
#Fastest method
def hamming_dist_lookuptable(x1, x2):
    return wordbits[x1] - wordbits[x2]

lookuptable_init()
print("Generated Lookup Table :",wordbits)

x1 = int(input("Give me number 1 :"))
x2 = int(input("Give me number 2 :"))

print(abs(hamming_dist(x1, x2)))
print(abs(hamming_dist_lookuptable(x1, x2)))
