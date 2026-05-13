#include "turtle_functions.h"

void init_turtle(Turtle* turtle, char* command)
{
    /*
        This function initializes a Turtle structure based on the given command string.
        :params:
            turtle: pointer to the Turtle structure to be initialized
            command: command string containing the turtle parameters
    */

    int command_index = 0;

    // Parse command string to extract parameters
    // Example command format: "TURTLE 10 20 45 5 90 255 0 0"
    char* token = strtok(command, " ");
    while (token != NULL) {
        if(command_index == 1) {
            turtle->x_pos = atof(token);
        } else if(command_index == 2) {
            turtle->y_pos = atof(token);
        } else if(command_index == 3) {
            turtle->step_size = atof(token);
        } else if(command_index == 4) {
            turtle->turtle_orientation = atof(token);
        } else if(command_index == 5) {
            turtle->step_angle = atof(token);
        } else if(command_index == 6) {
            turtle->derivation = (int)atoi(token);
        } else if(command_index == 7) {
            turtle->pen_color.r = (unsigned char)atoi(token);
        } else if(command_index == 8) {
            turtle->pen_color.g = (unsigned char)atoi(token);
        } else if(command_index == 9) {
            turtle->pen_color.b = (unsigned char)atoi(token);
        }
        command_index++;
        token = strtok(NULL, " ");
    }
}

void display_turtle_info(Turtle* turtle)
{
    /*
        This function displays the information of a Turtle structure.
        :params:
            turtle: pointer to the Turtle structure
    */

    printf("Turtle Position: (%.2f, %.2f)\n", turtle->x_pos, turtle->y_pos);
    printf("Turtle Orientation: %.2f degrees\n", turtle->turtle_orientation);
    printf("Step Size: %.2f\n", turtle->step_size);
    printf("Step Angle: %.2f degrees\n", turtle->step_angle);
    printf("Derivation Level: %d\n", turtle->derivation);
    printf("Pen Color: (R: %d, G: %d, B: %d)\n", turtle->pen_color.r, turtle->pen_color.g, turtle->pen_color.b);
}

void add_state(State** stack, int* top, int x_pos, int y_pos, double orientation)
{
    /*
        This function adds a new state to the state stack.
        :params:
            stack: pointer to the stack of State structures
            top: pointer to the index of the top of the stack
            x_pos: x position of the turtle
            y_pos: y position of the turtle
            orientation: orientation of the turtle
    */
    (*top)++;
    *stack = realloc(*stack, (*top + 1) * sizeof(State));
    (*stack)[*top].x_pos = x_pos;
    (*stack)[*top].y_pos = y_pos;
    (*stack)[*top].turtle_orientation = orientation;
    // printf("State added to stack. New top index: %d\n", *top);
}

void get_state(State** stack, int* top, int* x_pos, int* y_pos, double* orientation)
{
    /*
        This function retrieves the top state from the state stack.
        :params:
            stack: pointer to the stack of State structures
            top: pointer to the index of the top of the stack
            x_pos: pointer to store the x position of the turtle
            y_pos: pointer to store the y position of the turtle
            orientation: pointer to store the orientation of the turtle
    */
    *x_pos = (*stack)[*top].x_pos;
    *y_pos = (*stack)[*top].y_pos;
    *orientation = (*stack)[*top].turtle_orientation;
}

void remove_state(int* top)
{
    /*
        This function removes the top state from the state stack.
        :params:
            top: pointer to the index of the top of the stack
    */
    if(*top < 0) {
        printf("State stack is empty.\n");
        return;
    }
    (*top)--;
}

void set_pixel(Image* image, int x, int y, Pixel color)
{
    /*
        This function sets the pixel at (x, y) in the image to the specified color.
        :params:
            image: pointer to the Image structure
            x: x coordinate of the pixel
            y: y coordinate of the pixel
            color: Pixel structure representing the color to set
    */

    if(x < 0 || x >= image->width || y < 0 || y >= image->height) {
        // printf("Pixel coordinates (%d, %d) are out of bounds.\n", x, y);
        x = (x < 0) ? 0 : (x >= image->width) ? image->width - 1 : x;
        y = (y < 0) ? 0 : (y >= image->height) ? image->height - 1 : y;
    }

    image->img[y][x] = color;
}

void draw_line(Image* image, double x_start, double y_start, double x_end, double y_end, Pixel color)
{
    /*
        This function draws a line on the image from (x_start, y_start) to (x_end, y_end) with the specified color.
        :params:
            image: pointer to the Image structure where drawing will occur
            x_start: starting x coordinate
            y_start: starting y coordinate
            x_end: ending x coordinate
            y_end: ending y coordinate
            color: Pixel structure representing the color of the line
    */

    int x0 = (int)(x_start);
    int y0 = (int)(y_start);
    int x1 = (int)(x_end);
    int y1 = (int)(y_end);

    int dx = abs(x1 - x0);
    int dy = abs(y1 - y0);
    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx - dy;

    while (1) {
        set_pixel(image, x0, y0, color);

        if (x0 == x1 && y0 == y1) break;
        int err2 = err * 2;
        if (err2 > -dy) {
            err -= dy;
            x0 += sx;
        }
        if (err2 < dx) {
            err += dx;
            y0 += sy;
        }
    }
}

void execute_turtle_command(Image* image, LSystem* lsystem, Turtle* turtle, char* file_name_ppm, char* file_name_lsystem)
{
    /*
        This function executes the turtle graphics commands to draw on the image based on the L-system.
        :params:
            image: pointer to the Image structure where drawing will occur
            lsystem: pointer to the LSystem structure containing the L-system rules
            turtle: pointer to the Turtle structure containing turtle parameters
    */

    if(file_name_ppm == NULL) {
        printf("No image loaded.\n");
        exit(1);
    }
    else if(file_name_lsystem == NULL) {
        printf("No L-system loaded.\n");
        exit(1);
    }
    else{
        // printf("Starting drawing with turtle graphics...\n");
        char* result_derivation = NULL;
        derive_lsystem(lsystem, turtle->derivation, &result_derivation, file_name_lsystem);
        // printf("L-system derived string: %s\n", result_derivation);
        State* state_stack = malloc(sizeof(State));
        int top = -1;
        int x = (int)(turtle->x_pos);
        int y = (int)(turtle->y_pos);
        double angle = turtle->turtle_orientation;
        for(long long i = 0; result_derivation[i] != '\0'; i++) {
            // printf("%lld %ld %c\n", i, strlen(result_derivation), result_derivation[i]);
            char command_turtle = result_derivation[i];
            if(command_turtle == 'F') {
                int new_x = x + (int)(turtle->step_size * cos(angle * PI / 180.0));
                int new_y = y + (int)(turtle->step_size * sin(angle * PI / 180.0));
                draw_line(image, x, y, new_x, new_y, turtle->pen_color);
                x = new_x;
                y = new_y;
            }
            else if(command_turtle == '+') {
                angle += turtle->step_angle;
            }
            else if(command_turtle == '-') {
                angle -= turtle->step_angle;
            }
            else if(command_turtle == '[') {
                add_state(&state_stack, &top, x, y, angle);
            }
            else if(command_turtle == ']' && top >= 0) {
                get_state(&state_stack, &top, &x, &y, &angle);
                remove_state(&top);
            }
            else continue;
        }
        printf("Drowing done.\n");
    }
}