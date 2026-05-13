#include <string.h>
#include <stdio.h>
#include <stdlib.h>

struct LSystem {
    char* axiom;
    int rules_count;
    char* simbols;
    char** succesors;
};
typedef struct LSystem LSystem;

void load_lsystem_file(char* file_name, FILE** load_file, LSystem* lsystem);
void free_lsystem(LSystem* lsystem);
void display_lsystem_info(LSystem* lsystem);
void derive_lsystem(LSystem* lsystem, int iterations, char** result, char* file_name);