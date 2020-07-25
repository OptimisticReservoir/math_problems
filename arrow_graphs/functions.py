# Python module for my Project Euler functions

def max_product_2d_search(list_2d,size=4,dir=[(0,1),(1,0),(1,1),(1,-1)]):
    """
    Scans a 2D list and tests products to find the maximum.

    list_2d -- list of integer lists: [[int,int,int][int,int,int][...]]
    size -- how many adjacent numbers to use.
    dir -- directions to search. [(x,y),(x,y),(...)]
    """
def make_2d_array(str_list):
    """ Converts a list of strings containing ints into a 2d array."""
    int_2d_array = []
    row = 0
    for s in str_list:
        int_2d_array.append(str_list_to_int(s.split(" ")))
    return int_2d_array
def i_digits(x):
    """ Finds digits in the integer part of the number. """
    extra = 0
    if x < 0:
        x = abs(x)
        extra = 1
    d = 1
    while(x > 10**d):
        d +=1
    return d + extra
def str_list_to_int(str_list):
    """ Converts list of strings to list of ints. """
    int_list = []
    for s in str_list:
        int_list.append(cast_number(s))
    return int_list
def trim_empties(list):
    """ Removes empty ('') values from the list. """
    try:
        while(1):
            list.remove("")
    except ValueError:
        return list
def print_2d(list_2d, filler_char="0"):
    """ Prints the 2d array of integers nicely formatted. """
    # get row with largest value, then get largestvalue
    maximum = max(max(list_2d))
    digits = i_digits(maximum)
    #print(f"Max: {maximum} and digits: {digits}")
    output = ""
    x_sign = 0
    for row in list_2d:
        for x in row:
            d = digits - 1
            x_sign = -1 if x < 0 else 0
            x = abs(x) # so we can compare to 10**d
            d += x_sign # 1 less digit for the negative sign.
            if x_sign:
                output += "-"
            while(x < 10**d and d>0):
                output += filler_char
                d -= 1
            output += str(x)
            output += " "
        output += "\n"
    print(output[:-1])
def print_pythagorean_triple(p_triple,index):
    """ Prints out a Pythagorean triple and checks vs an index. """
    print(f"A pythagorean triple for index of {index} is:")
    print(f"a: {p_triple[0]}"
      + f" b: {p_triple[1]}"
      + f" c: {p_triple[2]}")
    print(f"The sum is {sum(p_triple)}"
      + f" which is {'valid' if index==sum(p_triple) else 'not valid'}")
    print(f"The product is {list_product(p_triple)}")
def find_pythagorean_triple(i=1000):
    """
    Finds Pythagorean triples with a given index

    i = index, or sum of a, b, and c (integer)

    Currently it is only set up to find a single triple per index.
    If more are needed, just append them to a list instead.

    It uses formulas from p09.py:
    let x = avg(a,b)
    let y be an offset from x.
    (x-y)**2 + (x+y)**2 = c**2
    Solving for y gives:
    y**2 = ((c**2 - 2*x**2)/2)
    """
    pythagoreanTriple = [0,0,0]
    for c in range(int(i/2 - 0.5*i**0.5 + 1),int(i*(2**0.5-1)),-1):
        # Starting range logic:
        # c is at most index/2
        # but that would mean a = 0, b = c. trivial.
        # We want a < b < c and all integers.
        # If b is super large, it could be almost as big as c,
        # however, a can't be too tiny because it needs to be
        # able to help b**2 become c**2.
        # The smallest a that could do that is (2b)**0.5
        # So b and c will split the loss of (2b)**0.5
        # b is trying to be i/2, so the total loss is i**0.5.
        # Split each way that is 0.5*i**0.5
        # c must be bigger than b, hence the +1.
        #
        # If a=b, then c is a minimum.
        # x**2 + x**2 = c**2
        # solving for c with a+b+c=i gives:
        # c = (2**0.5 - 1)*i
        #
        # With these two range restrictions, the search is much smaller
        # from a max of ~50% of i, to a low of ~41.4% of i.
        # instead of searching all of i, only about 8.5% is searched.
        x = (i - c)/2
        y2 = ((c**2 - 2*x**2)/2)
        if y2 < 0:
            #can't square root a negative number here.
            continue
        y = y2**0.5
        #print(f"y={y} c={c} x={x} i-c%2/2={((i-c)%2)/2}")
        if y%1 == ((i-c)%2)/2:
            # y = integer if i-c is even, or int + 0.5 if odd.
            pythagoreanTriple = [int(x-y), int(x+y), int(c)]
            break
    return pythagoreanTriple
