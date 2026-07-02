#include "subscreen.h"

SubScreen::SubScreen(float x, float y, float width, float height, Color background) {
    bounds = { x, y, width, height };
    bg_color = background;
    
    // Allocate a custom canvas texture on the GPU
    canvas = LoadRenderTexture((int)width, (int)height);
}

SubScreen::~SubScreen() {
    // Crucial C++ step: Free up the GPU memory when the subscreen is destroyed
    UnloadRenderTexture(canvas);
}

void SubScreen::begin_draw() {
    // Direct all future drawing commands away from the main window and onto this canvas
    BeginTextureMode(canvas);
    ClearBackground(bg_color);
}

void SubScreen::end_draw() {
    // Tell Raylib to stop drawing to this canvas and restore normal window rendering
    EndTextureMode();
}

void SubScreen::render_to_window() {
    // Raylib render textures are upside down by default due to OpenGL coordinates.
    // We flip the source rectangle's height negative to draw it right side up!
    //Rectangle src = { 0, 0, bounds.width, -bounds.height };
    
    // Draw our isolated canvas directly onto the main window screen
    //DrawTexturePro(canvas.texture, src, bounds, { 0, 0 }, 0.0f, WHITE);

    DrawTexture(canvas.texture, (int)bounds.x, (int)bounds.y, WHITE);
}

Vector2 SubScreen::get_local_mouse_pos() {
    Vector2 global_mouse = GetMousePosition();
    return { global_mouse.x - bounds.x, global_mouse.y - bounds.y };
}