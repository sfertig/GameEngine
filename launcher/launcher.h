
#ifndef LAUNCHER_H
#define LAUNCHER_H

#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <raylib.h>

typedef std::string str;

class Launcher {
    public:
        //vars
        bool running;

        int width; int height;
        Color bg_color;
        //funcs
        Launcher();
        void run();
        void update();
        void render();
};


#endif
