import socket
import struct
import pandas as pd

# Define the field structure
allData = [
    ("Packet Length", "I", 0, 4),
    ("Trading Symbol", "30s", 4, 30),
    ("Sequence Number", "q", 34, 8),
    ("Timestamp", "q", 42, 8),
    ("Last Traded Price (LTP)", "q", 50, 8),
    ("Last Traded Quantity", "q", 58, 8),
    ("Volume", "q", 66, 8),
    ("Bid Price", "q", 74, 8),
    ("Bid Quantity", "q", 82, 8),
    ("Ask Price", "q", 90, 8),
    ("Ask Quantity", "q", 98, 8),
    ("Open Interest (OI)", "q", 106, 8),
    ("Previous Close Price", "q", 114, 8),
    ("Previous Open Interest", "q", 122, 8)
]

SOCK_ADD = '0.0.0.0.0.0.0.1'  # Replace with the actual socket address
PORT = 5001  # Replace with the actual port number

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Send the data packet to the server
sock.connect(('127.0.0.1', PORT))
sock.send("working?".encode())

# Receive and process data continuously
data_dict = {}
while True:
    # Receive the packet length
    packet_length_data = sock.recv(4)
    packet_length = 130

    # Receive the complete packet
    packet_data = packet_length_data + sock.recv(packet_length - 4)

    # Process the packet and extract fields
    field_values = {}
    for field in allData[1:9]:  # Extracting the desired fields
        field_name, data_type, offset, length = field
        field_data = struct.unpack(data_type, packet_data[offset:offset+length])[0]

        # Decode the field data if it's a string
        if isinstance(field_data, bytes):
            field_data = field_data.decode().rstrip('\x00')

        field_values[field_name] = field_data

    # Check if trading symbol already exists in data_dict
    trading_symbol = field_values["Trading Symbol"]
    if trading_symbol in data_dict:
        # Update the existing entry
        data_dict[trading_symbol].update(field_values)
    else:
        # Add a new entry
        data_dict[trading_symbol] = field_values

    # Converting the dictionary to a DataFrame and storing the values and then converting to csv file
    df = pd.DataFrame(data_dict.values())
    df.to_csv('./flask1/output.csv', index=False)  

sock.close()