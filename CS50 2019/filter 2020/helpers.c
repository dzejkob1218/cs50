#include <stdio.h>
#include  <stdlib.h>
#include <math.h>
 #include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++){
        for (int x = 0; x < width; x++){
            RGBTRIPLE pixel = image[y][x];
            int avg = (pixel.r + pixel.g + pixel.b) / 3;
            pixel.r = pixel.g = pixel.b = avg;
            image[y][x] = pixel;
        }
    }


    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE mirror[height][width];

    for (int y = 0; y < height; y++){
        for (int x = 0; x < width; x++){
            mirror[y][x] = image[y][width - x];
        }
    }
    //actually replace pixels
    for (int y = 0; y < height; y++){
        for (int x = 0; x < width; x++){
            image[y][x] = mirror[y][x];
        }
    }

}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    // Allocate memory
    RGBTRIPLE(*avgs)[width] = calloc(height, width * sizeof(RGBTRIPLE));

    for (int y = 0; y < height; y++){
        for (int x = 0; x < width; x++){
            float avgR  = 0.0, avgG  = 0.0, avgB = 0.0;
            float avg_pixels = 0.0; // might not always be 9 at edges
            // go through neighbours
            for (int ay = -1; ay < 2; ay++){
                for (int ax = -1; ax < 2; ax++){
                    // check if within bounds
                    if ((x+ax) > 0 && (x+ax) < width && (y+ay) > 0 && (y+ay) < height){
                        avg_pixels++;
                        avgR += image[y+ay][x+ax].r;
                        avgG += image[y+ay][x+ax].g;
                        avgB += image[y+ay][x+ax].b;
                    }
                }
            }

            // calculate averages
            avgR = avgR / avg_pixels;
            avgG = avgG / avg_pixels;
            avgB = avgB / avg_pixels;

            avgs[y][x].r = (int)avgR;
            avgs[y][x].g = (int)avgG;
            avgs[y][x].b = (int)avgB;

    }

    }

                //actually replace pixels
             for (int y2 = 0; y2 < height; y2++){
                for (int x2 = 0; x2 < width; x2++){
                  image[y2][x2] = avgs[y2][x2];
                 }
            }

    return;
}


int clamp(int in){
    if (in > 255) return 255;
    if (in < 0) return 0;
    return in;

}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{

        // Allocate memory
    RGBTRIPLE(*avgs)[width] = calloc(height, width * sizeof(RGBTRIPLE));

    for (int y = 0; y < height; y++){
        for (int x = 0; x < width; x++){

            int xR  = 0.0, xG  = 0.0, xB = 0.0;
            int yR  = 0.0, yG  = 0.0, yB = 0.0;

            // go through neighbours
            for (int ay = -1; ay < 2; ay++){
                for (int ax = -1; ax < 2; ax++){
                    // check if within bounds
                    if ((x+ax) > 0 && (x+ax) < width && (y+ay) > 0 && (y+ay) < height){
                        int weigth = ax;
                        if (ay == 0) {weigth *= 2;}
                       //printf("[%i,%i],%i || ",ax,ay,weigth);
                        xR += image[y+ay][x+ax].r * weigth;
                        xG += image[y+ay][x+ax].g * weigth;
                        xB += image[y+ay][x+ax].b * weigth;
                        weigth = ay;
                        if (ax == 0) {weigth *= 2;}
                        yR += image[y+ay][x+ax].r * weigth;
                        yG += image[y+ay][x+ax].g * weigth;
                        yB += image[y+ay][x+ax].b * weigth;
                    }
                }
            }


            int avgR  = 0.0, avgG  = 0.0, avgB = 0.0;
            avgR = sqrt((xR * xR) + (yR * yR));
            avgB = sqrt((xB * xB) + (yB * yB));
            avgG = sqrt((xG * xG) + (yG * yG));
            // cap results
            avgR = clamp(avgR);
            avgG = clamp(avgG);
            avgB = clamp(avgB);
   // printf("\n");
            avgs[y][x].r = avgR;
            avgs[y][x].g = avgG;
            avgs[y][x].b = avgB;

    }
     //   printf("LINE");
    }

                //actually replace pixels
             for (int y2 = 0; y2 < height; y2++){
                for (int x2 = 0; x2 < width; x2++){
                  image[y2][x2] = avgs[y2][x2];
                 }
            }

    return;
}
