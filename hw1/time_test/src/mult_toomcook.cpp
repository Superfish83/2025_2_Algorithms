/*
    mult_toomcook.cpp

    Toom-Cook multiplication
    (This implements Toom-3 multiplication, as described in
    https://en.wikipedia.org/wiki/Toom-Cook_multiplication)
*/ 

#include "bigint.hpp"

Bigint mult_toomcook(Bigint a, Bigint b) {
    pad_max(a, b); // pad the shorter one to match lengths
    int N = a.getN();


    // Base case for recursion
    if (N <= BASECASE_N) {
        Bigint result = mult_gradeschool(a, b);
        if(a.getSign() != b.getSign()){
            result.setSign(1);
        }
        else {
            result.setSign(0);
        }
        return result;
    }

    // partition sizes
    int N_part = (N+2)/3;
    int N_0 = N - 2 * N_part; // size of the first part
    
    // partition a and b into 3 parts
    Bigint a0 = Bigint(a, 0, N_0);
    Bigint a1 = Bigint(a, N_0, N_part);
    Bigint a2 = Bigint(a, N_0 + N_part, N_part);
    Bigint b0 = Bigint(b, 0, N_0);
    Bigint b1 = Bigint(b, N_0, N_part);
    Bigint b2 = Bigint(b, N_0 + N_part, N_part);

    // 5 recursive calls
    Bigint r_0 = mult_toomcook(a0, b0); // r(0) = a(0)*b(0)
    Bigint r_1 = mult_toomcook(a0 + a1 + a2, b0 + b1 + b2); // r(1) = (a0+a1+a2)*(b0+b1+b2)
    Bigint r_m1 = mult_toomcook(a0 - a1 + a2, b0 - b1 + b2); // r(-1) = (a0-a1+a2)*(b0-b1+b2)
    Bigint r_m2 = mult_toomcook(a0 - (a1*2) + (a2*4), b0 - (b1*2) + (b2*4)); // r(-2) = (a0-2a1+4a2)*(b0-2b1+4b2)
    Bigint r_inf = mult_toomcook(a2, b2); // r(inf) = a2*b2

    // compute according to the recurrence relation
    // interpolation (according to the sequence proposed by Bodrato(2007))
    Bigint z0 = r_0;
    Bigint z4 = r_inf;
    Bigint z3 = (r_m2 - r_1)/3;
    Bigint z1 = (r_1 - r_m1)/2;
    Bigint z2 = r_m1 - r_0;
    z3 = ((z2 - z3)/2) + (r_inf*2);
    z2 = z2 + z1 - z4;
    z1 = z1 - z3;

    // recomposition
    Bigint result = Bigint(z0, 0, -1);
    result.mult10(N_part);
    result = result + z1;
    result.mult10(N_part);
    result = result + z2;
    result.mult10(N_part);
    result = result + z3;
    result.mult10(N_part);
    result = result + z4;

    result.trim();
    return result;
}