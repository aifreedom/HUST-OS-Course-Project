#ifndef _VFS_STRUCT_H
#define _VFS_STRUCT_H

#ifndef BOOL
#define BOOL char
#endif

#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

#define BLK_SIZE 512
#define BLK_COUNT 204800

#define NAME_LENGTH 8 /* the lenght of filename */
#define METABLK_COUNT 10 /* the number of  */
#define METABLK_OFFSET 1 /* the first file_metablk */
#define REGULAR_OFFSET (METABLK_OFFSET+METABLK_COUNT)

#define METANODE_COUNT (BLK_SIZE/sizeof(file_metanode))
/* the number of nodes in one file_metablk */


typedef struct {
     int dummy_head;
     int file_count;
} disk_metanode;

typedef struct {
     BOOL valid;
     char filename[NAME_LENGTH];
     int head;
} file_metanode;

typedef struct {
     file_metanode metanode[METANODE_COUNT];
} file_metablk;

typedef struct {
     int length;
     char content[BLK_SIZE - 2*sizeof(int)];
     int next;
} file_node;
     

#endif
