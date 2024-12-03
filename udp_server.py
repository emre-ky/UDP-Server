import socket

def start_udp_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    print(f"UDP Server Başlatıldı :  {ip}:{port}")
    
    while True:
        message, client_address = server_socket.recvfrom(1024)  # 1024 byte'lık mesaj al
        print(f"Mesaj Alındı : {message.decode()} from {client_address}")
        server_socket.sendto(f"Message received: {message.decode()}".encode(), client_address)

if __name__ == "__main__":
    ip = "127.0.0.1"  # Yerel IP adresi
    port = 8080        # Port numarası

    start_udp_server(ip, port)
