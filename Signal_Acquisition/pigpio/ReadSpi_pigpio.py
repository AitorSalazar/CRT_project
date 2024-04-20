import pigpio
import time

# Configure the SPI settings
SPI_CHANNEL = 0  # SPI channel (0 or 1)
SPI_SPEED = 1000000  # SPI speed in Hz (1 MHz)
SPI_FLAGS = 0  # SPI flags (0 for default)

# Create a pigpio instance
pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit()

# Open SPI connection as a slave
handle = pi.spi_open(SPI_CHANNEL, SPI_SPEED, SPI_FLAGS)

if handle < 0:
    print("Failed to open SPI connection.")
    pi.stop()
    exit()

print("Listening for SPI data...")

try:
    while True:
        # Receive 4 bytes of data from the master
        # Adjust the number of bytes according to your transmitted data size
        # For example, if the master sends a single byte, use 1 instead of 4
        count, data = pi.spi_read(handle, 4)
        
        if count >= 0:
            # Data received successfully
            # Convert the received bytes to a list of integers

            for i in range(3):
                print(data[i])
            received_data = list(data)
            
            # Print the received data
            print("Received Data:", received_data)
        else:
            # Error receiving data
            print("Error receiving SPI data.")
        
        time.sleep(0.5)  # Wait for 1 second before the next read

except KeyboardInterrupt:
    print("\nScript stopped by the user.")

finally:
    # Close SPI handle and stop pigpio
    pi.spi_close(handle)
    pi.stop()
