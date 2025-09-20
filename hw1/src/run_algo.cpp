#include <fstream>
#include <string.h>
#include <chrono>

#include "bigint.hpp"

using namespace std::chrono;
using namespace std;

#define TEST_TIMES 50

// read input and save to Bigint variables
void read_input(const char *inpath, Bigint &a, Bigint &b){
    char a_str[MAX_DIGITS];
    char b_str[MAX_DIGITS];

    ifstream ifs;
    ifs.open(inpath);
    ifs.getline(a_str, MAX_DIGITS);
    ifs.getline(b_str, MAX_DIGITS);
    ifs.close();

    a = Bigint(a_str);
    b = Bigint(b_str);
}

// run algorithm and write the result and runtime
void test_mult(const char *algo, const char *respath, const char *timepath, Bigint &a, Bigint &b) {
    fp_mult mult_func = nullptr;
    if(strcmp(algo, "gradeschool") == 0){ mult_func = &mult_gradeschool; }
    else if(strcmp(algo, "karatsuba") == 0){ mult_func = &mult_karatsuba; }
    else if(strcmp(algo, "toomcook") == 0){ mult_func = &mult_toomcook; }
    else{
        std::cerr << "invalid algorithm name" << std::endl;
        return;
    }

    // start measuring runtime
    auto start = system_clock::now();

    // run multiplication test
    Bigint result;
    for (int i = 0; i < TEST_TIMES; i++){
        result = (*mult_func)(a, b);
    }

    // end measuring runtime
    auto end = system_clock::now();
    float runtime = (float)( duration_cast<milliseconds>(end - start).count() ) / TEST_TIMES;
    
    // print test result to stdout
    ofstream ofs;
    ofs.open(respath);
    ofs.write(result.getStr(), result.getN());
    ofs.close();
    ofs.open(timepath);
    ofs << runtime << endl;
    ofs.close();
}   

int main(int argc, char *argv[]) {
    // (1) Get arguments (this program is called from test.py) 
    if(argc != 5){
        std::cerr << "invalid arguments" << std::endl;
        return -1;
    }
    const char *algo = argv[1];
    const char *inpath = argv[2];
    const char *respath = argv[3];
    const char *timepath = argv[4];

    // (2) Read input from file
    Bigint a = Bigint();
    Bigint b = Bigint();
    read_input(inpath, a, b);
    
    // (3) Run algorithm test
    test_mult(algo, respath, timepath, a, b);

    return 0;
}