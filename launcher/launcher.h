
#ifndef LAUNCHER_H
#define LAUNCHER_H

#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <raylib.h>
#include <unordered_map>

typedef std::string str;



class Launcher {
    public:
        //vars
        bool running;

        int width; int height;
        Color bg_color;

        str EDITOR_VERSION;

        //funcs
        Launcher(str version);
        void run();
        void update();
        void render();
};


#endif
