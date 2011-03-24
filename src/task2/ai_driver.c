/* Project: OS Course Project */
/* Author:  Xie Song <me@aifreedom.com> */
/* Date:    March 24, 2011 */
/* Remarks: A driver for a pseudo character device, outputing numbers
 *          continuously */

#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <asm/uaccess.h>

#define DEVICE_NAME "aimod"
#define BUF_LEN 300
#define SUCCESS 0

MODULE_AUTHOR("Xie Song <me@aifreedom.com>");
MODULE_LICENSE("GPLv3"); 

/* Declare file operation functions */
static int ai_open(struct inode *inode, struct file *file);
static int ai_release(struct inode *inode, struct file *file);
static ssize_t ai_read(struct file *filp, char *buffer,
                           size_t length, loff_t * offset);
static ssize_t ai_write(struct file *filp, const char *buff,
                        size_t len, loff_t * off);

static struct file_operations ai_fops = {
     .owner    =    THIS_MODULE,
     .open     =    ai_open,
     .release  =    ai_release,
     .read     =    ai_read,
     .write    =    ai_write,
};

static int major;
static int next = 0;
static int Device_Open = 0;
static size_t buf_len = 0;

static char buf[BUF_LEN+15]; // for convenience in generate()
static char *buf_ptr = buf;

static int __init ai_init(void)
{
     major = register_chrdev(0, DEVICE_NAME, &ai_fops);
     if (major < 0) {
          printk(KERN_ALERT "%s: Registering char device failed with %d\n", DEVICE_NAME, major);
          return major;
     }

     printk(KERN_INFO "%s: %s was assigned major number %d.\n", DEVICE_NAME, DEVICE_NAME, major);
     printk(KERN_INFO "%s: To talk to the driver, create a dev file with 'mknod /dev/%s c %d 0'.\n", DEVICE_NAME, DEVICE_NAME, major);
     printk(KERN_INFO "%s: Remove the device file and module when done.\n", DEVICE_NAME);

     return SUCCESS;     
}

static void __exit ai_exit(void)
{
     unregister_chrdev(major, DEVICE_NAME);
     printk(KERN_ALERT "%s: %s has been unregistered\n", DEVICE_NAME, DEVICE_NAME);
}

static int ai_open(struct inode *inode, struct file *file)
{
	if (Device_Open)
		return -EBUSY;

	Device_Open++;
	printk(KERN_ALERT "%s: Device opened.\n", DEVICE_NAME);

	try_module_get(THIS_MODULE);

	return SUCCESS;
}

static void generate(void)
{
     char* p = buf;
     int last_put;
     printk(KERN_INFO "%s: generate starts with next=%d, buf_len=%d, buf_ptr-buf=%d.\n",
            DEVICE_NAME, next, buf_len, buf_ptr - buf);
     buf_len = 0;
     while (buf_len < BUF_LEN) {
          last_put = sprintf(p, "%d\n", next++);
          buf_len += last_put;
          p += last_put;
     }
     if (buf_len >= BUF_LEN) {
          buf_len -= last_put;
          next--;
     }
     // buf[buf_len++] = '\0';
     buf_ptr = buf;
     printk(KERN_INFO "%s: generate ends with next=%d, buf_len=%d, buf_ptr-buf=%d.\n",
            DEVICE_NAME, next, buf_len, buf_ptr - buf);
}

static ssize_t ai_read(struct file *filp, char *buffer,
                           size_t length, loff_t * offset)
{
     int bytes_read = 0;
     int i;
     printk(KERN_INFO "%s: read --- ", DEVICE_NAME);
     for (i=0; i<buf_len; i++)
          printk(KERN_INFO "%c", buf[i]);
     printk(KERN_INFO "\n");
     while (length) {
          if (buf_ptr - buf >= buf_len)
               generate();
          
          put_user(*(buf_ptr++), buffer++);

          length--;
          bytes_read++;
     }

     return bytes_read;
}

static int ai_release(struct inode *inode, struct file *file)
{
	Device_Open--;		/* We're now ready for our next caller */

	module_put(THIS_MODULE);

    printk(KERN_ALERT "%s: Device released.\n", DEVICE_NAME);
	return 0;
}


static ssize_t
ai_write(struct file *filp, const char *buff, size_t len, loff_t * off)
{
     printk(KERN_ALERT "%s: Sorry, this operation isn't supported.\n",
            DEVICE_NAME);
     return -EINVAL;
}

module_init(ai_init);
module_exit(ai_exit);
