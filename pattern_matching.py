import math
from cmath import log
import random

alphabet= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'   

def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

# --------------------------------------------------------------------------------------------------------------------------------
# This function returns the value of N. The expression of the value of N is derived as follows:
# According to the given conditions : If x[i..(i + m − 1)] ̸= p, then Pr[i ∈ L] ≤ ε
# Consider x[i..(i + m − 1)] ̸= p , but f(x[i..(i + m − 1)]) mod q = f(p) mod q = r ;resulting in false positive.
# From above , f(x[i..(i + m − 1)]) = kq + r and f(p) = lq + r
# Taking difference we get, d = (f(x[i..(i + m − 1)]) - f(p)) = (k-l)q i.e. (f(x[i..(i + m − 1)]) - f(p)) mod q = 0
# Therefore q is a prime factor of d.
# Furthermore since d is positve integer it can be expressed as product of primes i.e. d = p1*p2*p3.....pk
# Since smallest prime is 2, we can say that d>=2^k----------------------------------(1)
# In our case, the maximum value d can take, for a pattern of length m is when one of string contains all As and the other contains all Zs.
# This gives, d<= f(string of length m with all Zs) - f(string of length m with all As)
        #  i.e. d<= 25*(26^(m-1) + 26^(m-2) + 26^(m-3)......... + 1) - 0
        #  i.e. d<= (26^m - 1) ------------------------------------------------------(2)
# From (1) and (2) we get,  2^k<=d<= (26^m - 1)
# Taking log with base 2 on both sides,  k <= mlog(26) ------------------------------(3)
# From (3), d can have atmost mlog(26) prime factors.
# Since the occurence of a false positive happens only when the chosen prime is prime factor of d, we want the probability 
# that a randomly chosen prime p in the range {1,2,.....,N} should be atmost ε. This can be mathematically written as :
#              mlog(26)/ No. of primes in {1,2,3......,N}   <= ε
#        i.e. (m/ε)log(26) <= No. of primes in {1,2,3,.......N}
# So, N should be chosen such that there are atleast (m/ε)log(26) primes in the range {1,2,3,.......N}.
# From a previously proved corollary, if we want k primes between 1 and n , then n>=2klog(k) (where base of log is 2) 
# Applying this we get, N>= 2(m/ε)log(26)log((m/ε)log(26))    where the  base of the log is 2.           
# Hence the value of N>=2(m/ε)log(26)log((m/ε)log(26)) i.e. the minimum value of N can have is N=2(m/ε)log(26)log((m/ε)log(26))
# which is returned by the function findN.
  
def findN(eps,m):
    return 2*(m/eps)*(log(26,2))*(log(((m/eps)*log(26,2)),2))
# -------------------------------------------------------------------------------------------------------------------------------

def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# --------------------------------------------------------------------------------------------------------------------------------
# This function returns the index of question mark in the pattern. If question mark is not present, it returns (-1).
def find_q(s):
    if '?' in s:
        return s.index('?')
    return -1
# --------------------------------------------------------------------------------------------------------------------------------

# This function calculates the hash value of the pattern and substrings to be matched. 
# It takes 3 arguments a string whose hash is to be calculated, a prime q and 'b' which is the index of '?' in the pattern.
# The alphabets are mapped to the set {0,1,2,......25} using the string 'alphabet' declared above such that A->0, B->1.....Z->25.
# Function calculates the value of summation(26^(n-i-1)*y[i]) where i is index of the pattern, n is length of the pattern and 
# y[i] is the number to which the letter at index i in the pattern is mapped. This summation is calculated using the method of polynomial
# accumulation. Finally the function returns the value of summation % q.
# If the pattern doesn't contain '?' , all the values of i are considered, else the value of the letter in the substring of text at index equal
# to the index of '?' in pattern is skipped.

# Time Complexity : It takes O(m) time to traverse the string and log(q,2) time for mod operation.
# Therefore, overall time complexity is mlog(q) where m is length of string , q is prime number and base of log is 2.

def find_hash(string,q,b):
    val=0
    for i in range(len(string)) :
            if b==-1:
                val= val * 26 + (alphabet.index(string[i])) 
            else:
                if i!=b:
                    val= val * 26 + (alphabet.index(string[i])) 
                else:
                    val = val*26
    return val%q
# -----------------------------------------------------------------------------------------------------------------------------------

