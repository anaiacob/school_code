#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct BDF {
    char* font_name;
    int* dx;
    int* dy;
    int* bbw;
    int* bbh;
    int* bbxoff;
    int* bbyoff;
    char* characters;
    int*** bitmap;
    int nr_characters;
};

typedef struct BDF BDF;

void load_bdf(char* file_name_bdf, FILE** bdf_file, BDF* bdf);
int hex_to_decimal(char* hex_string);
void display_bdf_info(BDF* bdf);
void free_bdf(BDF* bdf);
