#ifndef BUTTON_H
#define BUTTON_H

#include <raylib.h>
#include <string>
#include <iostream>
#include "subscreen.h"

typedef std::string str;

class Button {
public:
    //vars
    float x, y, width, height;
    Color bg_color;
    Color hover_color;
    str text;
    int text_size;
    Color text_color;

    bool is_hovered;
    bool is_pressed;
    bool mouse_down;
    bool is_active;

    //funcs
    Button() = default;
    Button(float x, float y, float width, float height, Color bg_color);
    Button(float x, float y, float width, float height, Color bg_color, Color hover_color, str text, Color text_color, int text_size);

    void update(Vector2 mouse_pos);
    void render();
    
};

class TextInputBox{
    public:
        //vars
        float x, y, width, height;
        Color bg;
        Color active_bg;
        str text;
        int text_size;
        Color text_color;

        SubScreen box;

        bool is_active;

        //funcs
        TextInputBox() = default;
        TextInputBox(float x, float y, float width, float height, Color bg, Color active_bg, Color text_color, int text_size);
        void update(Vector2 mouse_pos);
        void render();
        void renderToWin();
    };

#endif