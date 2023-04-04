import random

def prime_test(N, k):
	# This is main function, that is connected to the Test button. You don't need to touch it.
	return fermat(N,k), miller_rabin(N,k)


def mod_exp(x, y, N):
    """
    Calculates the expression x^y (mod N) using recursion
    
    Overall time complexity: O(n^3)
    Overall space complexity: O(n^2)
    """
    if y == 0: # If we've reached the base case, return 1
        return 1
    z = mod_exp(x, y // 2, N) # Recurse O(n) times
    if y % 2 == 0:
        return (z**2) % N # Multiplication of n-bit numbers is O(n^2)
    else:
        return (x * z**2) % N # Multiplication of n-bit numbers is O(n^2)
	

def fprobability(k):
    """
    Calculates the probability that an integer is prime given that it passed the Fermat
    test k times.

    Overall time complexity: O(1)
    Overall space complexity: O(1)
    (since both are with respect to n = logN, and k << n)
    """
    return 1 - .5**k


def mprobability(k):
    """
    Calculates the probability that an integer is prime given that it passed the Miller-Rabin
    test k times.

    Overall time complexity: O(1)
    Overall space complexity: O(1)
    (since both are with respect to n = logN, and k << n)
    """
    return 1 - .25**k


def fermat(N,k):
    """
    Applies Fermat's little theorem k times to test whether a given integer N is prime.

    Overall time complexity: O(n^3)
    Overall space complexity: O(n^2)
    """
    for _ in range(k): # Run the test k times
        a = random.randint(1, N - 1) # We take this to be an O(1) operation
        if mod_exp(a, N - 1, N) != 1: # If a^(N - 1) % N is not 1, we know N is composite
            return 'composite'
    return 'prime' # If it never failed for k iterations, we believe it to be prime


def miller_rabin(N,k):
    """
    Applies the Miller-Rabin test k times to determine whether a given integer N is prime.

    Overall time complexity: O(n^4)
    Overall space complexity: O(n^2)
    """
    for _ in range(k): # Run the test k times
        a = random.randint(1, N - 1) # We take this to be an O(1) operation
        if mod_exp(a, N - 1, N) != 1: # Briefly apply the Fermat test; O(n^3)
            return 'composite'
        e = N - 1
        while(e % 2 == 0): # End once we get to an odd exponent: O(n)
            e //= 2 # Since e is even, it doesn't matter if we use /= or //= . This is O(n)
            x = mod_exp(a, e, N) # Time complexity of mod_exp is O(n^3)
            if x == N - 1: # This is what we should expect for primes
                break
            elif x != 1: # This guarantees that N is composite
                return 'composite'
    return 'prime' # If it never failed for k iterations, we believe it to be prime
