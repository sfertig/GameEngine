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
    reinit();
    print_dict(read_json("data/launcher_data.json")); //test and debug json reading
}

void Launcher::reinit() {
    InitWindow(width, height, title.c_str());
    SetExitKey(KEY_NULL);
    //SetWindowTitle(title.c_str());
    //subscreens
    topBar = SubScreen(0.0,
    0.0, width,
    25.0, launcher_colors.top_bar_bg);
    create_button = Button(1.0,
    1.0,
    50.0,
    37.0, launcher_colors.create_button_norm, 
        launcher_colors.create_button_hovered,
    "+", 
        launcher_colors.create_button_text,
    20);
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
    if (IsKeyDown(KEY_ESCAPE) && IsKeyDown(KEY_LEFT_SHIFT)) {
        running = false;
    }
    //button updates
    create_button.update(topBar.get_local_mouse_pos());
    if (create_button.is_pressed || (IsKeyDown(KEY_LEFT_CONTROL) && IsKeyDown(KEY_N))) {
        NewProjectWin new_project_win = NewProjectWin(800, 600);
        new_project_win.run();
        //reinit window
        reinit();
    }
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

NewProjectWin::NewProjectWin(int width, int height) {
    this->width = width;
    this->height = height;
    bg_color =  Color{54, 61, 74, 255};
    running = true;

    CloseWindow(); // Close the launcher window when opening the new project window
    InitWindow(width, height, "New Project Creation"); 
    SetTargetFPS(60);
    SetExitKey(KEY_NULL);
    nameText = Button(5.0, 5.0, 215.0, 20.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255}, 
        "Project Name:", 
        Color{255, 255, 255, 255}, 
        20); nameText.is_active = false;
    name_box = TextInputBox(5.0, 25.0, 215.0, 30.0, 
        Color{200, 200, 200, 255}, 
        Color{150, 150, 150, 255}, 
        Color{0, 0, 0, 255}, 20); name_box.is_active = true; // Start with the text box active
    
    create_button = Button(5.0, 60.0, 100.0, 30.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255}, 
        "Create", 
        Color{255, 255, 255, 255}, 
        20); 

    cancel_button = Button(115.0, 60.0, 100.0, 30.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255}, 
        "Cancel", 
        Color{255, 255, 255, 255}, 
        20);

    
}

void NewProjectWin::run() {
    while(running) {
        update();
        render();
    }
    CloseWindow(); // Close the new project window when done
}

void NewProjectWin::update() {
    if (WindowShouldClose()) {
        running = false;
    }
    if (IsKeyPressed(KEY_ESCAPE) && !(name_box.is_active)) {
        running = false;
    }
    name_box.update(GetMousePosition());
    create_button.update(GetMousePosition());
    cancel_button.update(GetMousePosition());

    if (cancel_button.is_pressed) {
        running = false;
    }
    else if (create_button.is_pressed) {
        createProject();
        // will add later: running = false;
    }
}

void NewProjectWin::createProject(){
    //test for now
    str name = FormatName();
    print_str("Creating project with name: " + name);
    str path = "projects/" + name;
    
}

void NewProjectWin::render() {
    name_box.render();

    BeginDrawing();
        ClearBackground(bg_color);

        nameText.render();
        name_box.renderToWin();

        create_button.render();
        cancel_button.render();

    EndDrawing();
}

str NewProjectWin::FormatName() {
    str name = name_box.text;
    str text = "";
    for (char c : name) {
        if (isalnum(c) || c == '_') {
            text += c;
        }
        else if (isspace(c) || c == ' ' || c == '-') {
            text += '_'; // Replace spaces with underscores
        }
    }
    return text;
}
