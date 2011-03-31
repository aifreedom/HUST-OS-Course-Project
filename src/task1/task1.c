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
               execlp("./gtk-demo", "gtk-demo", NULL);
          else
               printf("Process %d: pid = %d\n", i,  pid[i]);
     }
     for (i=0; i<3; i++)
          wait(pid[i], &status, 0);
     return 0;
}
