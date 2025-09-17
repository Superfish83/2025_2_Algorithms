/*
    mult_karatsuba.cpp

    Karatsuba multiplication
*/

#include "bigint.hpp"

Bigint mult_karatsuba(Bigint a, Bigint b) {
    pad_max(a, b); // pad the shorter one to match lengths
    int N = a.getN();

    // Base case for recursion
    if (N <= 50) {
        /*
        int prod = a.getDigit(0) * b.getDigit(0);

        Bigint result = Bigint(2);
        result.setDigit(0, prod / 10);
        result.setDigit(1, prod % 10);
        result.trim();

        return result;
        */
        
        return mult_gradeschool(a, b);
    }

    int N_0 = N/2; 
    int N_1 = N - N_0;
    
    // partition a and b into 2 parts
    Bigint a_high = Bigint(a, 0, N_0);
    Bigint b_high = Bigint(b, 0, N_0);
    Bigint a_low = Bigint(a, N_0, N_1);
    Bigint b_low = Bigint(b, N_0, N_1);

    // 3 recursive calls
    Bigint z0 = mult_karatsuba(a_high, b_high);
    Bigint z1 = mult_karatsuba(a_high + a_low, b_high + b_low);
    Bigint z2 = mult_karatsuba(a_low, b_low);

    // compute according to the recurrence relation
    // a*b = [ z0 * 10^N ] + [ (z1 - z0 - z2) * 10^(N/2) ] + z2
    Bigint result = Bigint(z0, 0, -1);
    result.mult10(N_1);
    result = result + (z1 - z0 - z2);
    result.mult10(N_1);
    result = result + z2;
    result.trim();

    return result;
}