def max_product_slice(list,size):
    """
    Finds largest product of all slices of the list.

    list -- list of digits (string or list)
    size -- size of slice to take (integer)

    """
    max = 0;
    product = 0;
    for x in range(len(list)-size+1): # size is inclusive, so we need +1
        product = list_product(list[x:x+size])
        if product > max: max = product
    return max
def list_product(list):
    """ Calculates numbers list product. """
    val = 1
    for x in list:
        val *= int(x)
    return val
def ordinal(i):
    """ Returns the ordinal ending, e.g. 'st' for 1"""
    ending = { 1:"st",
               2:"nd",
               3:"rd"}
    if cast_number(i):
        i = int(float(i))
        if i%100>3 and i%100<14:
            return "th"
        return ending.get(i%10,"th")
    else:
        return ""
def sum_square_difference(num_list):
    """
    Sum square difference of a list

    Calculates the difference between the square of the sum and
    the sum of the squares.
    e.g. (a+b+c)**2 - (a**2 + b**2 + c**2)
    """
    square_sum_all = sum(num_list)**2
    sum_squares = 0
    for x in num_list:
        sum_squares += x**2
    return square_sum_all - sum_squares
def lcm(num_list):
    """
    Find lowest common multiple of number list

    num_list - list of integers to use

    Will factor each number in the list,
    then find LCM using dictionary_product.
    """
    primeList = generate_primes(max(num_list))
    # Initialize the factor dictionary to 0:
    primeDict = dict.fromkeys(primeList,0)
    for x in num_list: # will stop at maxNum
        primeDict = prime_list_factor(x,primeDict)
        #print(primeDict)
    return dictionary_product(primeDict)
def dictionary_product(numDict):
    """
    Find the product of dictionary: key**value

    numDict -- dictionary: {int: int, int: int ...}

    Calculates the product of all keys multiplied together.
    Each key counts value times.
    So, key1**value1 * key2**value2 * etc.
    """
    product = 1
    for x in numDict:
        product *= x ** numDict[x]
    return product
def prime_list_factor(num, prime_dict_original):
    """
    Factors given number using prime dictionary

    num -- number to factor (integer)
    prime_dict_original -- dictionary of prime numbers as keys.
                         The values are how many of each prime.
                         This allows comparison across mulitple runs.

    The dictionary is used because it keeps track of the factors.
    This implementation is used for function Lowest Common Multiple.
    To factor just a single number, send values as 0s.
    If num can already be made by the existing prime_dict values,
    then no changes are made.
    """
    q = num # q for quotient
    prime_dict = prime_dict_original
    # prime_dict = prime_dict_original.copy() #uncomment to preserve original
    for x in prime_dict:
        i = 0
        while q % x == 0:
            q /= x
            i += 1
        if i > prime_dict[x]:
            prime_dict[x] = i
    if q != 1:
        prime_dict[q] = 1 # add the remaining quotient to the end
                          # this is like a remainder in the event
                          # primeList was incomplete
    return prime_dict
