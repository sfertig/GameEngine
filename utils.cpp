#include "utils.h"
#include <iostream>
#include <vector>
#include <string>
#include <variant>

void print_str(str s, bool nl) {
    if (nl) {
        std::cout << s << std::endl;
    } else {
        std::cout << s;
    }
}

void print_int(int i, bool nl) {
    if (nl) {
        std::cout << i << std::endl;
    } else {
        std::cout << i;
    }
}

void nl() {
    std::cout << std::endl;
}
