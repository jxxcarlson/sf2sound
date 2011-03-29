/******************

 File: mix.c  -- ten channel mixer
 
 Usage: mix a.samp b.samp c.samp out.samp
 The files a.samp b.samp, c.samp are mixed,  
 the output is written to out.samp

 Purpose: Merge two audio sample files into one
 -- by adding values

*************/

#define MAXCHANELS 10 // of mixer
#define BUFFERSIZE 100

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

    FILE *infile[MAXCHANELS], *outfile;
    char line[MAXCHANELS][BUFFERSIZE];
    char *result[MAXCHANELS];
    char *tok;
    char *cmd;
    char *arg[MAXCHANELS]; // array of arguments
    int i;
    float maxAmplitude = 0.0;

    // Determine number of files to open -- 10 max
    
	int nFiles = argc - 2;
	if (nFiles > 10) {
		nFiles = 10;
	}
	
	// Open the files or report error
   	for (i = 0; i < nFiles; i++ ) {
    	if(  (infile[i] = fopen(argv[i+1], "r")) == NULL) {
      		printf("Error Opening Input File %d -- %s\n", i, argv[i+1]);
      		exit(1);
    	}
	}
    
    printf("Files opened: %d\n", nFiles);
    
    // open outfile
    if((outfile = fopen(argv[argc-1], "w")) == NULL) {
      printf("Error Opening Output File.\n");
      exit(1);
    } 
    
    // process each line of each file
    int scanning = 1;
    int lineCount = 0;
    while( scanning ) {
    	for (i = 0; i < nFiles; i++ ) {
    		char *result = fgets(line[i], sizeof(line[i]), infile[i]);
    		if (result == NULL) {
    			scanning = 0;
    		}  // if
    	} // for
    	if (scanning == 1) {
    		lineCount++;
    		double amplitude = 0.0;
    		for(i = 0; i < nFiles; i++) {
    			double sample = atof(line[i]);
    			amplitude +=sample;;
    		} //for
    		amplitude = amplitude/nFiles;
    		if (amplitude > maxAmplitude) {
    			maxAmplitude = amplitude;
    		}
        	fprintf(outfile,"%.8lf\n",amplitude);
    	} // if
    
    } // while
    printf("Lines processed: %d\n", lineCount);    
    // close the files
    for(i = 0; i < nFiles; i++) {
    	fclose(infile[i]);
    }
    fclose(outfile);
    printf("mix, maximum amplitude: %.2f\n", maxAmplitude);
   
}

// VOICES
