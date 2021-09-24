#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;


int main(int argc, char *argv[])
{

if (argc != 2){
    printf("Usage: recover file\n");
    return 1;
}

FILE *file = fopen(argv[1], "r");

if (file == NULL) {
    printf("Couldn't open file\n");
    return 2;
}
/*
// Define struct
typedef struct
{
unsigned char byte[512];
} JPEGBLOCK;

//Temporary storage;
JPEGBLOCK block;*/

BYTE block[512];
int jpegcount = 0;
empty:

fread(&block, 512, 1, file);

if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0 ) {

    goto jpegs;

} else {

    goto empty;
}

jpegs:

if (jpegcount > 100) goto end;
char newname[12];
sprintf(newname,"%i%i%i.jpg",(jpegcount/100),(jpegcount % 100)/10, (jpegcount % 10));
FILE *output = fopen(newname, "w");

while (1){
//WRITE TO NEW FILE
fwrite(&block, 512, 1, output);

//READ BLOCK FROM FILE
if (fread(&block, 512, 1, file)!=1) {goto end;}

//CHECK IF NEW JPEG STARTED
if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0 ) {
    jpegcount++;
    goto jpegs;}
}



end:
fclose (file);
fclose (output);

return 0;
}



