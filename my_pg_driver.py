import struct # module performs conversions between Python values and C structs
import io # tools for working with streams
import socket

# Create C struct
pg_packet = struct.Struct('!cI')

def make_query_message(query: str, magic='Q'):
    # encode: str -> byte
    payload = query.encode() + b'\0'
    # Create in-memory bytes buffer
    with io.BytesIO() as buff:
        # Return byte object
        pack = pg_packet.pack(magic.encode(), len(payload) + 4)
        # Write bytes to buffer
        buff.write(pack)
        buff.write(payload)
        # Return the entire contents of buffer
        return buff.getvalue()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 5432))
    sock.send(...)
    print(sock.recv(65535))
    for i in range(2):
        sock.send(make_query_message(f'SELECT pf_sleep(5); SELECT {i}'))
    print(sock.recv(65535))

a= make_query_message(f'SELECT pf_sleep(5); SELECT 1')
print(a)