def find_max_palindrome(digits):
    from classes import ProductPalindrome
    """
    Finds largest product that is a palindrome

    digits - max digits allowed in each factor (integer)
    Uses the idea of indecies to search for the largest
    palindrome first. It stops after the first one found.
    Not guaranteed to be the largest, but likely to be.
    """
    # TODO: Write a function to find all palindromes.
    digits = int(cast_number(digits))
    if not digits:
        digits = 3 # use 3 as default if invalid digit given.
    maxNum = int("9"*digits) # all 9s is max value
    maxIndex = 2 * maxNum # index = sum of the two numbers to be multipled.
    i = maxIndex
    x = maxNum
    y = maxNum
    solved = False
    # I'm postulating that this will find the maximum palindrome first
    # if not, I'll need to add all palindromes found to a list and then
    # find max later.
    # There could exist a situation where a particular index will give
    # two palindromes.
    # There could also exist a situation where a lower index would give
    # a larger palindrome.
    # TODO: add a more rigorous search.
    while(i > 0):
        x = maxNum
        y = i - x
        # x + y = i
        while(y <= maxNum):
            if is_palindrome(x*y):
                solved = True
                break
            x -= 1
            y += 1
        if solved:
            break
        i -= 1
    return ProductPalindrome(x,y)
def is_palindrome(s):
    """ Checks to see if passed string/number is a palindrome """
    s = str(s)
    # Old method - more memory efficient?
    #i = 0
    #while(i < len(s)/2):
    #    if s[i] != s[-(i+1)]: # 0 is first, -1 is last.
    #        return False
    #    i += 1
    #return True
    return s == s[::-1]
def generate_n_primes(nthPrime):
    """
    Generates a list of n primes

    nthPrime -- How many primes to getnerate (integer)
    returns the list of n primes
    """
    nthPrime = int(nthPrime)
    primeList = []
    primeCandidate = 0
    if 1 <= nthPrime:
        primeList.append(2)
    else:
        return primeList
    if 2 <= nthPrime:
        primeList.append(3)
    else:
        return primeList

    while(len(primeList)<nthPrime):
        primeCandidate += 6
        if check_prime(primeCandidate-1,primeList):
            primeList.append(primeCandidate-1)
        if check_prime(primeCandidate+1,primeList):
            primeList.append(primeCandidate+1)

    # might have generated 1 extra prime above nthPrime
    if len(primeList) > nthPrime:
        primeList.pop(-1)
    return primeList
def generate_primes(max_prime):
    """
    Generates a list of primes up to a maximum value

    maxPrime -- Largest acceptable value (integer)
    returns the list of primes < maxPrime
    """
    max_prime = int(max_prime)
    primeList = []
    primeCandidate = 0
    if 2 <= max_prime:
        primeList.append(2)
    else:
        return primeList
    if 3 <= max_prime:
        primeList.append(3)
    else:
        return primeList
    while(primeList[-1] < max_prime and primeCandidate+5 <= max_prime):
        # +5 because we are going to add 6 then subtract 1.
        primeCandidate += 6
        if check_prime(primeCandidate-1,primeList):
            primeList.append(primeCandidate-1)
        if check_prime(primeCandidate+1,primeList):
            primeList.append(primeCandidate+1)
    # might have generated 1 extra prime above max_prime
    if primeList[-1] > max_prime:
        primeList.pop(-1)
    return primeList
def check_prime(num, primes=None):
    """
    Checks number to see if it is prime

    num -- number to check (integer)
    primes -- (option) list of prime numbers ([integer])

    Accepts a number and an optional list of primes
    checks to see if number is divisible by a prime
    This will generate it's own pseudo-prime list if none provided.
    returns True if indivisible by Primes
    returns False if divisibile.
    """
    num = int(num)
    sqrtNum = int(num ** 0.5)
    if(primes is not None):
        for x in primes:
            if x > sqrtNum:
                break;
            if num % x == 0:
                return False
    else: # make our own list
        if num % 2 == 0:
            return False
        if num % 3 == 0:
            return False
        for x in {*range(6,sqrtNum+1,6)}:
            # primes besides 2 and 3 are 1 above or below multiples of 6
            # these aren't all primes, but close enough.
            if num % (x-1) == 0:
                return False
            if num % (x+1) == 0:
                return False
    return True
def largest_prime_factor(num):
    """
    Gets largest prime factor

    num -- number to factor (integer)
    """
    num = int(num)
    sqrtNum = int(num ** 0.5)
    primes = generate_primes(sqrtNum)
    largest = -1
    for x in primes:
        if num % x == 0 and x > largest:
            largest = x
    return largest
