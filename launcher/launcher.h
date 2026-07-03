
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

        str version;

        Button nameText;
        TextInputBox name_box;

        Button create_button;
        Button cancel_button;

        //settings
        Button settingsTag;
        TextInputBox s_fps; Button b_fps;
        TextInputBox s_width; Button b_width;
        TextInputBox s_height; Button b_height;
        TextInputBox s_bg_color; Button b_bg_color;
        TextInputBox s_title; Button b_title;

        //funcs
        NewProjectWin() = default;
        NewProjectWin(int width, int height, str version);

        void run();
        void update();
        void render();

        void createProject();

        str FormatName();
};


#endif
