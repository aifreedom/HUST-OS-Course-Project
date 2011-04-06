#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "vfs_struct.h"

int mount_disk(const char diskname[])
{
     int ret = open(diskname, O_RDWR);
     if (ret != 0)
     {
          printf("vdisk: disk ``%s'' not found!\n", diskname);
          exit(ret);
     }
}

void* get_block(int fd, int blk_number)
{
     void* ret = malloc(BLK_SIZE);
     lseek(fd, blk_number*BLK_SIZE, SEEK_SET);
     read(fd, ret, BLK_SIZE);
     return ret;
}

int write_block(int fd, int blk_number, void* blk_ptr)
{
     if (!blk_ptr)
          return -1;
     lseek(fd, blk_number*BLK_SIZE, SEEK_SET);
     write(fd, blk_ptr, BLK_SIZE);
     return 0;
}

file_metanode* file_find(int fd, const char filename[])
{
     int i, j;
     file_metanode* ret = NULL;
     for (i=METABLK_OFFSET;
          i<METABLK_COUNT+METABLK_OFFSET;
          i++) {
          file_metablk* metablk = (file_metablk*)get_block(fd, i);
          for (j=0; j<METANODE_COUNT; j++) {
               if (metablk->metanode[j].valid
                   && strcmp(filename, metablk->metanode[j].filename) == 0)
               {
                    ret = malloc(sizeof(file_metanode));
                    memcpy(ret, (metablk->metanode)+j, sizeof(file_metanode));
                    free(metablk);
                    return ret;
               }
          }
          free(metablk);
     }
     return ret;
}

int unmount_disk(int fd)
{
     return close(fd);
}
