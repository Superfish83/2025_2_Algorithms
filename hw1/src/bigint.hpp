/*
    bigint.hpp
    
    This file defines the Bigint class representing big unsigned integers,
    upon which the multiplication algorithms will operate.
    (addition and subtraction overloading are implemented here.)
*/

#include <iostream> // for debugging

#define MAX_DIGITS 1024
#define BASECASE_N 70

// Big (unsigned) integer class that stores large integers as strings
class Bigint {
protected:
    int N; // number of digits
    bool sign = 0; // is negative | 0: positive, 1: negative
    char s[MAX_DIGITS+1];
public:
    Bigint();
    Bigint(int N);
    Bigint(const char* text);
    Bigint(const Bigint &other, int start_digit, int length);

    int getN() const { return N; }
    const char* getStr() const { return s; }
    inline char getDigit(int index) const { return s[index] - '0'; }
    inline bool getSign() const { return sign; }
    
    inline void setDigit(int index, int value) { s[index] = value + '0'; }
    inline void setSign(bool value) { sign = value; }
    inline void negate() { sign = !sign; }
    void mult10(int k); // multiply by 10^k

    void pad(int k); // pad leading zeros, k times
    void trim(); // remove leading zeros

    // operator overloads
    Bigint operator+(const Bigint &other) const;
    Bigint operator-(const Bigint &other) const;
    Bigint operator*(int other) const;
    Bigint operator/(int other) const;
    bool operator>(const Bigint &other) const;
};

void pad_max(Bigint &a, Bigint &b);

// function pointer type for multiplication functions
typedef Bigint (*fp_mult)(Bigint, Bigint);

// declare multiplication functions
Bigint mult_gradeschool(Bigint a, Bigint b);
Bigint mult_karatsuba(Bigint a, Bigint b);
Bigint mult_toomcook(Bigint a, Bigint b);