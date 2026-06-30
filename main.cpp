#include "raylib.h"


int main() {
    // Initialize window: width, height, title
    InitWindow(800, 450, "raylib [core] example - basic window");

    SetTargetFPS(60); // Set game to run at 60 frames-per-second

    while (!WindowShouldClose()) { // Detect window close button or ESC key
        BeginDrawing();
            ClearBackground(RAYWHITE);
            DrawText("Congrats! You created your first window!", 190, 200, 20, LIGHTGRAY);
        EndDrawing();
    }

    CloseWindow(); // Close window and OpenGL context
    return 0;
}
