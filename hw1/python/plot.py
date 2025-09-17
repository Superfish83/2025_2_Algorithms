import matplotlib.pyplot as plt

def get_latency(line):
    return float(line[line.find(':')+1:])

if __name__ == "__main__":
    latency = [ [], [], [] ]
    test_n = range(25, 501, 25)

    for n in test_n:
        with open(f"tests/result/N_{n}.txt", "r") as f:
            lines = f.readlines()
            
            for i in range(3):
                latency[i].append(get_latency(lines[3*i + 2]))

    plt.axhline(y=0, color='k')
    plt.plot(test_n, latency[0], label="Grade School", marker='o')
    plt.plot(test_n, latency[1], label="Karatsuba", marker='o')
    plt.plot(test_n, latency[2], label="Toom-Cook", marker='o')

    plt.xlabel("Number of Digits (N)")
    plt.ylabel("Latency [ms]")
    plt.title("Multiplication Comparison")
    plt.legend()
    plt.grid(True)

    plt.savefig("result.png")
    plt.show()