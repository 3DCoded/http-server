SETUP
1. No setup required! 

USAGE
1. Import "server.py"
2. Use the Server() class. 
3. bind_addr((HOST, PORT))
4. bind('GET', GET)
5. bind accepts any valid http response type. 
6. bind sends a BaseHTTPRequestHandler object to your function. 
6. use run() to runserver
7. use close() close server
8. use unbind() to unbind server event
9. use reset() to reset server