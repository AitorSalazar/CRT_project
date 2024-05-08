#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#define MEMORY_NAME "/shm_temp_humidity"
#define MEMORY_SIZE 2048

int main() {
    // Open the shared memory object
    int shm_fd = shm_open(MEMORY_NAME, O_RDONLY, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(EXIT_FAILURE);
    }

    // Map the shared memory object into process address space
    void* ptr = mmap(NULL, MEMORY_SIZE, PROT_READ, MAP_SHARED, shm_fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    // Read integers from shared memory
    int* shared_data = (int*)ptr;
    for (int i = 0; i < 3; ++i) {
        printf("Value at index %d: %d\n", i, shared_data[i]);
    }

    // Unmap the shared memory
    if (munmap(ptr, MEMORY_SIZE) == -1) {
        perror("munmap");
        exit(EXIT_FAILURE);
    }

    // Close the shared memory object
    if (close(shm_fd) == -1) {
        perror("close");
        exit(EXIT_FAILURE);
    }

    return 0;
}
