#include "ppm_functions.h"

void load_ppm(char* file_name, FILE** load_file, Image* image)
{
    /*
        This function loads the information from the ppm file into memory.
        :params:
            file_name: the filename extracted from the load command
            load_file: the file in which the information will be read
        :return: None
    */
    char image_format[3];
    int max_val;

    *load_file = fopen(file_name, "rb");

    if(*load_file == NULL) {
        printf("Failed to load %s\n", file_name);
        exit(1);
    }

    fscanf(*load_file, "%2s", image_format);

    if(strcmp(image_format, "P6") != 0) {
        printf("Failed to load %s\n", file_name);
        fclose(*load_file);
        exit(1);
    }

    fscanf(*load_file, "%d %d", &image->width, &image->height);
    fscanf(*load_file, "%d", &max_val);
    fgetc(*load_file);

    image->img = (Pixel**)malloc(image->height * sizeof(Pixel*));
    if(!image->img) {
        printf("Failed to load %s\n", file_name);
        fclose(*load_file);
        exit(1);
    }

    for(int i= image->height - 1; i >= 0; i--) {
        image->img[i] = (Pixel*)malloc(image->width * sizeof(Pixel));
        if(!image->img[i]) {
            fclose(*load_file);
            printf("Failed to load %s\n", file_name);
            exit(1);
        }
        fread(image->img[i], sizeof(Pixel), image->width, *load_file);
    }

    printf("Loaded %s (PPM image %dx%d)\n", file_name, image->width, image->height);

}

void save_ppm(char* file_name, FILE** save_file, Image* image)
{
    /*
        This function saves the information from memory into a ppm file.
        :params:
            file_name: the filename extracted from the save command
            save_file: the file in which the information will be written
        :return: None
    */
    if(image->img == NULL) {
        printf("No image loaded\n");
        exit(1);
    }
    else {
        *save_file = fopen(file_name, "wb");

        if(!save_file) {
            printf("No image loaded\n");
            exit(1);
        }

        fprintf(*save_file, "P6\n");
        fprintf(*save_file, "%d %d\n", image->width, image->height);
        fprintf(*save_file, "255\n");

        for(int i= image->height - 1; i >= 0; i--) {
            fwrite(image->img[i], sizeof(Pixel), image->width, *save_file);
        }

        printf("Saved %s\n", file_name);
        fclose(*save_file);
    }
    
}

void free_image(Image* image)
{
    /*
        This function frees the memory allocated for the image.
        :params:
            image: pointer to the Image structure
        :return: None
    */

    for(int i=0; i< image->height; i++) {
        free(image->img[i]);
    }
    free(image->img);
}

void display_image_info(Image* image)
{
    /*
        This function displays the information of the image.
        :params:
            image: pointer to the Image structure
        :return: None
    */

    printf("Image width: %d\n", image->width);
    printf("Image height: %d\n", image->height);
    for(int i=0; i< image->height; i++) {
        printf("Row %d: ", i);
        for(int j=0; j< image->width; j++) {
            printf("(%3u,%3u,%3u) ", (unsigned)image->img[i][j].r, (unsigned)image->img[i][j].g, (unsigned)image->img[i][j].b);
        }
        printf("\n");
    }
}