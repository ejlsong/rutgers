import threading
import sys
import socket



def client(rs_host, rs_port, ts_port):
    try:
        rs_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: RS socket created.")
    except socket.error as err:
        print('RS socket open error: {} \n'.format(err))
        exit()

    rs_ip = socket.gethostbyname(rs_host)
    rs_server_binding = (rs_ip, rs_port)
    rs_sock.connect(rs_server_binding)
    print("[C]: RS server connection established.")

    ts_ip = None
    ts_sock = None

    with open('PROJI-HNS.txt', 'r') as in_file:
        lines = in_file.readlines()

    out = open('RESOLVED.txt', 'w')

    for line in lines:
        host_name = line.lower()
        rs_sock.send(host_name.encode('utf-8'))
        print("[C]: Sending RS hostname {}.".format(host_name.rstrip()))
        rcv = rs_sock.recv(200).decode('utf-8')
        print("[C]: Received {} from RS.".format(rcv.rstrip()))
        items = rcv.split()
        if items[2] == 'A':
            out.write("{}\n".format(rcv))
            print("[C]: Writing {} to file.".format(rcv.rstrip()))
        elif items[2] == 'NS':
            print("[C]: Hostname not found in RS.")
            try:
                if ts_sock is None:
                    ts_ip = socket.gethostbyname(items[0])
                    ts_server_binding = (ts_ip, ts_port)
                    ts_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ts_sock.connect(ts_server_binding)
                    print("[C]: TS server connection established.")
            except socket.error as err:
                print("TS socket open error: {}\n".format(err))
                exit()
            ts_sock.send(host_name.encode('utf-8'))
            print("[C]: Sending TS hostname {}.".format(host_name.rstrip()))
            ts_rcv = ts_sock.recv(200).decode('utf-8')
            print("[C]: Received {} from TS.".format(ts_rcv.rstrip()))
            out.write("{}\n".format(ts_rcv))

    rs_sock.close()
    ts_sock.close()
    exit()

if __name__ == '__main__':
    rs_name = sys.argv[1]
    port_rs = int(sys.argv[2])
    port_ts = int(sys.argv[3])
    t1 = threading.Thread(name='client', target=client, args=[rs_name, port_rs, port_ts])
    t1.start()