# This function returns a list of indices at which the pattern matches with the text. It first calculates the hash the value of the 
# given pattern- p1, hash value of first substring of length equal to the length of pattern - p3 and hash value of last substring 
# having length equal to length of pattern - p4.
# While traversing along the text, the hash values are not calculated from the beginning for every substring, instead the hash value
# of the next substring is deduced form the hash value of previous substring using the ralation as follows:
# initial substring = s, next substring = s', value of leftmost letter in s = s_left_val, value of rightmost letter in s' = s'_right_val 
# We can write,  s' = s - s_left + s'_left
#                val(s') = val(s - s_left_val*(26)^(n-1))*26 + s'_right_val
# Using this we get, hash(s') = (26*hash(s) - s_left_val*(hash(26^(n)) + s'_right_val) mod q
# If hash(s') = hash(pattern), its value is appended in l.
# Finally, l is returned.

# Space Complexity:
# Output list l = k
# p1,p2,p3,p4 = log(q)
# i = log(n)
# Therefore Overall Space Complexity : O(k + log(n) + log(q))

# Time Complexity: 
# It takes (mlog(q,2)) for the hash function to calculate and nlog(q,2) time for traversing along text and operations involving it.
# Therefore overall time complexity is O((m+n)log(q,2))

def modPatternMatch(q,p,x):
    l=[]
    p1 = find_hash(p,q,find_q(p))
    p2 = (26**(len(p)))%q
    p3 = find_hash(x[0:len(p)],q,find_q(p))
    p4 = find_hash(x[len(x)-len(p):],q,find_q(p))
    if p3 == p1:
        l.append(0)
    j = 0
    while j<(len(x)-len(p)):
        p3 = (26*p3 - (alphabet.index(x[j]))*p2 + (alphabet.index(x[j+len(p)])))%q
        if p3 == p1:
            l.append(j+1)            
        j = j +1
    
    if p4 == p1 and (len(x) - len(p)) not in l:
        l.append(len(x)-len(p))
    return l
# ---------------------------------------------------------------------------------------------------------------------------------

def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

# -----------------------------------------------------------------------------------------------------------------------------------
# This function returns list of indices at which the text matches the pattern, when the pattern has a wildcard. It works similar to
# modPatternMatch except while dealing with index of substring where the '?' occurs. While traversing the text, let j be the index of 
# '?' in the initial substring, therefore the next substring will have '?' at index j+1, so while calculating the value of hash of 
# next substring, it subtracts the value of letter at index j+1 (wrt initial substring) and adds the value of letter at index j (wrt initial substring).

# Time and Space Complexity same as modPatternMatch(q,p,x)

def modPatternMatchWildcard(q,p,x):
    l=[]
    p1 = find_hash(p,q,find_q(p))
    p2 = (26**(len(p)))%q
    p3 = find_hash(x[0:len(p)],q,find_q(p))
    p4 = find_hash(x[len(x)-len(p):],q,find_q(p))
    p5 = 26**(len(p)-find_q(p)-1)%q
    p6 = 26**(len(p)-find_q(p))%q
    if p3 == p1:
        l.append(0)
    j = 0
    while j<(len(x)-len(p)):
        p3 = (26*p3 - (alphabet.index(x[j]))*p2 + (alphabet.index(x[j+len(p)])) - (alphabet.index(x[j+ find_q(p)+1]))*p5 + (alphabet.index(x[j+find_q(p)]))*p6 )%q
        if p3 == p1:
            l.append(j+1)
        j = j +1
    
    if p4 == p1 and (len(x) - len(p)) not in l:
        l.append(len(x)-len(p))
    return l   


#------------------------------------------------------------------------------------------------------------------------------------ 

def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# ----------------------------------------------------------------------------------------------------------------------------------
# print(modPatternMatchWildcard(1000000007,'?A','ABCDE'))
# print(modPatternMatch(1000000007, 'AA', 'AAAAA'))
# print(modPatternMatchWildcard(1000000007, 'D?', 'ABCDE'))
# print(modPatternMatch(2, 'AA', 'ACEGI'))
# # print(hash('ABCDE',10000))
# print(modPatternMatchWildcard(19,'JA?S','AMADBOXERSHOTQUICKGLOVEDJABSTOTHEJAWSOFHISDIZZYOPPONENTATTHEJAMSROCKSHUFFLE'))

