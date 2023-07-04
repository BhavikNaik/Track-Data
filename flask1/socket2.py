import socket
import csv

# Socket configuration
socket_address = '0.0.0.0.0.0.0.1'  # Replace with the actual socket address
port = 9011  # Replace with the actual port number

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Send the data packet to the server
sock.connect(('127.0.0.1', port))
sock.send("Hello".encode())

# Create a CSV file and writer
csv_file = open('./output.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

# Write the CSV header
header = [
    'Trading Symbol',
    'Last Traded Price (LTP)',
    'Sequence Number',
    'Bid Price',
    'Bid Quantity',
    'Last Traded Quantity',
    'Timestamp',
    'Volume'
]
csv_writer.writerow(header)

try:
    while True:
        # Receive the packet data
        packet_data = sock.recv(130)

        # Extract field values from the packet data
        trading_symbol = packet_data[4:34].decode().rstrip('\x00')
        last_traded_price = int.from_bytes(packet_data[50:58], 'little')
        sequence_number = int.from_bytes(packet_data[34:42], 'little')
        bid_price = int.from_bytes(packet_data[74:82], 'little')
        bid_quantity = int.from_bytes(packet_data[82:90], 'little')
        last_traded_quantity = int.from_bytes(packet_data[58:66], 'little')
        timestamp = int.from_bytes(packet_data[42:50], 'little')
        volume = int.from_bytes(packet_data[66:74], 'little')

        # Write the field values to the CSV file
        csv_writer.writerow([
            trading_symbol,
            last_traded_price,
            sequence_number,
            bid_price,
            bid_quantity,
            last_traded_quantity,
            timestamp,
            volume
        ])

except KeyboardInterrupt:
    pass

finally:
    # Close the CSV file
    csv_file.close()

    # Close the socket
    sock.close()