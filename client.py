import socket
import struct

# Build socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '192.168.86.31'
server_port = 8181
s.connect((server_ip, server_port))
print('Connected to server ', server_ip, ':', server_port)

# Messages that send to server.
# Modify this variable for testing different groups of messages.
# Protocal:
# The first element is the number of messages.
# The (2i)th element is the length of the ith message.
# The (2i + 1)th element is the ith message.
messages = [2, 10, 'Hi Fredrik', 14, 'This is Weiduo']

# The buffer size of reading bytes from the server.
bufsize = 16

collection = []

# Encode the message to bytes.
# Given: the message
# Return: the encoded bytes
def encode_data(d):
    num_of_answers = d[0]
    result = [num_of_answers.to_bytes(2, byteorder='big')]
    k = 1
    while k < 2 * num_of_answers + 1:
        result.append(d[k].to_bytes(2, byteorder='big'))
        k += 1
        expression = ''
        for j in range(0, len(d[k])):
            expression += str(d[k][j])
        result.append(expression.encode())
        k += 1

    return result


# Send messages to the server with limited buff size each time
# Given: the socket and by
def send_bytes_to_server(s, temp):
    index = 0
    while index <= len(temp):
        s.sendall(temp[index:index+bufsize])
        index += bufsize


# Decode data from the server
# Given: the bytes from the server
# Return: the decoded array
def decode_data(d):
    arr = []
    t = struct.unpack('bb', d[0:2])
    num_of_answers = int.from_bytes(t, byteorder='big')
    arr.append(num_of_answers)
    index = 2
    for i in range(0, num_of_answers):
        len_of_string = int.from_bytes(d[index:index + 2], byteorder='big')
        arr.append(len_of_string)
        index += 2
        arr.append(d[index: index + len_of_string].decode())
        index += len_of_string
    return arr


# Decide if the client can stop receiving bytes.
# Given: the bytes from the client
# Return: true if the client can stop receiving bytes
def can_stop(d):
    t = struct.unpack('bb', d[0:2])
    num_of_answers = int.from_bytes(t, byteorder='big')
    index = 2
    p = 2
    n = len(d)
    for i in range(0, num_of_answers):
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


# Read bytes.
# Given: the data packet
# Return: the data from the server
def read_bytes(s):
    temp = []
    while True:
        cur = s.recv(bufsize)
        temp.append(cur)
        if can_stop(b''.join(temp)):
            break

    result = b''.join(temp)
    return result


# Main function.
for line in messages:
    collection.append(line)
temp = b''.join(encode_data(collection))
print('Client sent:', temp)
send_bytes_to_server(s, temp)
data = read_bytes(s)
print('Client received:', data)
encoded_message = decode_data(data)
print('Client encoded:', encoded_message)

# Close socket to send EOF to server.
s.close()
