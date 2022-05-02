import os
from socket import SOCK_STREAM, socket, AF_INET
from http import HTTPStatus

HOST = "109.68.118.189"
PORT = 375


def getStatus(data):
    return data.split()[1].split("/?status=")


def getStatusCode(status):
    return int(status[1].split()[0])


with socket(AF_INET, SOCK_STREAM) as s:
    print(f"Server started on {HOST}:{PORT}, pid: {os.getpid()}")
    s.bind(('', PORT))
    s.listen(1)

    while True:
        print("Waiting for client request..")
        conn, address = s.accept()
        print("Connection from", address)

        data = conn.recv(1024)
        print(f"Received data: \n{data}\n")
        data = data.decode("utf-8").strip()

        status_value = 200
        status_phrase = "OK"
        try:
            status = getStatus(data)
            if len(status) == 2:
                status_code = getStatusCode(status)
                stat = HTTPStatus(status_code)
                status_value = status_code
                status_phrase = stat.phrase
        except (ValueError, IndexError):
            pass

        status_line = f"{data.split()[2]} {status_value} {status_phrase}"
        resp = "\r\n".join(data.split("\r\n")[1:])

        conn.send(f"{status_line}\r\n\r\n"
                  f"\nRequest Method: {data.split()[0]}"
                  f"\nRequest Source: {address}"
                  f"\nResponse Status: {status_value} {status_phrase}\r\n"
                  f"\n{resp}".encode("utf-8"))
        conn.close()
