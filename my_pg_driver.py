import struct # module performs conversions between Python values and C structs
import io # tools for working with streams
import socket

# c - char (length - 1 byte), I - unsigned int  (length - 4 bytes)
format_for_packing = '!cI'
# Create C struct
pg_packet = struct.Struct(format_for_packing)

# Struct of message to PostgreSQL
# type_of_msg(b'Q') + (length of body + 4 bytes of length) + body + separator
# Q - query
def make_query_message(query: str, type_of_msg='Q'):
    separator = b'\0'
    # str.encode: str -> byte
    body_of_msg = query.encode() + separator
    # Create in-memory bytes buffer
    with io.BytesIO() as buff:
        # Return byte object
        pack = pg_packet.pack(type_of_msg.encode(), len(body_of_msg) + 4)
        # Write bytes to buffer
        buff.write(pack)
        buff.write(body_of_msg)
        # Return the entire contents of buffer
        return buff.getvalue()

HOST = 'localhost'
PORT = 5432
# Create a new socket object. A socket object represents one endpoint of a network connection.
# AF_INET - socket domains, SOCK_STREAM - socket types
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    # Connect the socket to a remote address (host, port)
    client.connect((HOST, PORT))
    # Send data
    authentication_message = b'authentication_message'
    client.send(authentication_message)
    # receive data
    print(client.recv(65535))
    for i in range(2):
        client.send(make_query_message(f'SELECT pf_sleep(5); SELECT {i}'))
    print(client.recv(65535))

a = make_query_message(f'SELECT pf_sleep(5); SELECT 1')
print(a)
