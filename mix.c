/******************

 File: mix.c

 Purpose: Merge two audio sample files into one

*************/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Strip trailing newline
void stripnl(char *str) {
  while(strlen(str) && ( (str[strlen(str) - 1] == 13) || 
       ( str[strlen(str) - 1] == 10 ))) {
    str[strlen(str) - 1] = 0;
  }
}
 

#ifndef M_PI
#define M_PI (3.141592654)
#endif

#define SRATE 44100

int main(int argc, char **argv) {

    FILE *infile1, *infile2, *outfile;
    char line1[100], line2[100];
    char *tok;
    char *cmd;
    char *arg[10]; // array of arguments

     // Open infile1.  If NULL is returned there was an error
    if((infile1 = fopen(argv[1], "r")) == NULL) {
      printf("Error Opening Input File 1.\n");
      exit(1);
    } 

     // Open infile2.  If NULL is returned there was an error
    if((infile2 = fopen(argv[2], "r")) == NULL) {
      printf("Error Opening Input File 2.\n");
      exit(1);
    } 

    // Open outfile.  If NULL is returned there was an error 
    if((outfile = fopen(argv[3], "w")) == NULL) {
      printf("Error Opening Output File.\n");
      exit(1);
    } 

    int scanning = 1;
    int lineCount = 0;
    while( scanning ) {

     // Get each line from the infile 

      char *result1 = fgets(line1, sizeof(line1), infile1);
      char *result2 = fgets(line2, sizeof(line2), infile2);
      if ((result1 != NULL) && (result2 != NULL)) {
	scanning = 1;
	lineCount++;
      } else {
	scanning = 0;
      }
    }
  
  // Close the files
  fclose(infile1); 
  fclose(infile2); 
  fclose(outfile);

  printf("line count = %d\n", lineCount);
}

// X1
