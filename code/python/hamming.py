import numpy as np

wordbits = []

#Equivalent for population count (number of bits set to 1) --> hamming weight
#work for all binary length up to 64 bits
def popcount_8(x):
    #put count of each 2 bits into those 2 bits
    x -= (x >> 1) & 0x5555555555555555 #binary: 0101...
    
    #put count of each 4 bits into those 4 bits              
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333) #binary: 00110011..
    
    #put count of each 8 bits into those 8 bits 
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f #binary:  4 zeros,  4 ones ...
    
    #left 8 bits of x + (x<<8) + (x<<16) + (x<<24) + ... 
    x = (x * 0x0101010101010101) >> 56 #the sum of 256 to the power of 0,1,2,3...       
    
    return x & 0xff;  #returns result with 8 bit masking

#Allow to compute Hamming weight of any integer iff x <= 8 bits
#with the Lookup table of the hamming function
def bitcount_8(x):
    return wordbits[x & 0xFF] #+ wordbits[x >> 8]

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
def hamming_dist_bitcount_8(x1, x2):
    #number of different bit of x1 xor x2
    return bitcount_8(x1^x2)

def hamming_dist_popcount_8(x1, x2):
    return popcount_8(x1^x2)

lookuptable_init()
#print("Generated Lookup Table :",wordbits)

x1 = int(input("Give me number 1 :"))
x2 = int(input("Give me number 2 :"))

print("bitcount_8 hamming weight of x1:",bitcount_8(x1))
print("bitcount_8 hamming weight of x2:",bitcount_8(x2),"\n")
print("popcount_8 hamming weight of x1:",popcount_8(x1))
print("popcount_8 hamming weight of x2:",popcount_8(x2),"\n")

print("bitcount_8 hamming distance :", abs(hamming_dist_bitcount_8(x1, x2)))
print("popcount_8 hamming distance :", abs(hamming_dist_popcount_8(x1, x2)))
