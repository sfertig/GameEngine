#include "utils.h"
#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <unordered_map>
#include <fstream>
#include "json.hpp"
#include <filesystem>

using json = nlohmann::json;

void print_str(str s, bool nl) {
    if (nl) {
        std::cout << s << std::endl;
    } else {
        std::cout << s;
    }
}

void print_int(int i, bool nl) {
    if (nl) {
        std::cout << i << std::endl;
    } else {
        std::cout << i;
    }
}

void print_dict(str_dict d, bool nl) {
    for (const auto& pair : d) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    if (nl) {
        std::cout << std::endl;
    }
}

void nl() {
    std::cout << std::endl;
}

bool collideRect(Vector2 pos, Rectangle rect){
    return(pos.x >= rect.x && pos.x <= rect.x + rect.width &&
        pos.y >= rect.y && pos.y <= rect.y + rect.height);
}

std::unordered_map<str, Color> Colors = {
    {"black", BLACK},
    {"blue", BLUE},
    {"brown", BROWN},
    {"gray", GRAY},
    {"green", GREEN},
    {"magenta", MAGENTA},
    {"maroon", MAROON},
    {"orange", ORANGE},
    {"pink", PINK},
    {"purple", PURPLE},
    {"red", RED},
    {"white", WHITE},
    {"yellow", YELLOW},
};

str_dict newProjectDetails = {
    {"name", "DEFAULTNAME"},
    {"path", "projects/DEFAULTNAME"},
    {"version", "1.0.0"},
    //configs
    {"cnfg_width", "800"},
    {"cnfg_height", "600"},
    {"cnfg_fps", "60"},
    {"cnfg_title", "DevPace Editor v1.0.0"},
    {"cnfg_bg_color", "white"},
    {"cnfg_start_scene", ""},
    //scenes (none made by default)

};

//reading json

str_dict read_json(str path) {
    std::ifstream file(path);
    str_dict details = {};
    
    if (file.is_open()) {
        json j;
        // 2. Parse the file stream directly into the JSON object
        file >> j;
        
        // 3. Convert the JSON object back into your native C++ map
        details = j.get<str_dict>();
        
        file.close();
    } else {
        std::cerr << "Error: Could not open file for reading: " << path << std::endl;
    }
    
    return details;
};



struct _launcher_colors launcher_colors = {
    Color{190, 190, 190, 255},
    Color{54, 61, 74, 255},
    Color{77, 89, 153, 255},
    Color{119, 137, 237, 255},
    Color{255, 255, 255, 255},

}; 

void save_json(str path, str_dict details) {
    // 1. Open an output file stream
    std::ofstream file(path);
    
    if (file.is_open()) {
        // 2. Convert the map directly to a JSON object
        json j = details;
        
        // 3. Write it to the file with nice 4-space indentation (like Python's indent=4)
        file << j.dump(4); 
        
        file.close();
        std::cout << "Project file saved successfully!" << std::endl;
    } else {
        std::cerr << "Error: Could not open file for writing: " << path << std::endl;
    }
}

bool folder_exists(const std::string& path) {
    return std::filesystem::is_directory(path);
}

bool file_exists(const std::string& path) {
    return std::filesystem::exists(path);
}

void create_folder(const std::string& path) {
    std::filesystem::create_directory(path);
}
std::vector<str> list_folders(const std::string& path){
    std::vector<str> folders;
    for (const auto& entry : std::filesystem::directory_iterator(path)) {
        if (entry.is_directory()) {
            folders.push_back(entry.path().string());
        }
    }
    return folders;
}
