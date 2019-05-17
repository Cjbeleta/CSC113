import socket
import sys

# server functions
def add(n1, n2):
	try:
		add = n1 + n2
		return 'OK %s \n' % str(add)
	except:
		return 'ERR Invalid arguments for ADD\n'

def sub(n1, n2):
	try:
		sub = n1 - n2
		return 'OK %s \n' % str(sub)
	except:
		return 'ERR Invalid arguments for SUB\n'

def mul(n1, n2):
	try:
		mul = n1 * n2
		return 'OK %s \n' % str(mul)
	except:
		return 'ERR Invalid arguments for ADD\n'

def div(n1, n2):
	try:
		if n2 == 0:
			return 'ERR Integer division by 0\n'
		else:
			div = n1 / n2
			return 'OK %s \n' % str(div)
	except:
		return 'ERR Invalid arguments for ADD\n'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('210.213.231.10', 14345)
print >> sys.stderr, 'Starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >> sys.stderr, 'Waiting for a connection...'
    connection, client_address = sock.accept()

    try:
        print >> sys.stderr, 'Connection from ', client_address
        # print >> sys.stderr, 'received "%s"' % data
        connection.sendall('OK Welcome to the Arithmetic Server \n')
        connection.sendall('>> ')
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(128)
            # if data is received, process it
            if data:

                # connection.sendall(data)

                params = data.split(' ')

                if params[0].upper() == 'QUIT\r\n':
                    connection.sendall('OK Goodbye \n')
                    break

                elif params[0].upper() == 'HELP\r\n' or params[0].upper() == 'HELP':

                    try:

                        if params[1].upper() == 'ADD\r\n':
                            connection.sendall('	= ADD <N1> <N2> - adds N1 and N2 \n')
                            connection.sendall('>> ')
                        elif params[1].upper() == 'SUB\r\n':
                            connection.sendall('	= SUB <N1> <N2> - subtracts N2 from N1 \n')
                            connection.sendall('>> ')
                        elif params[1].upper() == 'MUL\r\n':
                            connection.sendall('	= MUL <N1> <N2> - multiplies N1 and N2 \n')
                            connection.sendall('>> ')
                        elif params[1].upper() == 'DIV\r\n':
                            connection.sendall('	= DIV <N1> <N2> - divides N1 by N2 \n')
                            connection.sendall('>> ')
                        elif params[1].upper() == 'QUIT\r\n':
                            connection.sendall('	= QUIT - ends the current session of the arithmetic server \n')
                            connection.sendall('>> ')
                        else:
                            connection.sendall('ERR Invalid argument \n')
                            connection.sendall('>> ')

                    except:
                        connection.sendall('''
        The following commands are available:
                                
        ADD <N1> <N2> - adds N1 and N2
        SUB <N1> <N2> - subtracts N2 from N1
        MUL <N1> <N2> - multiplies N1 and N2
        DIV <N1> <N2> - divides N1 by N2
        HELP [command] - to display the syntax and semantics of a
                         specific command. If no command is specified, it will display all the
                         available commands and their meanings
        QUIT - to end the current session of the arithmetic server \n\n''')
                        connection.sendall('>> ')

                elif params[0].upper() == 'ADD':
                    try:
                    	msg = add(int(params[1]), int(params[2]))
                        connection.sendall(msg)
                        connection.sendall('>> ')
                    except:
                        connection.sendall('ERR Invalid number of arguments \n')
                        connection.sendall('>> ')

                elif params[0].upper() == 'SUB':
                    try:
                    	msg = sub(int(params[1]), int(params[2]))
                        connection.sendall(msg)
                        connection.sendall('>> ')
                    except:
                        connection.sendall('ERR Invalid number of arguments \n')
                        connection.sendall('>> ')

                elif params[0].upper() == 'MUL':
                    try:
                    	msg = mul(int(params[1]), int(params[2]))
                        connection.sendall(msg)
                        connection.sendall('>> ')
                    except:
                        connection.sendall('ERR Invalid number of arguments \n')
                        connection.sendall('>> ')

                elif params[0].upper() == 'DIV':
                    try:
                    	msg = div(int(params[1]), int(params[2]))
                        connection.sendall(msg)
                        connection.sendall('>> ')
                    except:
                        connection.sendall('ERR Invalid number of arguments \n')
                        connection.sendall('>> ')

                else:
                    connection.sendall('ERR Invalid command \n')
                    connection.sendall('>> ')

            else:

                print >> sys.stderr, 'No more data from ', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()