#include "raylib.h"
#include "utils.h"
#include <string>
#include <iostream>

const str ENGINE_VERSION = "1.0.0";


int main() {
    nl(); print_str("Devpace launched successfully"); nl();
    print_str("DevPace version: " + ENGINE_VERSION);

    return 0;
}
