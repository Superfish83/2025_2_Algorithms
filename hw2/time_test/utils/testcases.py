import random

################ Test Directory Paths ################
TEST_DIR = "./tests"
IN_DIR = f"{TEST_DIR}/input"
EXP_DIR = f"{TEST_DIR}/expected"
OUT_DIR = f"{TEST_DIR}/output"
TIME_DIR = f"{TEST_DIR}/time"
FIGS_DIR = f"./figures"
######################################################


def read_array(path):
    with open(path, "r") as f:
        arr = [int(x) for x in f.read().strip().split()]
    return arr

def write_array(path, arr):
    with open(path, "w") as f:
        for x in arr:
            f.write(f"{x} ")
        f.write("\n")

# Generate testcase of a random array
def gen_tcase(N):
    arr = random.sample(range(1, 10000001), N)

    # [TESTCASE INPUT] (1) random array
    write_array(f'{IN_DIR}/N{N}_random.txt', arr)

    arr.sort()

    # [TESTCASE INPUT] (2) sorted array
    write_array(f'{IN_DIR}/N{N}_sorted.txt', arr)

    # [TESTCASE EXPECTED OUTPUT] sorted array
    write_array(f'{EXP_DIR}/N{N}.txt', arr)

    arr.reverse()

    # [TESTCASE INPUT] (3) reversed array
    write_array(f'{IN_DIR}/N{N}_reversed.txt', arr)
    
    arr.reverse()
    # Swap 10% of the elements
    for _ in range(N // 20):
        i1 = random.randint(0, N - 1)
        i2 = random.randint(0, N - 1)
        arr[i1], arr[i2] = arr[i2], arr[i1]
    
    # [TESTCASE INPUT] (4) nearly sorted array
    write_array(f'{IN_DIR}/N{N}_nearlysorted.txt', arr)

        
def gen_tcases(nlist):
    for N in nlist:
        print(f"Generating testcases for N={N}...", end=" ", flush=True)
        gen_tcase(N)
        print("done.")



############# below: for directory structure management #############
import os

# Recursively remove a directory and its contents (equivalent to 'rm -r -f')
def rmdir_recursively(path):
    if os.path.isdir(path):
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            rmdir_recursively(full_path)
        os.rmdir(path)
    else:
        os.remove(path)

def make_test_dirs():
    if os.path.exists(TEST_DIR):
        rmdir_recursively(TEST_DIR)
    os.mkdir(TEST_DIR)

    os.mkdir(IN_DIR)
    os.mkdir(EXP_DIR)
    os.mkdir(OUT_DIR)
    os.mkdir(TIME_DIR)