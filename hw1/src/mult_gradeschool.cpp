/*
    mult_gradeschool.cpp

    Grade school multiplication
*/

#include "bigint.hpp"

Bigint mult_gradeschool(Bigint a, Bigint b) {
    pad_max(a, b); // pad the shorter one to match lengths
    int N = a.getN();

    Bigint result = Bigint(2*N);

    // Perform multiplication
    for (int i = N - 1; i >= 0; i--) {
        int carry = 0;
        for (int j = N - 1; j >= 0; j--) {
            int prod = a.getDigit(i) * b.getDigit(j) + result.getDigit(i + j + 1) + carry;
            result.setDigit(i + j + 1, prod % 10);
            carry = prod / 10;
        }
        result.setDigit(i, result.getDigit(i) + carry);
    }

    result.trim();
    return result;
}