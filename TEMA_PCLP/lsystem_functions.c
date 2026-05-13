#include "lsystem_functions.h"

void load_lsystem_file(char* file_name, FILE** load_file, LSystem* lsystem)
{
    /*
        This function loads an L-system file.
        :params:
            file_name: name of the L-system file to load
            load_file: pointer to the FILE pointer for the L-system file
    */

    *load_file = fopen(file_name, "r");
    if (*load_file == NULL) {
        printf("Failed to load %s\n", file_name);
        return;
    }
    lsystem->axiom = (char*)malloc(sizeof(char));
    char character;
    int capacity = 0;
    int length = 0;
    while ((character = fgetc(*load_file)) != '\n' && character != EOF) {
        if (length + 1 >= capacity) {
            capacity += 16;
            char* temp = realloc(lsystem->axiom, capacity);
            if (temp == NULL) {
                printf("Error at allocation.\n");
                free(lsystem->axiom);
                return;
            }
            lsystem->axiom = temp;
        }
        lsystem->axiom[length++] = character;
    }
    lsystem->axiom[length] = '\0';
    // fscanf(*load_file, "%s\n", lsystem->axiom);
    fscanf(*load_file, "%d\n", &lsystem->rules_count);
    lsystem->simbols = (char*)malloc(lsystem->rules_count * sizeof(char));
    lsystem->succesors = (char**)malloc(lsystem->rules_count * sizeof(char*));
    for (int i = 0; i < lsystem->rules_count; i++) {
        lsystem->succesors[i] = (char*)malloc(sizeof(char));
        fscanf(*load_file, "%c\n", &lsystem->simbols[i]);
        capacity = 0;
        length = 0;
        while ((character = fgetc(*load_file)) != '\n' && character != EOF) {
            if (length + 1 >= capacity) {
                capacity += 16;
                char* temp = realloc(lsystem->succesors[i], capacity);
                if (temp == NULL) {
                    printf("Error at allocation.\n");
                    free(lsystem->succesors[i]);
                    return;
                }
                lsystem->succesors[i] = temp;
            }
            lsystem->succesors[i][length++] = character;
        }
        lsystem->succesors[i][length] = '\0';
    }
    printf("Loaded %s (L-system with %d rules)\n", file_name, lsystem->rules_count);
}

void free_lsystem(LSystem* lsystem)
{
    /*
        This function frees the memory allocated for the L-system.
        :params:
            lsystem: pointer to the LSystem structure
    */

    for (int i = 0; i < lsystem->rules_count; i++) {
        free(lsystem->succesors[i]);
    }
    free(lsystem->simbols);
    free(lsystem->succesors);
    free(lsystem->axiom);
}

void display_lsystem_info(LSystem* lsystem)
{
    /*
        This function displays information about the L-system.
        :params:
            lsystem: pointer to the LSystem structure
    */

    printf("Axiom: %s\n", lsystem->axiom);
    printf("Number of rules: %d\n", lsystem->rules_count);
    for (int i = 0; i < lsystem->rules_count; i++) {
        printf("Rule %d: %c -> %s\n", i + 1, lsystem->simbols[i], lsystem->succesors[i]);
    }
}

void derive_lsystem(LSystem* lsystem, int iterations, char** result, char* file_name)
{
    /*
        This function derives the L-system.
        :params:
            lsystem: pointer to the LSystem structure
            iterations: number of derivation iterations
            result: pointer to the string where the result will be stored
            file_name: name of the L-system file
    */
    if(file_name == NULL) {
        printf("No L-system loaded\n");
        exit(1);
    }
    else {
        if(iterations < 0) {
            exit(1);
        }
        else if(iterations == 0) {
            *result = (char*)malloc((strlen(lsystem->axiom) + 1) * sizeof(char));
            strcpy(*result, lsystem->axiom);
        }
        else {
            char* previous_derivation;
            previous_derivation = (char*)malloc((strlen(lsystem->axiom) + 1) * sizeof(char));
            strcpy(previous_derivation, lsystem->axiom);
            // printf("Previous derivation: %s\n", previous_derivation);
            char* current_derivation = NULL;
            for(int i = 0; i < iterations; i++) {
                current_derivation = (char*)malloc(sizeof(char));
                int length_current = 0;
                for(int j = 0; j < strlen(previous_derivation); j++) {
                    char current_symbol = previous_derivation[j];
                    // printf("Current symbol: %c\n", current_symbol);
                    int rule_found = 0;
                    for(int k = 0; k < lsystem->rules_count; k++) {
                        if(current_symbol == lsystem->simbols[k]) {
                            int length_succesor = strlen(lsystem->succesors[k]);
                            current_derivation = (char*)realloc(current_derivation, (length_current + length_succesor + 1) * sizeof(char));
                            strcpy(current_derivation + length_current, lsystem->succesors[k]);
                            // printf("Applied rule: %c -> %s\n", current_symbol, lsystem->succesors[k]);
                            // printf("Current derivation: %s\n", current_derivation);
                            length_current += length_succesor;
                            rule_found = 1;
                            break;
                        }
                    }
                    if(!rule_found) {
                        current_derivation = (char*)realloc(current_derivation, (length_current + 2) * sizeof(char));
                        current_derivation[length_current] = current_symbol;
                        // printf("No rule for symbol: %c, keeping it unchanged. %s\n", current_symbol, current_derivation);
                        length_current++;
                    }
                }
                free(previous_derivation);
                current_derivation[length_current] = '\0';
                previous_derivation = current_derivation;
            }
            *result = (char*)malloc((strlen(current_derivation) + 1) * sizeof(char));
            strcpy(*result, current_derivation);
            // printf("Final result after %d iterations: %s\n", iterations, *result);
            free(current_derivation);
        }
    }
}