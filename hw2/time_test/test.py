import time

from algorithms import *

from utils.testcases import *
from utils.plot import *

################# Test Configuration #################
# (directory paths for testing are set in utils/testcases.py)

ALGO_LIST = [Insert_Sort, Merge_Sort, Quick_Sort, Quick_DualPivot_Sort]
ALGO_NAME_LIST = ["Insert", "Merge", "Quick", "QuickDualPivot"]

TCASE_N_LIST = [1000, 10000, 100000] #10^3, 10^4, 10^5
TCASE_CLASS_LIST = ["random", "sorted", "reversed", "nearlysorted"]
######################################################


# Run algorithm, check correctness, and measure runtime.
# Returns correctness and runtime in milliseconds.
def run_test(algo_func, in_path, exp_path, out_path, time_path):
    # (0) Load input
    arr = read_array(in_path)

    # (1) Run the algorithm and measure runtime
    time_start = time.process_time()

    algo_func(arr)

    time_end = time.process_time()
    runtime_ms = (time_end - time_start) * 1000
    with open(time_path, "w") as f:
        f.write(f"{runtime_ms}\n")

    # (2) Write result to output file
    write_array(out_path, arr)

    # (3) Check correctness
    expected = read_array(exp_path)
    isCorrect = (arr == expected)
        
    # (4) Return
    return isCorrect, runtime_ms


if __name__ == "__main__":
    # (1) Prepare directory
    print("[ALGORITHM TEST] (1) Preparing directories...")
    make_test_dirs()
    print("[ALGORITHM TEST] directory preparation complete.")

    # (2) Generate testcases
    print("[ALGORITHM TEST] (2) Generating testcases...")
    gen_tcases(TCASE_N_LIST)
    print("[ALGORITHM TEST] testcase generation complete.")
    
    # (3) Run tests
    print("[ALGORITHM TEST] (3) Running tests...")
    
    for i, algo_name in enumerate(ALGO_NAME_LIST):
        algo_func = ALGO_LIST[i]

        # Run tests for testcases
        for N in TCASE_N_LIST:
            for tclass in TCASE_CLASS_LIST:
                in_path = f"{IN_DIR}/N{N}_{tclass}.txt"
                exp_path = f"{EXP_DIR}/N{N}.txt"
                out_path = f"{OUT_DIR}/{algo_name}_N{N}_{tclass}.txt"
                time_path = f"{TIME_DIR}/{algo_name}_N{N}_{tclass}.txt"
                    
                print(f"testing {algo_name} with testcase '{in_path}'...", end=' ', flush=True)
        
                isCorrect, runtime_ms = run_test(algo_func, in_path, exp_path, out_path, time_path)

                if isCorrect:
                    print(f"Output is correct! (took {runtime_ms:.2f} ms)")
                else:
                    print(f"Output is wrong (took {runtime_ms:.2f} ms)")

    print("[ALGORITHM TEST] testing complete.")
    
    # (4) Plot runtime comparison graph
    print("[ALGORITHM TEST] plotting measured runtime...")
    plot_runtime(ALGO_NAME_LIST, TCASE_N_LIST, TCASE_CLASS_LIST)
    print("[ALGORITHM TEST] plotting complete.")
    print(f"\tfigures are saves at '{FIGS_DIR}'.")

    print("[ALGORITHM TEST] all done. (Profit!!!!!!)")