CC = gcc

all: task1 gtk-demo

gtk-demo: gtk-demo.c
	gcc `pkg-config --cflags --libs gtk+-2.0` $^ -o $@

clean:
	rm task1 gtk-demo

.PHONY: clean all