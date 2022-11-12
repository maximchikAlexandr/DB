import struct
import io # tools for working with streams
import socket


pg_packet = struct.Struct('!cI')

# encode: str -> byte
def make_query_message(query: str, magic='Q'):
    payload = query.encode() + b'\0'
    with io.BytesIO() as buff:
        buff.write(pg_packet.pack(magic.encode(), len(payload) + 4))
        buff.write(payload)
        return buff.getvalue()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 5432))
    # sock.send(...)
    print(sock.recv(65535))
    for i in range(2):
        sock.send(make_query_message(f'SELECT pf_sleep(5); SELECT {i}'))
    print(sock.recv(65535))
