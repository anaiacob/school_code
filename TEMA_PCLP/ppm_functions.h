#include <string.h>
#include <stdio.h>
#include <stdlib.h>

struct Pixel {
    unsigned char r, g, b;
};

typedef struct Pixel Pixel;

struct Image {
    int width;
    int height;
    Pixel** img;
};

typedef struct Image Image;

void load_ppm(char* file_name, FILE** load_file, Image* image);
void save_ppm(char* file_name, FILE** save_file, Image* image);
void free_image(Image* image);
void display_image_info(Image* image);
