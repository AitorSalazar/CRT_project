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

# Open SPI connection as a master
handle = pi.spi_open(SPI_CHANNEL, SPI_SPEED, SPI_FLAGS)

if handle < 0:
    print("Failed to open SPI connection.")
    pi.stop()
    exit()

try:
    while True:
        # Example: Send some data (4 bytes) every second
        # You can modify this part to send your actual data
        data_to_send = [0x01, 0x02, 0x03, 0x04]  # Example data
        count, data_received = pi.spi_xfer(handle, data_to_send)
        
        if count >= 0:
            # Data sent successfully
            print("Sent Data:", data_to_send)
        else:
            # Error sending data
            print("Error sending SPI data.")
        
        time.sleep(1)  # Wait for 1 second before sending again

except KeyboardInterrupt:
    print("\nScript stopped by the user.")

finally:
    # Close SPI handle and stop pigpio
    pi.spi_close(handle)
    pi.stop()
