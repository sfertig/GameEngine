#include "raylib.h"
#include "utils.h"
#include <string>
#include <iostream>
#include "launcher.h"

const str ENGINE_VERSION = "1.0.0";


int main() {
    SetTraceLogLevel(LOG_ERROR);
    SetExitKey(KEY_NULL);
    nl(); print_str("Devpace launched successfully"); nl();
    print_str("DevPace version: " + ENGINE_VERSION);

    //Launcher
    Launcher launcher = Launcher(ENGINE_VERSION);
    launcher.run();

    print_str("Exit with code -1");

    return 0;
}


