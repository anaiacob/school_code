#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "ppm_functions.h"
#include "lsystem_functions.h"
#define PI 3.14159265

struct Turtle {
    double x_pos;
    double y_pos;
    double turtle_orientation;
    double step_size;
    double step_angle;
    int derivation;
    Pixel pen_color;
};

typedef struct Turtle Turtle;

struct  State {
    double x_pos;
    double y_pos;
    double turtle_orientation;
};
typedef struct State State;

void init_turtle(Turtle* turtle, char* command);
void display_turtle_info(Turtle* turtle);
void execute_turtle_command(Image* image, LSystem* lsystem, Turtle* turtle, char* file_name_ppm, char* file_name_lsystem);
void add_state(State** stack, int* top, int x_pos, int y_pos, double orientation);
void get_state(State** stack, int* top, int* x_pos, int* y_pos, double* orientation);
void remove_state(int* top);
void set_pixel(Image* image, int x, int y, Pixel color);
void draw_line(Image* image, double x_start, double y_start, double x_end, double y_end, Pixel color);
