#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
     int i;
     int status;
     pid_t pid[3];
     for (i=0; i<3; i++)
     {
          pid[i] = fork();
          if (pid[i] == 0)
          {
               printf("Running gtk-demo with execl\n");
               execlp("./gtk-demo", "gtk-demo", 0);
               printf("Done!\n");
               break;
          }
     }
     wait(&status);
     return 0;
}
