#include "launcher.h"
#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <subscreen.h>
#include "utils.h"
#include "button.h"

// This global constant can live here perfectly fine
str LAUNCHER_VERSION = "1.0.0";

// 1. The Constructor implementation
Launcher::Launcher(str version) {
    EDITOR_VERSION = version;
    running = true;
    width = 1152.0;
    height = 648.0;
    bg_color = launcher_colors.launcher_bg;
    
    str title = "DevPace Launcher v" + LAUNCHER_VERSION;
    InitWindow(width, height, title.c_str());

    //subscreens
    topBar = SubScreen(0.0, 0.0, width, 25.0, launcher_colors.top_bar_bg);
    create_button = Button(1.0, 1.0, 50.0, 37.0, launcher_colors.create_button_norm, 
        launcher_colors.create_button_hovered, "+", launcher_colors.create_button_text);
    print_dict(read_json("data/launcher_data.json")); //test and debug json reading
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

    //button updates
    create_button.update();

}

// 4. The render step implementation
void Launcher::render() {
    topBar.begin_draw();
        create_button.render();
    topBar.end_draw();

    BeginDrawing();
        ClearBackground(bg_color); 

        topBar.render_to_window(); 
    
    EndDrawing();
}