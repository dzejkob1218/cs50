// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize scale infile outfile\n");
        return 1;
    }

    float scale = atof(argv[1]);

    if (scale <= 0.0 || scale > 100.0)
    {

        fprintf(stderr, "Enter integer between 1 and 100\n");
        return 2;
    }

printf("%f\n", scale);

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);


    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }


    //get props of infile
    int inWidth = bi.biWidth;
    int inHeight = bi.biHeight;
    int inlineleng = bi.biWidth * sizeof(RGBTRIPLE);
    int inPadding = (4 - (inWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    //DOUBLE
    bi.biWidth *=scale;
    bi.biHeight *=scale;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);



    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

 float yscanOffset = 0.0; //Represents the 'debt' the scanline accumullates due to fractions' difference in pixel count

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(inHeight); i < biHeight; i++)
    {
 yscanOffset += scale;

    if (yscanOffset >= 1.0) {

        float xscanOffset = 0.0; //Represents the 'debt' the scanline accumullates due to fractions' difference in pixel count
        nextline:
        // iterate over pixels in scanline
        for (int j = 0; j < inWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            //ADD SCAN OFFSET
            xscanOffset += scale;

            // write RGB triple to outfile
           while (xscanOffset >= 1.0)
        {   fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            xscanOffset -= 1.0;
        }

        }
        // then add padding
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, outptr);
        }

        //go back
        yscanOffset--;
        if (yscanOffset >= 1) {fseek(inptr, (-1 * inlineleng), SEEK_CUR); goto nextline;}

}

else {

 fseek(inptr, (inWidth * sizeof(RGBTRIPLE)), SEEK_CUR);


}



        // skip over infiles padding, if any
        fseek(inptr, inPadding, SEEK_CUR);


    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
