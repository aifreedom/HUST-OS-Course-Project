#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utilities.h"
#include "vfs_struct.h"

void usage()
{
     /* printf("Usage: format [--bs] VDiskFile\n"); */
     printf("Usage: format VDiskFile\n");
     exit(-1);
}

void version()
{
     printf("VDisk format tool.\nAuthor: Xie Song <me@aifreedom.com>\n");
     exit(-1);
}

int vformat(int fd)
{
     int i, j;
     
     disk_metanode* disk_meta = (disk_metanode*)get_block(fd, 0);
     file_metanode* metanode;

     /* initialize disk metanode */
     disk_meta->dummy_head = METABLK_OFFSET + METABLK_COUNT;
     disk_meta->file_count = 0;
     free(disk_meta);
     disk_meta = NULL;

     for (i=METABLK_OFFSET; i<METABLK_OFFSET+METABLK_COUNT; i++) {
          file_metablk* metablk = (file_metablk*)get_block(fd, i);
          for (j=0; j<METANODE_COUNT; j++) {
               metablk->metanode[j].valid = FALSE;
          }
          write_block(fd, i, (void*)metablk);
          free(metablk);
     }

     for (i=REGULAR_OFFSET; i<BLK_COUNT; i++) {
          file_node* node = (file_node*)get_block(fd, i);
          node->next = i + 1;
          write_block(fd, i, (void*)node);
          free(node);
     }
}

int main(int argc, char *argv[])
{
     if (argc == 2) {
          if (strcmp(argv[1], "--help") == 0)
               usage();
          else if (strcmp(argv[1], "--version") == 0)
               version();
          else if (strstr(argv[1], "--") == argv[1]) {
               printf("vformat: no vdisk filename.\n");
               usage();
          }
          else {
               int fd = mount_disk(argv[1]);
               vformat(fd);
               unmount_disk(fd);
          }
     }
     /* else if (argc == 4) { */
     /* } */
     else {
          usage();
     }
     return 0;
}
