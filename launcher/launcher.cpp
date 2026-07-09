#include "launcher.h"
#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <subscreen.h>
#include "utils.h"
#include "button.h"
// This global constant can live here perfectly fine
str LAUNCHER_VERSION = "1.1.0";

str_dict recents_list = read_json("data/launcher_data.json");
const int scroll_speed = 20;
const int arrow_factor = 10;
const int arrow_scroll_speed = scroll_speed/arrow_factor;

// 1. The Constructor implementation
Launcher::Launcher(str version) {
    recents_list = read_json("data/launcher_data.json");
    EDITOR_VERSION = version;
    running = true;
    width = 1152.0;
    height = 648.0;
    bg_color = Color{209, 235, 14, 255};
    
    title = "DevPace Launcher v" + LAUNCHER_VERSION;
    reinit();
    print_dict(recents_list); //test and debug json reading
}

void Launcher::reinit() {
    save_json("data/launcher_data.json", recents_list);
    InitWindow(width, height, title.c_str());
    SetExitKey(KEY_NULL);
    SetWindowTitle(title.c_str());
    //subscreens
    topBar = SubScreen(0.0,
    0.0, width,
    25.0, launcher_colors.top_bar_bg);
    create_button = Button(1.0,
    1.0,
    50.0,
    24.0, launcher_colors.create_button_norm, 
        launcher_colors.create_button_hovered,
    "+", 
        launcher_colors.create_button_text,
    20);
    refresh_button = Button(55.0,
    1.0,
    50.0,
    24.0, launcher_colors.create_button_norm, 
        launcher_colors.create_button_hovered,
    "R", 
        launcher_colors.create_button_text,
    20);
    projectList = SubScreen(0.0, 25.0, width, height-25.0, Color{33, 38, 46, 255});
    gen_projects();
}

void Launcher::gen_projects() {
    int _x = 5;
    int _y = 10;
    int _w = width - _x*2;
    int _h = 100;
    projects.clear();
    for (auto &entry : recents_list) {
        //check if project path is valid
        if (!folder_exists(entry.second)) {
            //remove from recents
            recents_list.erase(entry.first);
        } else {
            projects.push_back(
                ProjectDisplay(_x, _y, _w, _h, entry.second, projectList)
            );
            _y += _h+10;
        }
    }
}
// 2. The run loop implementation
void Launcher::run() {
    while (running) {
        update();
        render();
    }
    save_json("data/launcher_data.json", recents_list);
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

    refresh_button.update(topBar.get_local_mouse_pos());
    if (refresh_button.is_pressed || (IsKeyDown(KEY_LEFT_CONTROL) && IsKeyDown(KEY_R))) {
        print_str("Refreshing project list");
        gen_projects();
    }
    for (ProjectDisplay &project : projects) {
        project.update();
    }

    //scrolling project list
    handle_projectDisplay_scroll();

}
// 4. The render step implementation
void Launcher::render() {
    topBar.begin_draw();
        create_button.render();
        refresh_button.render();
    topBar.end_draw();

    for (ProjectDisplay &project : projects) {
        project.render();
    }
    projectList.begin_draw();
        for (ProjectDisplay &project : projects) {
            project.render_to_canvas(); // Draws directly onto the list view!
        }
    projectList.end_draw();

    BeginDrawing();
        ClearBackground(bg_color); 

        topBar.render_to_window(); 
        projectList.render_to_window();

    
    EndDrawing();
}

void Launcher::handle_projectDisplay_scroll(){
    if (IsKeyDown(KEY_UP) && can_scroll(-arrow_scroll_speed)) {
        for (ProjectDisplay &project : projects) {
        project.move_y(-arrow_scroll_speed);
    }
    }
    else if (IsKeyDown(KEY_DOWN) && can_scroll(arrow_scroll_speed)) {
        for (ProjectDisplay &project : projects) {
        project.move_y(arrow_scroll_speed);
    }
    }
    int scroll = GetMouseWheelMove();
    if (scroll != 0.0 && can_scroll(-(scroll*scroll_speed))) {
        for (ProjectDisplay &project : projects) {
        project.move_y(int(-(scroll*scroll_speed)));
    }
    }
}

bool Launcher::can_scroll(int i){
    for (ProjectDisplay &project : projects) {
    if (project.y+i+project.height > height || project.y + i < 0) {return false;}
    }
    return true;
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
        Color{39, 45, 79, 255}, 
        Color{119, 137, 237, 255}, 
        "Advanced Settings", 
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
    //if all goes well add to project list
    recents_list[name] = path;
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

ProjectDisplay::ProjectDisplay(int x, int y, int width, int height, str path, SubScreen& canvas) {
    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;
    this->path = path;
    this->bg_color = Color{46, 46, 59, 255};
    this->screen = SubScreen(x, y, width, height, bg_color);
    this->canvas = &canvas;
}

void ProjectDisplay::update(){

}

void ProjectDisplay::render(){
    screen.begin_draw();
        DrawText(path.c_str(), 15, 15, 18, WHITE);
    screen.end_draw();
}

void ProjectDisplay::render_to_canvas(){
    
    Rectangle src = { 0, 0, (float)width, -(float)height };
    Rectangle dest = { (float)x, (float)y, (float)width, (float)height };
    
    // Draw the item card's texture asset straight onto the parent texture!
    DrawTexturePro(screen.canvas.texture, src, dest, { 0, 0 }, 0.0f, WHITE);
}

void ProjectDisplay::move_y(int i){
    y += i;
    screen.bounds.y += i;
}
