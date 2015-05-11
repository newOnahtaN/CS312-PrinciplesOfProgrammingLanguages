all: openmp pthread

openmp:
	gcc openmp.c -std=gnu99 -fopenmp -lm -o openmp

pthread:
	gcc pthread.c -std=gnu99 -lpthread -lm -o pthread

clean:
	rm openmp pthread