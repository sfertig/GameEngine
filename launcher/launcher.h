
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
typedef std::unordered_map<str, str> str_dict; 


extern str_dict recents_list;

class ProjectDisplay{
    public:
        //vars
        int width, height, x, y;
        Color bg_color;
        SubScreen screen;
        str path;
        str name;
        SubScreen* canvas;

        Button remove_btn;
        bool remove_btn_active;

        Button run_btn;

        //funcs
        ProjectDisplay(int x, int y, int width, int height, str path, str name, SubScreen& canvas);
        void update();
        void render();
        void render_to_canvas();
        void move_y(int i);

};


class Launcher {
    public:
        //vars
        bool running;

        float width; float height;
        Color bg_color;

        str EDITOR_VERSION;
        str title;
        SubScreen topBar;
        SubScreen projectList;
        Button create_button;
        Button refresh_button;
        Button regen_btn;

        std::vector<ProjectDisplay> projects;

        //funcs
        Launcher(str version);
        void reinit();
        void gen_projects();
        void run();
        void update();
        void render();
        void handle_projectDisplay_scroll();
        bool can_scroll(int i);
        void regen_projects_folder();
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
