import matplotlib.pyplot as plt
import math
from utils.testcases import *

def get_runtime(path):
    with open(path, "r") as f:
        runtime_ms = float(f.readline().strip())
    return runtime_ms


# Draw runtime comparison graphs
def plot_runtime(ALGO_NAME_LIST, TCASE_N_LIST, TCASE_CLASSES):
    for tclass in TCASE_CLASSES:
        # (1) Prepare data
        data = {}
        for algo in ALGO_NAME_LIST:
            for N in TCASE_N_LIST:
                path = f"{TIME_DIR}/{algo}_N{N}_{tclass}.txt"
                data_item = math.log10(get_runtime(path))

                if algo not in data:
                    data[algo] = []
                data[algo].append(data_item)

        logN = [round(math.log10(x)) for x in TCASE_N_LIST]

        # (2) Plot
        plt.figure()
        plt.axhline(y=0, color='k')
        plt.grid(True)

        for algo in ALGO_NAME_LIST:
            plt.plot(logN, data[algo], label=algo, marker='o')
        
        plt.legend()

        plt.xlabel("Number of Elements (N) (log_10 scale)")
        plt.ylabel("runtime [ms] (log_10 scale)")
        plt.title(f"Sort Time Comparison ({tclass} case)")
        
        plt.savefig(f"{FIGS_DIR}/{tclass}.png")
