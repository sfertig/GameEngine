
#ifndef LAUNCHER_H
#define LAUNCHER_H

#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <raylib.h>
#include <unordered_map>
#include "subscreen.h"

typedef std::string str;



class Launcher {
    public:
        //vars
        bool running;

        float width; float height;
        Color bg_color;

        str EDITOR_VERSION;

        SubScreen topBar;

        //funcs
        Launcher(str version);
        void run();
        void update();
        void render();
};


#endif
