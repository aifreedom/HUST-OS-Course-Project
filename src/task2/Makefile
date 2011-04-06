obj-m := aimod.o                   #要生成的模块名     
aimod-objs:= ai_driver.o        #生成这个模块名所需要的目标文件

KDIR := /lib/modules/`uname -r`/build
PWD := $(shell pwd)

all: task2 aimod.ko

aimod.ko:
	make -C $(KDIR) M=$(PWD) modules

clean:
	rm -rf *.o .*.cmd *.ko *.mod.c .tmp_versions *.symvers *.order task2

.PHONY: clean all