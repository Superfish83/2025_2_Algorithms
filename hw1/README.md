
# Algorithms HW #1-2: implementing Integer Multiplication

Author: Yeonjun Kim (2024-13755 / Dept. of Computer Science and Enginnering)
Date: 2025-09-20
This code is tested in Ubuntu 24 environment.

## Features
- Grade-school / Karatsuba / Toom-Cook (Toom-3) multiplication.
- Automatic test case generation and testing, runtime comparison.

## How to build and run
**In this assignment, I used C++ to implement the integer class and the multiplication algorithms, and used Python for testing and plotting.**
- The C++ program is located in `./build/` directory. You can compile the source code by running `./build.sh` (in Linux environment).
- You can run automatic testing by running `python3 ./test.py`. This program does three jobs:
	- Automatically generates random testcases for different N's.
	- Calls the C++ program, records the output and checks correctness.
	- Plots the runtime versus N for each of the 3 algorithms.

## Directory structure
- `./`: Python code and script
    - `README.md`
	-  `./build.sh`: shell script for C++ compilation
	- `./test.py`: tests the program and plots runtime graphs
	- `./gen_tcases.py`:  generates random testcases for different N's
- `./src/`: C++ source code 
    - `run_algo.cpp`: where main() of C++ program is located. handles file I/O, calls one of the multiplication function, measures the running time
	- `bigint.cpp, bigint.hpp`: my implementation for big integer class
	- `mult_gradeschool.cpp, mult_karatsuba.cpp, mult_toomcook.cpp`: integer multiplication functions.
-  `./build/`: C++ build
-  `./tests/`: where testcase input, output, execution result, runtime files are stored
