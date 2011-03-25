#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define BUF_LEN 80

int main(int argc, char *argv[])
{
     int i, num;
     char buf[BUF_LEN+10];
     
     /* Open the file */
     int dev = open("/dev/aimod", O_RDONLY);
     if (dev == -1)
          return dev;

     /* Read it and output it */
     read(dev, buf, BUF_LEN);
     for (i=0; i<BUF_LEN; i++)
          putchar(buf[i]);
     putchar('\n');

     /* Close the file */
     close(dev);     
     return 0;
}
