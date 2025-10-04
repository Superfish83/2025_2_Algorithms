/*
    bigint.cpp
    
    This file defines the Bigint class representing big unsigned integers,
    upon which the multiplication algorithms will operate.
    (addition and subtraction overloading are implemented here.)

    NOTE: this implementation has poor error checking
*/

#include <iostream>
#include <string.h>

#include "bigint.hpp"

// pad leading zeros to string
void Bigint::pad(int k){
    for(int i = N; i >= 0; i--){
        s[i + k] = s[i];
    }
    for(int i = 0; i < k; i++){
        s[i] = '0';
    }
    N += k;
    s[N] = '\0';
}

// pad the shorter one to match lengths
void pad_max(Bigint &a, Bigint &b){ 
    int Na = a.getN();
    int Nb = b.getN();
    
    if (Na < Nb) {
        a.pad(Nb - Na);
    } 
    else if (Nb < Na) {
        b.pad(Na - Nb);
    }
}

// Remove leading zeros from string if any
void Bigint::trim(){
    int lead_zeros = 0;
    while (lead_zeros < N - 1 && s[lead_zeros] == '0') {
        lead_zeros++;
    }
    if (lead_zeros > 0) {
        for (int i = lead_zeros; i < N; i++) {
            s[i - lead_zeros] = s[i];
        }
        N -= lead_zeros;
        s[N] = '\0';
    }
    if(N == 0){
        // prevent N = 0
        N=1;
        s[0] = '0';
        s[1] = '\0';
    }
}

// constructors
// 0 with N digits
Bigint::Bigint() {
    N=1;
    s[0] = '0';
    s[1] = '\0';
}

Bigint::Bigint(int N) {
    this->N = N;
    for(int i = 0; i < N; i++){
        s[i] = '0';
    }
    s[N] = '\0';
}

// initialize from string with padding leading zeros if necessary
Bigint::Bigint(const char* text) {
    N = strlen(text);
    for(int i = 0; i < N; i++) {
        s[i] = text[i];
    }
    s[N] = '\0';
    trim();
}

// copy substring from other Bigint
Bigint::Bigint(const Bigint &other, int start_digit, int length) {
    N = (length == -1) ? other.getN() : length;
    sign = other.getSign();
    for(int i = 0; i < N; i++) {
        s[i] = other.getDigit(start_digit + i) + '0';
    }
    s[N] = '\0';
    trim();
}

// multiply by 10^k
void Bigint::mult10(int k){
    for(int i = N; i < N+k; i++){
        s[i] = '0';
    }
    N += k;
    s[N] = '\0';
    trim();
}

// operator overloads
// comparison (>)
// NOTE: this assumes that this and other are padded appropriately.
bool Bigint::operator>(const Bigint &other) const {
    if(this->getSign() && !other.getSign()) return false;
    if(!this->getSign() && other.getSign()) return true;

    for(int i = 0; i < N; i++) {
        if(this->getDigit(i) > other.getDigit(i)) return !this->getSign();
        if(this->getDigit(i) < other.getDigit(i)) return this->getSign();
    }

    return false;
}

// addition
Bigint Bigint::operator+(const Bigint &other) const {
    // copy operands to local instances
    Bigint result = Bigint(*this, 0, -1);
    Bigint tmp = Bigint(other, 0, -1);

    // temporarily pad both numbers to the same length
    pad_max(result, tmp);

    // * redirect operation if signs differ *
    if (result.getSign() != tmp.getSign()) {
        if(result.getSign()){ // if result < 0
            result.setSign(0);
            return tmp - result;
        }
        else{ // if tmp < 0
            tmp.setSign(0);
            return result - tmp;
        }
    }

    // pad to handle possible carry
    result.pad(1);
    tmp.pad(1);

    // perform addition
    int carry = 0;
    for(int i = result.getN() - 1; i >= 0; i--){
        int sum = (result.getDigit(i)) + (tmp.getDigit(i)) + carry;
        result.setDigit(i, sum % 10);
        carry = sum / 10;
    }

    // trim and return
    result.trim();
    return result;
}

// subtraction
Bigint Bigint::operator-(const Bigint &other) const {
    // copy operands to local instances
    Bigint result = Bigint(*this, 0, -1);
    Bigint tmp = Bigint(other, 0, -1);

    // temporarily pad both numbers to the same length
    pad_max(result, tmp);

    // * redirect operation if signs differ *
    if (result.getSign() != tmp.getSign()) {
        tmp.negate();
        return result + tmp;
    }
    // * redirect operation if abs(other) > abs(this) *
    if ((!result.getSign() && (tmp > result)) ||
             (result.getSign() && (result > tmp))){
        Bigint res = tmp - result;
        res.negate();
        return res;
    }

    // pad to handle possible carry
    result.pad(1);
    tmp.pad(1);

    // perform subtraction
    int borrow = 0;
    for(int i = result.getN() - 1; i >= 0; i--){
        int diff = result.getDigit(i) - tmp.getDigit(i) - borrow;
        if(diff < 0){
            diff += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        result.setDigit(i, diff);
    }

    // trim and return
    result.trim();
    return result;
}

// multiplication with small positive integer (0 to 9)
Bigint Bigint::operator*(int other) const {
    Bigint result = Bigint(*this, 0, -1);
    if (other <= 0) {
        return Bigint();
    }

    // temporairly pad to handle possible carry
    result.pad(1);

    // perform multiplication
    int carry = 0;
    for(int i = result.getN() - 1; i >= 0; i--){
        int prod = (result.getDigit(i)) * other + carry;
        result.setDigit(i, prod % 10);
        carry = prod / 10;
    }

    // trim and return
    result.trim();
    return result;
}

// division with small positive integer (1 to 9)
Bigint Bigint::operator/(int other) const {
    Bigint result = Bigint(*this, 0, -1);
    if (other <= 1) {
        return result;
    }

    // perform division
    int remainder = 0;
    for (int i = 0; i < result.getN(); i++) {
        int current = remainder * 10 + result.getDigit(i);
        result.setDigit(i, current / other);
        remainder = current % other;
    }

    // trim and return
    result.trim();
    return result;
}