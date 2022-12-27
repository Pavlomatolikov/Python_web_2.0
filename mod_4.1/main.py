import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
from _datetime import datetime
import json
import threading

UDP_IP = '127.0.0.1'
UDP_PORT = 5000


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        # print(1, data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        # print(2, data_parse)
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        # print(3, data_dict)
        message = {str(datetime.now()): data_dict}
        # print(4, message)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        run_client(UDP_IP, UDP_PORT, message)
        # print(5, "message udp sent")

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f'Received data: {data.decode()} from: {address}')
            with open("storage\\data.json", "r") as read_file:
                info = json.load(read_file)
                data_to_append = json.loads(data.decode())
                info.update(data_to_append)
            with open("storage\\data.json", "w") as write_file:
                json.dump(info, write_file)
            sock.sendto("OK".encode(), address)
            print(f'Send data: "OK" to: {address}')

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


def run_client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    message = json.dumps(message).encode()
    sock.sendto(message, server)
    print(f'Send data: {message} to server: {server}')
    response, address = sock.recvfrom(1024)
    print(f'Response data: {response.decode()} from address: {address}')
    sock.close()


if __name__ == '__main__':
    http_server = threading.Thread(target=run)
    socket_server = threading.Thread(target=run_server, args=(UDP_IP, UDP_PORT))

    http_server.start()
    socket_server.start()
    http_server.join()
    socket_server.join()
    print('Done!')
