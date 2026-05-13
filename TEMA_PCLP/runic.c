#include "general_functions.h"
// #include "ppm_functions.h"
// #include "lsystem_functions.h"
#include "turtle_functions.h"
#include "bdf_functions.h"

int main()
{
    char** commands = NULL;
    int nr_commands;
    int type_of_commands;
    FILE* load_file = NULL;
    FILE* save_file = NULL;
    char* file_name_ppm = NULL;
    char* file_name_lsystem = NULL;
    char* file_name_save_ppm = NULL;
    int lenght_file;
    Image image;
    FILE* lsystem_file = NULL;
    LSystem lsystem;
    int iterations;
    char* result = NULL;
    Turtle turtle;
    FILE* bdf_file = NULL;
    char* font_name = NULL;
    char* file_name_bdf = NULL;
    BDF bdf;

    commands = read_commands(&nr_commands);
    image.img = NULL;

    if(!commands) {
        printf("Error at read.\n");
        return 1;
    }
    printf("\n\n");
    for (int i = 0; i < nr_commands; i++) {
        printf("%s\n", commands[i]);
        if(strncmp(commands[i], "UNDO", 4) == 0) {
            // EXECUTE UNDO COMMAND
        }
        else if(strncmp(commands[i], "REDO", 4) == 0) {
            // EXECUTE REDO COMMAND
        }
        else if(strncmp(commands[i], "SAVE", 4) == 0) {
            if(check_command(commands[i]) == 1) {
                if(file_name_save_ppm != NULL) {
                    free(file_name_save_ppm);
                    file_name_save_ppm = NULL;
                    lenght_file = 0;
                }
                lenght_file = strlen(commands[i]) - 5;
                file_name_save_ppm = malloc(lenght_file * sizeof(char));
                strcpy(file_name_save_ppm, commands[i]+5);
                // printf("%d %s\n", lenght_file, file_name_save_ppm);
                save_ppm(file_name_save_ppm, &save_file, &image);
            }
            else {
                printf("Invalid command\n");
            }
        }
        else if(strncmp(commands[i], "LSYSTEM", 7) == 0) { // combinne with check_command
            // EXECUTE LSYSTEM COMMAND
            if(check_command(commands[i]) == 2) {
                if(file_name_lsystem != NULL) {
                    free(file_name_lsystem);
                    file_name_lsystem = NULL;
                    lenght_file = 0;
                    fclose(lsystem_file);
                }
                lenght_file = strlen(commands[i]) - 8;
                file_name_lsystem = malloc(lenght_file * sizeof(char));
                strcpy(file_name_lsystem, commands[i] + 8);
                printf("%d %s\n", lenght_file, file_name_lsystem);
                load_lsystem_file(file_name_lsystem, &lsystem_file, &lsystem);
                //display_lsystem_info(&lsystem);
            }
            else {
                printf("Invalid command\n");
            }
        }
        else if(strncmp(commands[i], "DERIVE", 6) == 0) {
            // EXECUTE DERIVE COMMAND
            if(check_command(commands[i]) == 3) {
                iterations = (int)strtol(commands[i] + 7, NULL, 10);
                // printf("Deriving L-system for %d iterations...\n", iterations);
                derive_lsystem(&lsystem, iterations, &result, file_name_lsystem);
                // printf("Result after %d iterations: %s\n", iterations, result);
            }

        }
        else if(strncmp(commands[i], "TURTLE", 6) == 0) {
            // EXECUTE TURTLE COMMAND
            if(check_command(commands[i]) == 4) {
                printf("Executing TURTLE command...\n");
                init_turtle(&turtle, commands[i]);
                display_turtle_info(&turtle);
                execute_turtle_command(&image, &lsystem, &turtle, file_name_ppm, file_name_lsystem);
                display_turtle_info(&turtle);
                // display_image_info(&image);
            }
        }
        else if(strncmp(commands[i], "LOAD", 4) == 0) {
            if(check_command(commands[i]) == 1) {
                if(file_name_ppm != NULL) {
                    free(file_name_ppm);
                    file_name_ppm = NULL;
                    lenght_file = 0;
                    fclose(load_file);
                }
                lenght_file = strlen(commands[i]) - 5;
                file_name_ppm = malloc(lenght_file * sizeof(char));
                strcpy(file_name_ppm, commands[i]+5);
                printf("%d %s\n", lenght_file, file_name_ppm);
                load_ppm(file_name_ppm, &load_file, &image);
                // display_image_info(&image);
            }
            else {
                printf("Invalid command\n");
            }
        }
        else if(strncmp(commands[i], "FONT", 4) == 0) {
            // EXECUTE FONT COMMAND
            if(check_command(commands[i]) == 5) {
                if(file_name_bdf != NULL) {
                    free(file_name_bdf);
                    file_name_bdf = NULL;
                    lenght_file = 0;
                    fclose(bdf_file);
                }
                lenght_file = strlen(commands[i]) - 5;
                file_name_bdf = malloc(lenght_file * sizeof(char));
                strcpy(file_name_bdf, commands[i]+5);
                printf("%d %s\n", lenght_file, file_name_bdf);
                load_bdf(file_name_bdf, &bdf_file, &bdf);
                display_bdf_info(&bdf);
                // load_bdf_file(file_name_bdf, &bdf_file);
                // display_bdf_info(&bdf);
            }
            else {
                printf("Invalid command\n");
            }
        }
        else if(strncmp(commands[i], "TYPE", 4) == 0) {
            // EXECUTE TYPE COMMAND
        }
        else if(strncmp(commands[i], "BYTECHECK", 9) == 0) {
            // EXECUTE BYTECHECK COMMAND
        }
        else {
            printf("Invalid command\n");
        }
    }

    for (int i = 0; i < nr_commands; i++) {
        free(commands[i]);
    }
    if(file_name_save_ppm != NULL) {
        free(file_name_save_ppm);
        printf("OK1\n");
    }
    if(file_name_lsystem != NULL) {
        free(file_name_lsystem);
        printf("OK2\n");
        fclose(lsystem_file);
        printf("OK3\n");
        free_lsystem(&lsystem);
        printf("OK3.5\n");
    }
    if(file_name_ppm != NULL) {
        free(file_name_ppm);
        printf("OK4\n");
        fclose(load_file);
        printf("OK5\n");
        free_image(&image);
        printf("OK6\n");
    }
    if(file_name_bdf != NULL) {
        free(file_name_bdf);
        printf("OK7\n");
        fclose(bdf_file);
        printf("OK8\n");
        free_bdf(&bdf);
        printf("OK9\n");
    }
    free(commands);
    return 0;
}