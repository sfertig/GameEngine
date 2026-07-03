
#ifndef LAUNCHER_H
#define LAUNCHER_H

#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <raylib.h>
#include <unordered_map>
#include "subscreen.h"
#include "button.h"

typedef std::string str;



class Launcher {
    public:
        //vars
        bool running;

        float width; float height;
        Color bg_color;

        str EDITOR_VERSION;
        str title;
        SubScreen topBar;
        Button create_button;

        //funcs
        Launcher(str version);
        void reinit();
        void run();
        void update();
        void render();
};

class NewProjectWin{
    public:
        //vars
        int width; int height;
        Color bg_color;

        bool running;

        TextInputBox name_box;

        //funcs
        NewProjectWin() = default;
        NewProjectWin(int width, int height);

        void run();
        void update();
        void render();
};


#endif
