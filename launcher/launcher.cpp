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
        NewProjectWin new_project_win = NewProjectWin(800, 600, EDITOR_VERSION);
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

NewProjectWin::NewProjectWin(int width, int height, str version) {
    this->width = width;
    this->height = height;
    bg_color =  Color{54, 61, 74, 255};
    this->version = version;
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

    //settings
    settingsTag = Button(0.0, 100.0, width, 30.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255}, 
        "Settings (Coming Soon)", 
        Color{255, 255, 255, 255}, 
        20);
    //title
    b_title = Button(5.0, 140.0, 215.0, 20.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255}, 
        "Game Title:", 
        Color{255, 255, 255, 255}, 
        20); b_title.is_active = false;

    s_title = TextInputBox(5.0, 160.0, 215.0, 30.0, 
        Color{200, 200, 200, 255}, 
        Color{150, 150, 150, 255}, 
        Color{0, 0, 0, 255}, 20); s_title.text = newProjectDetails["cnfg_title"];
    //fps
    b_fps = Button(230.0, 140.0, 215.0, 20.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255},
        "FPS:",
        Color{255, 255, 255, 255}, 20.0),
    s_fps = TextInputBox(230.0, 160.0, 215.0, 30.0, 
        Color{200, 200, 200, 255}, 
        Color{150, 150, 150, 255}, 
        Color{0, 0, 0, 255}, 20); s_fps.text = newProjectDetails["cnfg_fps"];
    //bg color
    b_bg_color = Button(455.0, 140.0, 215.0, 20.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255},
        "Background Color:",
        Color{255, 255, 255, 255}, 20.0),
    s_bg_color = TextInputBox(455.0, 160.0, 215.0, 30.0, 
        Color{200, 200, 200, 255}, 
        Color{150, 150, 150, 255}, 
        Color{0, 0, 0, 255}, 20); s_bg_color.text = newProjectDetails["cnfg_bg_color"];
    //width
    b_width = Button(5.0, 200.0, 215.0, 20.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255},
        "Width:",
        Color{255, 255, 255, 255}, 20.0),
    s_width = TextInputBox(5.0, 220.0, 215.0, 30.0, 
        Color{200, 200, 200, 255}, 
        Color{150, 150, 150, 255}, 
        Color{0, 0, 0, 255}, 20); s_width.text = newProjectDetails["cnfg_width"];
    //height
    b_height = Button(230.0, 200.0, 215.0, 20.0, 
        Color{77, 89, 153, 255}, 
        Color{119, 137, 237, 255},
        "Height:",
        Color{255, 255, 255, 255}, 20.0),
    s_height = TextInputBox(230.0, 220.0, 215.0, 30.0, 
        Color{200, 200, 200, 255}, 
        Color{150, 150, 150, 255}, 
        Color{0, 0, 0, 255}, 20); s_height.text = newProjectDetails["cnfg_height"];

    
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
    else if (IsKeyDown(KEY_LEFT_CONTROL) && IsKeyPressed(KEY_ENTER)) {
        createProject();
    }
    name_box.update(GetMousePosition());
    create_button.update(GetMousePosition());
    cancel_button.update(GetMousePosition());

    s_title.update(GetMousePosition());
    s_fps.update(GetMousePosition());
    s_bg_color.update(GetMousePosition());
    s_width.update(GetMousePosition());
    s_height.update(GetMousePosition());
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
    //if project already exists, do not create
    if (folder_exists(path)) {
        print_str("Error: Project already exists at path: " + path);
        return;
    }
    //else create folder and save project details
    create_folder(path);
    create_folder(path + "/assets");
    create_folder(path + "/assets/images");
    create_folder(path + "/assets/sounds");
    create_folder(path + "/assets/models");
    create_folder(path + "/data");
    create_folder(path + "/data/scenes");
    create_folder(path + "/data/scripts");
    //create project details file
    str_dict details(newProjectDetails);
    //config json file data
    details["name"] = name;
    details["path"] = path;
    details["version"] = version;
    details["cnfg_width"] = s_width.text;
    details["cnfg_height"] = s_height.text;
    details["cnfg_fps"] = s_fps.text;
    details["cnfg_title"] = s_title.text;
    details["cnfg_bg_color"] = s_bg_color.text;
    save_json(path + "/details.json", details);
    running = false;
}

void NewProjectWin::render() {
    name_box.render();
    s_title.render();
    s_fps.render();
    s_bg_color.render();
    s_width.render();
    s_height.render();

    BeginDrawing();
        ClearBackground(bg_color);

        nameText.render();
        name_box.renderToWin();

        create_button.render();
        cancel_button.render();

        settingsTag.render();

        b_title.render();
        s_title.renderToWin();

        b_fps.render();
        s_fps.renderToWin();

        b_bg_color.render();
        s_bg_color.renderToWin();

        b_width.render();
        s_width.renderToWin();

        b_height.render();
        s_height.renderToWin();

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
    //only lowercase letters
    for (char& c : text) {
        c = tolower(c);
    }
    return text;
}
