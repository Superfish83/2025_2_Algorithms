#include <fstream>
#include <string.h>
#include <chrono>

#include "bigint.hpp"

using namespace std::chrono;

#define TEST_TIMES 100

// test correctness and measure latency of each algorithm
void test_mult(fp_mult mult_func, const char *name, Bigint &a, Bigint &b){
    // start measuring runtime
    auto start = system_clock::now();

    // run multiplication test
    Bigint result;
    for (int i = 0; i < TEST_TIMES; i++){
        result = (*mult_func)(a, b);
    }

    // end measuring runtime
    auto end = system_clock::now();
    float latency = (float)( duration_cast<milliseconds>(end - start).count() ) / TEST_TIMES;
    
    // print test result to stdout
    std::cout << name << std::endl;
    std::cout << "result:" << result.getStr() << std::endl;
    std::cout << "latency[ms]:" << latency << std::endl;
    std::cout.flush();
}   

int main(void) {
    char a_str[MAX_DIGITS];
    char b_str[MAX_DIGITS];

    // read input from stdin
    std::cin >> a_str >> b_str;
    
    Bigint a = Bigint(a_str);
    Bigint b = Bigint(b_str);

    // run tests and print results
    test_mult(mult_gradeschool, "grade school multiplication", a, b);
    test_mult(mult_karatsuba, "Karatsuba multiplication", a, b);
    test_mult(mult_toomcook, "Toom-Cook multiplication", a, b);

    return 0;
}