def test_args(args):
    """ Tests an argument list and prints results. """
    print(str(len(args)) + " arguments.")
    i = 0
    x = 0
    output = 0
    while(i < len(args)):
        x = cast_number(args[i])
        output = str(x if is_floatstring(args[i]) else args[i])
        output += " " + str(type(x if is_floatstring(args[i]) else args[i]))
        print(output)
        i += 1
def lookup_best_byte_size(mod):
    # XXX: The XXX tag means that byte_size is only so-so
    # It will probably need a bigger one.
    # I checked up to 128 and I couldn't find a better option.
    lookup_table = {
11:60,14:62,18:61,22:59,23:55,25:60,28:61,31:60,33:60,
36:61,38:61,41:60,42:61,44:59,46:62,47:46,50:61,52:62, # XXX:
53:52,54:61,55:60,58:60, # XXX:
59:58,61:50,62:62,66:59,67:33,69:55,70:62, # XXX:
71:35,72:62, # XXX:
74:57, # XXX:
75:60,76:61,77:60,78:62, # XXX:
79:39,81:54,82:61, # XXX:
83:41,84:61,86:58,89:55,90:62, # XXX:
92:58,93:60,94:49,97:60,98:50,99:60,101:50,103:51,104:62, # XXX:
106:58 # XXX:
    }
    return lookup_table.get(mod,63)
def print_best_byte_sizes(width):
        from functions import best_byte_size
        results = {}
        bbs = []
        for x in range(2,width+1):
            bbs = best_byte_size(x)
            results[x] = max(i for i in bbs if i<64 or len(bbs)<4)
            #results[x] = min(i for i in bbs if (i<128 and i>20) or len(bbs)<4)
            #print(f"{x}: size:{bbs}")
        for x in results:
            if 256**results[x]%x > 16:
                print(f"{x:3}: {results[x]:3} --- {256**results[x]%x}")
def best_byte_size(mod):
    min_mod = float("inf") # set to infinitely large
    best = []
    MIN_READ = 4
    MAX_READ = 128 # max bytes to read at once.
    BYTE_VALUE = 256 # bytes are base 256
    for x in range(MIN_READ,MAX_READ+1):
        n = BYTE_VALUE**x % mod
        if n < min_mod:
            min_mod = n
            best = [x]
        elif n == min_mod:
            best.append(x)
    return best
def bytes_to_int(byte_arr):
    BYTE_VALUE = 256 # bytes are base 256
    s = 0 #sum
    for i,n in enumerate(byte_arr):
        s += n * BYTE_VALUE**i
    return s
def cast_number(n):
    """ Casts given string as a number - int or float as required. """
    if type(n) == type(""):
        if is_intstring(n): # "5.4" gives False
            return int(n)
        elif is_floatstring(n):
            return float(n)
    elif type(n) == type(5.0) or type(n) == type(5):
        return n # no casting needed
    return None
def get_boolstring(s):
    """ Attempts to cast input to boolean. Return None if failed. """
    if type(s) == type(True):
        # s is already bool
        return s
    elif type(s) == type("string"):
        # s is string
        s = s.lower()
        if s[0:4] == "true":
            return True
        elif s[0:5] == "false":
            return False
        else:
            return None
    elif type(s) == type(0) or type(s) == type(0.0):
        # s is number
        if s:
            return True
        else:
            return False
    else:
        # s isn't simple:
        return None
def is_boolstring(s):
    """ Tests if input is a boolean. """
    if type(s) == type(True):
        # s is already bool
        return True
    elif type(s) == type("string"):
        # s is string
        s = s.lower()
        if s[0:4] == "true":
            return True
        elif s[0:5] == "false":
            return True
        else:
            return False
    elif type(s) == type(0) or type(s) == type(0.0):
        # s is number
        return True
    else:
        # s isn't simple:
        return False
def is_floatstring(s):
    """ Tests if string is a float. """
    try:
        float(s)
        return True
    except ValueError:
        return False
def is_intstring(s):
    """ Tests if string is an int. """
    try:
        int(s) # exception for float strings.
        return True
    except ValueError:
        return False
