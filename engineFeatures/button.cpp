#include <raylib.h>
#include <string>
#include <iostream>
#include "button.h"
#include "subscreen.h"
#include "utils.h"


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
    this->mouse_down = false;
}

Button::Button(float x, float y, float width, float height, Color bg_color, Color hover_color, str text, Color text_color, int text_size) {
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
    this->mouse_down = false;
}

void Button::update(Vector2 mouse_pos) {
    is_hovered = false;
    is_pressed = false;

    //hovering
    if (collideRect(mouse_pos, Rectangle{x, y, width, height})) {
        is_hovered = true;

        //clicking
        if (IsMouseButtonDown(MOUSE_LEFT_BUTTON)) {
            mouse_down = true;
        } else {
            if (mouse_down) {
                is_pressed = true; // Button was clicked
            }
            mouse_down = false;
        }
    } else {
        mouse_down = false; // Reset mouse down state if not hovering

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

TextInputBox::TextInputBox(float x, float y, float width, float height, Color bg, Color active_bg, Color text_color, int text_size) {
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    this->bg = bg;
    this->active_bg = active_bg;
    this->text_color = text_color;
    this->text_size = text_size;

    this->text = "";

    this->is_active = false;

    // Initialize the SubScreen box
    box = SubScreen(x, y, width, height, bg);
}
void TextInputBox::update(Vector2 mouse_pos){
    // Keep your excellent collision logic!
    Rectangle click_area = {box.bounds.x, box.bounds.y, box.bounds.width, box.bounds.height};
    
    if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) {
        if (collideRect(mouse_pos, click_area)) {
            is_active = true;
        } else {
            is_active = false;
        }
    }

    if (is_active) {
        // 1. Handle Backspace (Use IsKeyPressed or IsKeyDown)
        if (IsKeyPressed(KEY_BACKSPACE) && text.size() > 0) {
            text.pop_back();
        }
        
        // 2. Clear key presses by processing Raylib's queue properly
        int key = GetCharPressed();
        while (key > 0) {
            // Only allow normal text range characters (printable ASCII)
            if ((key >= 32) && (key <= 125)) {
                text += (char)key;
            }
            key = GetCharPressed(); // Grab next character in queue
        }
    }
}

void TextInputBox::render(){
    // Set your active color swap cleanly
    box.bg_color = is_active ? active_bg : bg;

    box.begin_draw();
        // FIXED: Draw text at local relative coordinates (0, 0) inside the box!
        // We add a tiny offset padding (like 5 pixels) so text doesn't slam into the edge.
        DrawText(text.c_str(), 5, 5, text_size, text_color);
    box.end_draw();
}

void TextInputBox::renderToWin(){
    box.render_to_window();
}

