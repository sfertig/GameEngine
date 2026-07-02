#ifndef SUBSCREEN_H
#define SUBSCREEN_H

#include <raylib.h>

class SubScreen {
private:
    RenderTexture2D canvas; // The off-screen drawing surface
    Rectangle bounds;       // X, Y, Width, Height on the main window
    Color bg_color;

public:
    // Constructor: Takes position, size, and background color
    SubScreen() = default;
    SubScreen(float x, float y, float width, float height, Color background);
    
    // Destructor: Clean up GPU memory!
    ~SubScreen();

    // Core Engine Flow
    void begin_draw();
    void end_draw();
    void render_to_window();

    // Helper to get mouse position relative to THIS subscreen
    Vector2 get_local_mouse_pos();
};

#endif