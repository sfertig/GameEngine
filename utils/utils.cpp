#include "utils.h"
#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <unordered_map>
#include <fstream>
#include "json.hpp"

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

void nl() {
    std::cout << std::endl;
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




