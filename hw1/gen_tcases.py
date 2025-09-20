from random import choice

def makeInt(digits): # takes a list of digits (as returned by getDigits) and returns the integer they represent
    return sum( [ 10**(len(digits)-i-1)*digits[i] for i in range(len(digits))])

def gen_tcase(n):
    lst1 = [ choice(range(10)) for i in range(n) ] # generate a random list of length n
    lst2 = [ choice(range(10)) for i in range(n) ] # generate another random list of length n

    a = makeInt(lst1)
    b = makeInt(lst2)

    return (a, b, a*b)

def gen_tcases(indir, outdir, nlist, count):
    for n in nlist:
        for i in range(count):
            a, b, c = gen_tcase(n)

            with open(f"{indir}/N{n}_{i}.txt", "x") as f:
                f.write(f"{a}\n{b}")
            with open(f"{outdir}/N{n}_{i}.txt", "x") as f:
                f.write(f"{c}")