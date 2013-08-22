   
# Misc functions

def CountCombinations(n, m=1):
    """Number of ways to partition a number e.g 1+1+1, 2+1"""
    ans = 1
    if n <= 1:
        return 1
    for i in xrange(m, int(ceil(n/2.))):
       ans += comb(n-i, i)
    return ans

def prime(n):
    return n>1 and not any(map(lambda x: n % x == 0, xrange(n/2+1)))
    
def fact(n):
    return reduce(op.mul, xrange(2,n+1)) if n > 1 else 1
    
def hcf(a, b):
    return hcf(b, a % b) if a % b else b

def lcm(a, b):
    return a * b / hcf(a, b)

def fact(n):
    return reduce(op.mul, xrange(2,n+1)) if n > 1 else 1

# Triangle number
Tn = lambda n:n*(n+1)/2

# Pentagonal number
Pn = lambda n:n*(3*n-1)/2

# Hexagonal number
Hn = lambda n:n*(2*n-1)
