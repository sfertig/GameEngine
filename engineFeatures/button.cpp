#include <raylib.h>
#include <string>
#include <iostream>
#include "button.h"


Button::Button(float x, float y, float width, float height, Color bg_color) {
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    this->bg_color = bg_color;

    this->hover_color = bg_color; // Default hover color is the same as background
    this->text = ""; // Default text is empty
    this->text_color = WHITE; // Default text color is white

    this->is_hovered = false;
    this->is_pressed = false;
}

Button::Button(float x, float y, float width, float height, Color bg_color, Color hover_color, str text, Color text_color, int text_size=20) {
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    this->bg_color = bg_color;
    this->hover_color = hover_color;
    this->text = text;
    this->text_color = text_color;
    this->text_size = text_size;

    this->is_hovered = false;
    this->is_pressed = false;
}

void Button::update() {
    // Check if the mouse is hovering over the button
    if (CheckCollisionPointRec(GetMousePosition(), { x, y, width, height })) {
        is_hovered = true;
        if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) {
            is_pressed = true;
        }
    } else {
        is_hovered = false;
        is_pressed = false;
    }
}

void Button::render() {
    // Draw the button background
    Color current_color = is_hovered ? hover_color : bg_color;
    DrawRectangle(x, y, width, height, current_color);

    // Draw the button text if it exists
    if (!text.empty()) {
        int font_size = text_size; // Use the specified font size
        Vector2 text_size = MeasureTextEx(GetFontDefault(), text.c_str(), font_size, 1);
        float text_x = x + (width - text_size.x) / 2;
        float text_y = y + (height - text_size.y) / 2;
        DrawText(text.c_str(), static_cast<int>(text_x), static_cast<int>(text_y), font_size, text_color);
    }
}

