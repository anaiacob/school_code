#include "general_functions.h"

char** read_commands(int* nr_commands)
{
    /*
        This function reads commands from stdin until the entrence is EXIT.
        :params: 
            nr_commands: pointer used to return the number of commands read
        :return:
            commands: pointer to a dynamically allocated array of strings
    */

    char** commands = NULL;
    *nr_commands = 0;

    while (1) {
        char* command = NULL;
        char character;
        int capacity = 0;
        int length_command = 0;

        while ((character = getchar()) != '\n' && character != EOF) {

            if (length_command + 1 >= capacity) {
                capacity += 16;
                char* temp = realloc(command, capacity);
                if (temp == NULL) {
                    printf("Error at allocation.\n");
                    free(command);
                    return commands;
                }
                command = temp;
            }

            command[length_command++] = character;
        }

        if (command == NULL)
            continue;

        command[length_command] = '\0';

        if (strcmp(command, "EXIT") == 0) {
            free(command);
            break;
        }

        char** temp_commands = realloc(commands, (*nr_commands + 1) * sizeof(char*));

        if (temp_commands == NULL) {
            printf("Error at reallocation!\n");
            free(command);
            return commands;
        }

        commands = temp_commands;
        commands[*nr_commands] = malloc(strlen(command) + 1);

        if (commands[*nr_commands] == NULL) {
            printf("ERROR at allocation.\n");
            free(command);
            return commands;
        }

        strcpy(commands[*nr_commands], command);
        (*nr_commands)++;
        free(command);
    }

    return commands;
}

int check_command(char* command)
{
    /*
        This function checks if the structure of the load command or save command is correct.
        :params:
            command: a pointer to a string which is a load command or a save command
        :return:
            0 -> if the command is not written correctly
            1 -> if the command is written correctly
    */

    int lenght_command = strlen(command);
    if(lenght_command > 4 && strncmp(command + lenght_command - 4, ".ppm", 4) == 0) {
        return 1;
    }
    else if(lenght_command > 8 && strncmp(command + lenght_command - 5, ".lsys", 5) == 0) {
        return 2;
    }
    else if(strncmp(command, "DERIVE", 6) == 0) {
        for(int i = 8; i < lenght_command; i++) {
            if(command[i] < '0' || command[i] > '9') {
                return 0;
            }
        }

        return 3;
    }
    else if(strncmp(command, "TURTLE", 6) == 0) {
        int space_count = 0;
        for(int i = 7; i < lenght_command; i++) {
            if(command[i] == ' ' && i != 7) {
                space_count++;
            }
            else if((command[i] < '0' || command[i] > '9') && command[i] != '.' && command[i] != '-') {
                return 0;
            }
        }
        if(space_count != 8) {
            return 0;
        }
        return 4;
    }
    else if(lenght_command > 4 && strncmp(command + lenght_command - 4, ".bdf", 4) == 0) {
        return 5;
    }
    else {
        return 0;
    }
}

// void undo_command(Image* image)
// {
//     // This function executes the UNDO command

// }

// void redo_command(Image* image)
// {
//     // This function executes the REDO command

// }