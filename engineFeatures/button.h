#ifndef BUTTON_H
#define BUTTON_H

#include <raylib.h>
#include <string>
#include <iostream>

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

    //funcs
    Button() = default;
    Button(float x, float y, float width, float height, Color bg_color);
    Button(float x, float y, float width, float height, Color bg_color, Color hover_color, str text, Color text_color, int text_size);

    void update(Vector2 mouse_pos);
    void render();
    
};

#endif