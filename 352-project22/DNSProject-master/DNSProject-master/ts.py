import threading
import socket
import sys

dns_table = {}

def get_table():
    with open('PROJI-DNSTS.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        items = line.split()
        dns_table[items[0]] = (items[1], items[2])


def server(listen_port):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created.")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', listen_port)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Received a connection request from a client at {}".format(addr))
    # returns

    while True:
        target_host = csockid.recv(200).decode('utf-8').rstrip()
        if target_host:
            if target_host not in dns_table:
                print("[S]: Hostname {} not found.".format(target_host))
                error_msg = target_host + " - Error:HOST NOT FOUND"
                csockid.send(error_msg.encode('utf-8'))
            else:
                print("[S]: Hostname {} found as {} {} {}".format(target_host, target_host, dns_table[target_host][0],
                                                                  dns_table[target_host][1]))
                ret_str = target_host + " " + dns_table[target_host][0] + " " + dns_table[target_host][1]
                csockid.send(ret_str.encode('utf-8'))
        else:
            print("[S]: No more hostnames to recieve.")
            break

    ss.close()
    exit()

if __name__ == '__main__':
    get_table()
    port = int(sys.argv[1])
    t1 = threading.Thread(name='server', target=server, args=[port])
    t1.start()
