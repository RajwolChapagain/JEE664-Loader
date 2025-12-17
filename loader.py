import serial
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Path to the object file to be loaded')

args = parser.parse_args()

ser = serial.Serial(
    port='COM1',
    baudrate=9600,
    bytesize=8,
    parity='O',
    stopbits=2.0,
    timeout=1
)

if not ser.dsr:
    print('Error: Programmer not set to RS 232 Interface')
    ser.close()
    exit()

# Reset programmer to make it anticipate a control word next
ser.dtr = False
ser.dtr = True

with open(args.file, 'r') as f:
    line = f.readline()

    # Programmer expects 256 bytes of data after control word
    # After sending the 256 bytes of data, we need to send another control word for the next 256 bytes
    byte_count = 256

    # Set the address to F800 on the programmer (Specific to assembler and EPROM chip)
    next_address = 0xF800
    i = 0
    while line:
        if line.startswith('s1'):
            address = line[4:8]
            while (next_address != int(address, 16)):
                if byte_count == 256:
                    ser.write(b'\xAE')
                    byte_count = 0
                ser.write(bytes.fromhex('FF'))
                next_address += 1
                byte_count += 1
                
            data = line[8:-3]
            data_list = []
            cur = 0
            while cur < len(data):
                data_list.append(data[cur: cur+2])
                cur += 2

            for d in data_list:
                if byte_count == 256:
                    ser.write(b'\xAE')
                    byte_count = 0
                ser.write(bytes.fromhex(d))
                byte_count += 1

            num_bytes_in_line = int(line[2:4], 16) - 3 # Subtract by 3 to account for 2 address bytes and 1 checksum byte at the end
            next_address = int(address, 16) + num_bytes_in_line
            print(hex(next_address))
            i += 1
            
        line = f.readline()

ser.close()
