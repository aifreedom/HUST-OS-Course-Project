#ifndef _UTILITIES_H
#define _UTILITIES_H

#include "vfs_struct.h"

int mount_disk(const char diskname[]);
void* get_block(int fd, int blk_number);
int write_block(int fd, int block_number, void* block_ptr);
file_metanode* file_find(int fd, const char filename[]);
int unmount_disk(int fd);

#endif
