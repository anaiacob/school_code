#include "bdf_functions.h"

int hex_to_decimal(char* hex_string)
{
    /*
        This function converts a hexadecimal string to its decimal equivalent.
        :params:
            hex_string: pointer to the hexadecimal string
        :return:
            decimal_value: the decimal equivalent of the hexadecimal string
    */

    int decimal_value = 0;
    int base = 1; // 16^0

    int length = strlen(hex_string);
    for(int i = length - 1; i >= 0; i--) {
        char current_char = hex_string[i];
        int current_value;

        if(current_char >= '0' && current_char <= '9') {
            current_value = current_char - '0';
        }
        else if(current_char >= 'A' && current_char <= 'F') {
            current_value = current_char - 'A' + 10;
        }
        else if(current_char >= 'a' && current_char <= 'f') {
            current_value = current_char - 'a' + 10;
        }
        else {
            continue; // Skip invalid characters
        }

        decimal_value += current_value * base;
        base *= 16;
    }

    return decimal_value;
}

void load_bdf(char* file_name_bdf, FILE** bdf_file, BDF* bdf)
{
    /*
        This function loads a BDF font file.
        :params:
            file_name_bdf: pointer to the name of the BDF file
            bdf_file: pointer to the FILE pointer of the BDF file
            bdf: pointer to the BDF structure where the font data will be stored
    */

    *bdf_file = fopen(file_name_bdf, "r");
    if(*bdf_file == NULL) {
        printf("Failed to load %s\n", file_name_bdf);
        exit(1);
    }
    else {
        char character;
        int capacity = 0;
        int length = 0;
        char* line = NULL;
        int number_of_characters = 0;
        int chars_index = 0;
        int check_bitmap = 0;
        while((character = fgetc(*bdf_file)) != EOF) {
            if(character == '\n' && line != NULL) {
                line[length] = '\0';
                // Process the line
                if(strncmp(line, "FONT ", 5) == 0) {
                    bdf->font_name = (char*)malloc((strlen(line) - 5 + 1) * sizeof(char));
                    strcpy(bdf->font_name, line + 5);
                    printf("Font name: %s\n", bdf->font_name);
                    bdf->font_name[strlen(line) - 5] = '\0';
                }
                else if(strncmp(line, "CHARS ", 6) == 0) {
                    // Process character data
                    number_of_characters = atoi(line + 6);
                    bdf->nr_characters = number_of_characters;
                    printf("Number of characters: %d\n", bdf->nr_characters);
                    bdf->characters = (char*)malloc((number_of_characters + 1) * sizeof(char));
                    printf("OK1\n");
                    bdf->dx = (int*)malloc(number_of_characters * sizeof(int));
                    printf("OK2\n");
                    bdf->dy = (int*)malloc(number_of_characters * sizeof(int));
                    printf("OK3\n");
                    bdf->bbw = (int*)malloc(number_of_characters * sizeof(int));
                    printf("OK4\n");
                    bdf->bbh = (int*)malloc(number_of_characters * sizeof(int));
                    printf("OK5\n");
                    bdf->bbxoff = (int*)malloc(number_of_characters * sizeof(int));
                    printf("OK6\n");
                    bdf->bbyoff = (int*)malloc(number_of_characters * sizeof(int));
                    printf("OK7\n");
                    bdf->bitmap = (int***)malloc(number_of_characters * sizeof(int**));
                    printf("OK8\n");
                }
                else if(strncmp(line, "STARTCHAR ", 10) == 0 && number_of_characters > 0) {
                    // Process each character
                    
                    number_of_characters--;
                    strcpy(bdf->characters + chars_index, line + 10);
                    chars_index++;
                    printf("Character: %c %d %d\n", bdf->characters[chars_index], number_of_characters, chars_index);

                }
                else if(strncmp(line, "DWIDTH ", 7) == 0) {
                    char *p = line;
                    char *end;
                    p += 7;

                    bdf->dx[chars_index] = strtol(p, &end, 10);
                    bdf->dy[chars_index] = strtol(end, &end, 10);
                    printf("  DWIDTH: (%d, %d)\n", bdf->dx[chars_index], bdf->dy[chars_index]);
                }
                else if(strncmp(line, "BBX ", 4) == 0) {
                    char *p = line;
                    char *end;
                    p += 4;

                    bdf->bbw[chars_index] = strtol(p, &end, 10);
                    bdf->bbh[chars_index] = strtol(end, &end, 10);
                    bdf->bbxoff[chars_index] = strtol(end, &end, 10);
                    bdf->bbyoff[chars_index] = strtol(end, &end, 10);
                    printf("  BBX: (width: %d, height: %d, xoff: %d, yoff: %d)\n",
                           bdf->bbw[chars_index], bdf->bbh[chars_index],
                           bdf->bbxoff[chars_index], bdf->bbyoff[chars_index]);
                }
                else if(strncmp(line, "BITMAP",6) == 0) {
                    check_bitmap = 1;
                }
                else if(strncmp(line, "ENDCHAR",7) == 0) {
                    check_bitmap = 0;
                }
                else if(check_bitmap == 1) {
                    // Process bitmap data
                    bdf->bitmap[chars_index] = (int**)malloc(bdf->bbh[chars_index] * sizeof(int*));
                    for(int i = 0; i < bdf->bbh[chars_index]; i++) {
                        bdf->bitmap[chars_index][i] = (int*)malloc(bdf->bbw[chars_index] * sizeof(int));
                        printf("  Reading BITMAP line %d for character %c: %s\n", i + 1, bdf->characters[chars_index], line);
                        int decimal_value = hex_to_decimal(line);
                        printf("    BITMAP line %d: hex %s -> decimal %d\n", i + 1, line, decimal_value);
                        for(int j = bdf->bbw[chars_index] - 1; j >= 0; j--) {
                            bdf->bitmap[chars_index][i][j] = decimal_value % 2;
                            decimal_value /= 2;
                        }
                    }
                }
                // Reset for next line
                free(line);
                line = NULL;
                capacity = 0;
                length = 0;
            }
            else if(character != '\n') {
                if(length + 1 >= capacity) {
                    capacity += 16;
                    char* temp = realloc(line, capacity);
                    if(temp == NULL) {
                        printf("Error at allocation.\n");
                        free(line);
                        return;
                    }
                    line = temp;
                }
                line[length++] = character;
            }
            else if(character == '\n' && line == NULL) {
                continue;
            }
        }
        bdf->characters[chars_index] = '\0';
        free(line);
        printf("Loaded %s (bitmap font %s)\n", file_name_bdf, bdf->font_name);
    }
}

