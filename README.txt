Task:
Implement a communication protocol to send and receive real time messages between client and server.

Protocol:
# The first element is the number of messages.
# The (2i)th element is the length of the ith message.
# The (2i + 1)th element is the ith message.
e.g. messages = [2, 10, 'Hi Fredrik', 14, 'This is Weiduo']
2 is the number of messages.
10 is the length of the first message 'Hi Fredrik'.
14 is the length of the second message 'This is Weiduo'.

How to start server:
python3 server.py

How to start client:
python3 client.py

How to test different use cases:
Modify the variable "message" in client.py