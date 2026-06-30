#include "launcher.h"
#include <iostream>
#include <vector>
#include <string>
#include <variant>

// This global constant can live here perfectly fine
str LAUNCHER_VERSION = "1.0.0";

// 1. The Constructor implementation
Launcher::Launcher() {
    running = true;
    width = 800;
    height = 600;
    bg_color = LIGHTGRAY;
    
    str title = "DevPace Launcher v" + LAUNCHER_VERSION;
    InitWindow(width, height, title.c_str());
}

// 2. The run loop implementation
void Launcher::run() {
    while (running) {
        update();
        render();
    }
}

// 3. The update loop implementation
void Launcher::update() {
    if (WindowShouldClose()) {
        running = false;
    }
}

// 4. The render step implementation
void Launcher::render() {
    BeginDrawing();

    ClearBackground(bg_color);
    
    EndDrawing();
}