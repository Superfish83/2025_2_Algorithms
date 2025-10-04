import os
import subprocess
import matplotlib.pyplot as plt

from gen_tcases import gen_tcases


BUILD_PATH = "build/run_algo"
ALGO_LIST = ["gradeschool", "karatsuba", "toomcook"]

TEST_DIR = "tests"
IN_DIR = f"{TEST_DIR}/input"
EXP_DIR = f"{TEST_DIR}/expected_output"
OUT_DIR = f"{TEST_DIR}/output"
TIME_DIR = f"{TEST_DIR}/runtime"

TCASE_N_LIST = range(25, 501, 25)
TCASE_COUNT = 20  # number of testcases per N

# Recursively remove a directory and its contents (equivalent to 'rm -r -f')
def rmdir_recursively(path):
    if os.path.isdir(path):
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            rmdir_recursively(full_path)
        os.rmdir(path)
    else:
        os.remove(path)

# Print if the result matches the expected output
def print_result(inpath, exppath, outpath):
    with open(inpath, "r") as f:
        indata = f.read().strip()
    with open(exppath, "r") as f:
        outdata = f.read().strip()
    with open(outpath, "r") as f:
        resdata = f.read().strip()
    
    if(outdata == resdata):
        print(f"Correct")
        return
    else:
        print("Wrong")
        print(f"Input: {indata}")
        print(f"* Expected: {outdata}")
        print(f"* Output: {resdata}")

# retrieve measured algorithm runtime in milliseconds
def retrieve_runtime(timepath):
    with open(timepath, "r") as f:
        runtime = f.read().strip()
    return float(runtime)

# Draw runtime comparison graph
def plot_runtime(runtime_data):
    plt.axhline(y=0, color='k')
    for algo in ALGO_LIST:
        plt.plot(TCASE_N_LIST, runtime_data[algo], label=algo, marker='o')
    plt.xlabel("Number of Digits (N)")
    plt.ylabel("runtime [ms]")
    plt.title("Multiplication Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # (1) Prepare directory
    print("Preparing directories...")
    if os.path.exists(TEST_DIR):
        rmdir_recursively(TEST_DIR)
    os.mkdir(TEST_DIR)
    os.mkdir(IN_DIR)     # test case input files
    os.mkdir(EXP_DIR)    # test case (desired) output files
    os.mkdir(OUT_DIR)    # algorithm execution result files
    for algo in ALGO_LIST: 
        os.mkdir(f"{OUT_DIR}/{algo}")
    os.mkdir(TIME_DIR)   # algorithm execution runtime files

    # (2) Generate testcases
    print("Generating testcases...")
    gen_tcases(indir = IN_DIR, outdir = EXP_DIR,
               nlist = TCASE_N_LIST, count=TCASE_COUNT)
    
    # (3) Run tests
    print("Running tests...")
    print(f"This will load testcase input from '{IN_DIR}' and write results to '{OUT_DIR}'. The expected testcases should be in '{EXP_DIR}'.")

    runtime_data = { algo: [] for algo in ALGO_LIST }
    # Run tests for each algorithm
    for algo in ALGO_LIST:
        # Run tests for testcases
        for n in TCASE_N_LIST:
            mean_runtime = 0.0
            for i in range(TCASE_COUNT):
                print(f"testing N={n} for {algo}... (i={i}) ", end='', flush=True)
                inpath = f"{IN_DIR}/input_N{n}_{i}.txt"
                exppath = f"{EXP_DIR}/output_N{n}_{i}.txt"
                outpath = f"{OUT_DIR}/{algo}/output_N{n}_{i}.txt"
                timepath = f"{TIME_DIR}/{algo}runtime_N{n}_{i}.txt"
        
                # Run the algorithm (implemented with C++)
                res = subprocess.run([BUILD_PATH, algo, inpath, outpath, timepath],
                    capture_output=True, text=True, check=True)
                
                #print('\n\n[DEBUG] Subprocess call result:')
                #print(res)
                
                print_result(inpath, exppath, outpath)
                mean_runtime += retrieve_runtime(timepath)
            runtime_data[algo].append(mean_runtime / TCASE_COUNT)

    print("testing complete.")
    
    # (4) Plot runtime comparison graph
    plot_runtime(runtime_data)
    plt.savefig(f"{TEST_DIR}/result.png")