void display_bdf_info(BDF* bdf)
{
    /*
        This function displays information about the BDF font.
        :params:
            bdf: pointer to the BDF structure
    */

    printf("Font Name: %s\n", bdf->font_name);
    printf("Characters:\n");
    for(int i = 0; i < bdf->nr_characters; i++) {
        printf("Character: %c\n", bdf->characters[i]);
        printf("  DWIDTH: (%d, %d)\n", bdf->dx[i], bdf->dy[i]);
        printf("  BBX: (width: %d, height: %d, xoff: %d, yoff: %d)\n",
               bdf->bbw[i], bdf->bbh[i], bdf->bbxoff[i], bdf->bbyoff[i]);
        printf("  BITMAP:\n");
        for(int j = 0; j < bdf->bbh[i]; j++) {
            for(int k = 0; k < bdf->bbw[i]; k++) {
                printf("%d", bdf->bitmap[i][j][k]);
            }
            printf("\n");
        }
    }
}

void free_bdf(BDF* bdf)
{
    /*
        This function frees the memory allocated for the BDF font.
        :params:
            bdf: pointer to the BDF structure
    */

    for (int i = 0; i < bdf->nr_characters; i++) {
        for (int j = 0; j < bdf->bbh[i]; j++) {
            free(bdf->bitmap[i][j]);   // int*
        }
        free(bdf->bitmap[i]);          // int**
    }
    free(bdf->bitmap);                 // int***
    // free(bdf->bitmap);
    printf("OKFREE3\n");
    free(bdf->dx);
    printf("OKFREE4\n");
    free(bdf->dy);
    printf("OKFREE5\n");
    free(bdf->bbw);
    printf("OKFREE6\n");
    free(bdf->bbh);
    printf("OKFREE7\n");
    free(bdf->bbxoff);
    printf("OKFREE8\n");
    free(bdf->bbyoff);
    printf("OKFREE9\n");
    free(bdf->characters);
    printf("OKFREE10\n");
    free(bdf->font_name);
    printf("OKFREE11\n");
}