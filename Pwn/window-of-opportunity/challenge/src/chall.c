#include <linux/init.h>   /* Needed for the macros */
#include <linux/kernel.h> /* Needed for KERN_INFO */
#include <linux/module.h> /* Needed by all modules */
#include <linux/printk.h>
#include <linux/slab.h>
#include <linux/types.h>
#include <linux/fs.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Eth007");
MODULE_DESCRIPTION("Often we look so long at the closed door that we do not see the one that has been opened for us.");

#define proc_name "window"

int Major_num;

int init_module(void);
void cleanup_module(void);
static int device_open(struct inode *filp, struct file *file);
int device_release(struct inode *inode, struct file *file);
long device_ioctl(struct file *, unsigned int, unsigned long);
ssize_t device_write(struct file *file, const char __user *buf, size_t count, loff_t *offset);

struct file_operations fops = {
  .open = device_open,
  .unlocked_ioctl = device_ioctl,
  .compat_ioctl = device_ioctl,
  .write = device_write,
  .release = device_release,
};

struct request {
  char* ptr;
  char buf[0x100];
};

int init_module(void) {
  Major_num = register_chrdev(0, proc_name, &fops);
  if (Major_num < 0) {
    printk(KERN_INFO "Failed to register device, major num returned %d", Major_num);
    return Major_num;
  }

  printk(KERN_INFO "Registered character device with major number %d", Major_num);
  printk(KERN_INFO "'mknod /dev/%s c %d 0'.\n", proc_name, Major_num);

  printk(KERN_INFO "Knock, and the door will be opened unto you.");
  return 0;
}

static int device_open(struct inode *inode_num, struct file *file) {
  file->private_data = ((void *)0);
  return 0;
}

int device_release(struct inode *inode, struct file *file) {
  return 1;
}

void cleanup_module(void){
  printk(KERN_INFO "When one door closes, another window opens.");
  unregister_chrdev(Major_num, proc_name);
}

long device_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
  struct request req;
  int res = 0;
  if (cmd == 0x1337) {
    res = copy_from_user(&req, (struct request*) arg, sizeof(struct request));
    res = _copy_to_user((char*)arg + sizeof(char*), req.ptr, 0x100);
    return res;
  }
  return -1;
}

ssize_t device_write(struct file *file, const char __user *buf, size_t count, loff_t *offset)
{
  int res;
  char a[64];
  res = _copy_from_user(a, buf, count);
  return 0;
}
