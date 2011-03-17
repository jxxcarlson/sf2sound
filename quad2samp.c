/******************

 File: quad.c
 Purpose: take file of quadruples (freq, dur, decay, amplitude) as input,
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

  2. Complie this file:

    % gcc quad.c -o quad

  3. Create a text file of the sampled waveform:

    % ./quad foo.quad

  4. Create the corresponding .wav file:

    % text2sf foo.samp foo.wav 44000 1 .90

  Here 44000 Hertz is the sample rate, 1 is the number
  of channels, and 0.90 is the gain.

  Note the output to the terminal window:

    TEXT2SF: convert text audio data to soundfile
    copying....
    Done. 132000 sample frames copied to foo.wav
    PEAK information:
    CH 1:0.8989 at 2.0006 secs

  The program text2sf (See: "The Audio Programming Book",
  Boulanger and Lazzarini, eds) has processed 132000 sample
  frames, which checks: 3.0 seconds of sound x 44,000 sample
  frames per second = 132,000 samples.

  Note that foo.samp is a 1.4 MB file, while foo.wav is a 
  260 K file.  So 0.47 MB/sec for foo.samp, 87 KB/sec for
  foo.wav.


  5.  Play the file:

    % play foo.wav

  (Mac: ) This command brings up the QuickTime player loaded with foo.wav.
  Click the pla button to listen to foo.wav.

 NOTE:  Since I am lazy, I usually package all of the above as follows:

 a.  Create a file m.sh with contents

   gcc quad.c -o quad
   ./quad foo.quad foo.samp
   text2sf foo.samp foo.wav 44000 1 .90
   rm foo.samp
   play foo.wav
  
 b.  Make an alias:

   % alias m 'sh m.sh'

 c.  Run the whole shebang:

  % m

 Thus when experimenting, I have only to type a single character to 
 test the each step.

*************/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


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
    float freq, dur, decay, amplitude;

    int srate = SRATE;
  
	int sr, nsamps, phase;
	double samp,k,a,x;
	double twopi = 2.0 * M_PI;
	double angleincr;
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
  
   float ATTACK = atof(argv[3]);
   float RELEASE = atof(argv[4]);
  
   phase = 0;
   while( fgets(line, sizeof(line), infile) != NULL ) {
     // Get each line from the infile 
     tok = strtok(line, " ");
    
     /*                    */ freq = atof(tok);
     tok = strtok(NULL, " "); dur = atof(tok);
     tok = strtok(NULL, " "); decay = atof(tok);
     tok = strtok(NULL, " "); amplitude = atof(tok);
     
     nsamps = (int)(dur * srate);
	 angleincr = twopi * freq / srate;
	 k = dur/nsamps;
	 a = exp(-k/decay);
	 x = 1.0;
	 
	 int i; // i is the local phase
	 float endAttack = ATTACK*nsamps;
	 float releaseSamples = RELEASE*nsamps;
	 float beginRelease = nsamps - releaseSamples;
	 
	 for( i = 0; i < nsamps; i++ ){
	    phase++;
	    float A, attackAmplitude, releaseAmplitude;
	    
	    if ( i < endAttack ) {
	       attackAmplitude = pow(i/endAttack, 2);
	     } else {
	       attackAmplitude = 1.0;
	    }
	    
	    if ( i > beginRelease ) {
	       float j = (nsamps - i)/(nsamps - beginRelease);
	       releaseAmplitude = pow(j, 2);
	     } else {
	       releaseAmplitude = 1.0;
	    }
	    
	    A = attackAmplitude*releaseAmplitude*amplitude;
	    
     	samp = A*sin(angleincr*phase);
		x *= a;
		samp *= x;       
		fprintf(outfile,"%.8lf\n",samp);		
	 }
  }
  // Close the files
  fclose(infile); 
  fclose(outfile);
}
