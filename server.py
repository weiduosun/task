import socket
import struct
import _thread

# Build socket.
host_name = socket.gethostname()
print('host_name:', host_name)
host_ip = socket.gethostbyname(host_name)
host_port = 8181
print(host_ip, ':', host_port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host_ip, host_port))
s.listen()

print('\nServer started. Waiting for connection...\n')

# Handle the decoded data.
# Given: the decoded data from a client
# Return: the data for sending to the client
def handle_data(d):
    num_of_messages = int.from_bytes(d[0], byteorder='big')
    temp = []
    k = 1
    while k < 2 * num_of_messages + 1:
        k += 1
        message = ''
        for j in range(0, len(d[k])):
            message += str(d[k][j])
        temp.append(message)
        k += 1

    result = [num_of_messages.to_bytes(2, byteorder='big')]

    for j in range(0, len(temp)):
        result.append(len(str(temp[j])).to_bytes(2, byteorder='big'))
        result.append(temp[j].encode('utf_8'))

    return result

collection = []


# Decode the data from the client.
# Given: the data from the client
# Return: the decoded data
def decode_data(d):
    collection.append(d[0:2])
    t = struct.unpack('bb', d[0:2])
    num_of_messages = int.from_bytes(t, byteorder='big')
    index = 2
    for i in range(0, num_of_messages):
        collection.append(d[index:index + 2])
        len_of_string = int.from_bytes(d[index:index + 2], byteorder='big')
        index += 2
        collection.append(d[index: index + len_of_string].decode())
        index += len_of_string

# The buffer size of reading the bytes from the client.
bufsize = 16


# Decide if the server can stop receiving bytes.
# Given: the bytes from the client
# Return: true if the server can stop receiving bytes
def can_stop(d):
    t = struct.unpack('bb', d[0:2])
    num_of_messages = int.from_bytes(t, byteorder='big')
    index = 2
    p = 2
    n = len(d)
    for i in range(0, num_of_messages):
        p += 2
        if n < p:
            return False
        len_of_string = int.from_bytes(d[index:index + 2], byteorder='big')
        index += 2
        p += len_of_string
        if n < p:
            return False
        index += len_of_string
    return True

# read bytes.
# Given: the data packet
# Return: the data from the client
def read_bytes(s):
    temp = []
    while True:
        cur = s.recv(bufsize)
        temp.append(cur)
        if can_stop(b''.join(temp)):
            break

    result = b''.join(temp)
    return result

# A helper function to receive data from the client.
# Given: the data packet
def helper(conn):
    data = read_bytes(conn)
    print('Server received:', data)
    decode_data(data)
    response = b''.join(handle_data(collection))
    print('Server sent:', response)
    p = 0
    while p < len(response):
        conn.sendall(response[p:p+bufsize])
        p += bufsize


# Main function.
while True:
    conn, addr = s.accept()
    print('Server connected by', addr)
    _thread.start_new(helper, (conn,))
