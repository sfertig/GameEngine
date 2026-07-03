
#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <vector>
#include <string>
#include <variant>
#include <unordered_map>
#include "raylib.h"

typedef std::string str;
typedef std::unordered_map<str, str> str_dict; 

void print_str(str s, bool nl = true);
void print_int(int i, bool nl = true);
void print_dict(str_dict d, bool nl = true);
void nl();

//dicts

extern std::unordered_map<str, Color> Colors;
extern str_dict newProjectDetails;
extern std::unordered_map<str, Color> recent_projects_dict;

//defines

struct _launcher_colors {
    Color launcher_bg;
    Color top_bar_bg;
    Color create_button_norm;
    Color create_button_hovered;
    Color create_button_text;
};
extern _launcher_colors launcher_colors;

//reading files (json as dict[str, str])
str_dict read_json(str path);
void save_json(str path, str_dict details);

#endif
