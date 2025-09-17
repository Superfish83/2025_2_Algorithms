from random import choice

def makeInt(digits): # takes a list of digits (as returned by getDigits) and returns the integer they represent
    return sum( [ 10**(len(digits)-i-1)*digits[i] for i in range(len(digits))])

def generate_testcases(n):
    lst1 = [ choice(range(10)) for i in range(n) ] # generate a random list of length n
    lst2 = [ choice(range(10)) for i in range(n) ] # generate another random list of length n

    a = makeInt(lst1)
    b = makeInt(lst2)

    return (a, b, a*b)

if __name__ == "__main__":
    test_n = range(25, 501, 25)
    for n in test_n:
        a, b, c = generate_testcases(n)

        with open(f"tests/input/N_{n}.txt", "x") as f:
            f.write(f"{a}\n{b}")

        with open(f"tests/output/N_{n}.txt", "x") as f:
            f.write(f"{c}")