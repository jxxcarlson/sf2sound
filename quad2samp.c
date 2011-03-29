/******************

 File: quad2samp.c
 Purpose: take file of quadruples (freq, dur, decay, amplitude) as input,ff
 produce file of sampled waveform as output

 Example:

 1. Create file "foo.quad" with contents

     220 1.0 0.5 0.2
     330 1.0 0.5 0.5
     440 1.0 0.5 1.0

  Here 220 is the frequency of the first sound in Hertz, 1.0
  is the duration in seconds, 0.5 is the decay constant (larger
  for more sustained sound, smaller for more percussive sound),
  and 0.2 is the amplitude (larger = louder, smaller = quieter).

  2. Compile this file:

    % gcc quad2samp.c -o quad2samp

  3. Create a text file of the sampled waveform:

    % ./quad2samp foo.quad foo.samp

  4. Create the corresponding .wav file:

    % text2sf foo.samp foo.wav 44100 1 0.90

  Here 44100 Hertz is the sample rate, 1 is the number
  of channels, and 0.90 is the gain.

 
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

    FILE *infile, *outfile;
    char line[100];
    char *tok;
    char *cmd;
    char *arg[10]; // array of arguments
    int nHarmonics;
    float harmonicAmplitude[8]; 
    float freq, dur, decay, amplitude;
    float ATTACK, RELEASE;

    int srate = SRATE;
  
	int sr, nsamps, phase;
	double samp,k,a,x;
	double twopi = 2.0 * M_PI;
	double W;
	double maxsamp = 0.0;


     // Open infile.  If NULL is returned there was an error
    if((infile = fopen(argv[1], "r")) == NULL) {
      printf("Error Opening Input Fle.\n");
      exit(1);
    } 

    // Open outfile.  If NULL is returned there was an error 
    if((outfile = fopen(argv[2], "w")) == NULL) {
      printf("Error Opening Output File.\n");
      exit(1);
    } 
  
   phase = 0; // global phase -- runs from start to finish of waveform
   while( fgets(line, sizeof(line), infile) != NULL ) {
   
     // Get each line from the infile 
     if (line[0] == '@') {
     
        // parse:
     	tok = strtok(line, ":\n"); cmd = tok;
     	
     	// execute
     	if (strcmp(cmd,"@attack") == 0) {
     	  arg[0] = strtok(NULL, ":\n");
     	  ATTACK = atof(arg[0]);
     	  printf("ATTACK: %.4f\n", ATTACK);
     	}
     	
     	if (strcmp(cmd,"@release") == 0) {
     	  arg[0] = strtok(NULL, ":\n");
     	  RELEASE = atof(arg[0]);
     	  printf("RELEASE: %.4f\n", RELEASE);
     	}
     	
     	if (strcmp(cmd,"@harmonics") == 0) {
     	    
     	  	int scanning = 1;
     	  	nHarmonics = 0;
     	  	while( scanning ){
     	    	tok = strtok(NULL, ":");
     	    	if (tok == NULL) {
     	      		scanning = 0;
     	     	} else {
     	    		harmonicAmplitude[nHarmonics] = atof(tok);
     	    		nHarmonics++;
     	    	} // else
     	  	} // while
     	  	printf("harmonics:\n");
     	  	int i;
     	  	for (i = 0; i < nHarmonics; i++) {
     	  		printf("   %d: %.4f\n", i, harmonicAmplitude[i]);
     	  	}
     	} // if (strcmp(cmd,"@harmonics") == 0) 
     } else { // if line[0] != '@'
		
		// Parse the line to recover the elements
		// of tuple as floats
		 tok = strtok(line, " "); freq = atof(tok);
		 tok = strtok(NULL, " "); dur = atof(tok);
		 tok = strtok(NULL, " "); amplitude = atof(tok);
		 tok = strtok(NULL, " "); decay = atof(tok);
		 
		 // Set up parameters
		 nsamps = (int)(dur * srate);
		 W = twopi * freq / srate;
		 k = dur/nsamps;
		 float dampingFactor = exp(-k/decay);
		 float dampingAmplitude = 1.0;
		 
		 int i; // local phase - use for a single tuple
		 
		 // Parameters for basic waveform shaping
		 float endAttack = ATTACK*nsamps;
		 float releaseSamples = RELEASE*nsamps;
		 float beginRelease = nsamps - releaseSamples;
		 
		 for( i = 0; i < nsamps; i++ ){
			phase++;
			float A, attackAmplitude, releaseAmplitude;
			
			// Compute attack amplitude
			if ( i < endAttack ) {
			   attackAmplitude = pow(i/endAttack, 2);
			 } else {
			   attackAmplitude = 1.0;
			}
			
			 // Compute release amplitude
			if ( i > beginRelease ) {
			   float j = (nsamps - i)/(nsamps - beginRelease);
			   releaseAmplitude = pow(j, 2);
			 } else {
			   releaseAmplitude = 1.0;
			}
			
			// Update dampingAmplitude
			dampingAmplitude = dampingAmplitude*dampingFactor;
			
			// Final amplitude is a product of amplitudes
			A = attackAmplitude*releaseAmplitude*dampingAmplitude*amplitude;
			
			// Form the sine wave and add harmonics to it
			int k;
			for (k = 0; k < nHarmonics; k++) {
			 	samp = harmonicAmplitude[k]*sin(W*(k+1)*phase);
			}
			// Shape the wave
			samp *= A;
			
	
			// Write the sample to file      
			fprintf(outfile,"%.8lf\n",samp);		
		 }
	 }
  }
  
  // Close the files
  fclose(infile); 
  fclose(outfile);
}

// X1
