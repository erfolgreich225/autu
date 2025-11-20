import subprocess
import sys

def main():
    print("\033[94m[Manager] Bắt đầu chạy main.py\033[0m")
    process = subprocess.Popen([sys.executable, 'main.py'])
    print(f"\033[96m[Manager] Chờ main.py hoàn thành (PID: {process.pid})\033[0m")
    process.wait()
    print("\033[92m[Manager] main.py đã hoàn thành\033[0m")

    print("\033[94m[Manager] Bắt đầu chạy avai.py\033[0m")
    process2 = subprocess.Popen([sys.executable, 'avai.py'])
    print(f"\033[96m[Manager] Chờ avai.py hoàn thành (PID: {process2.pid})\033[0m")
    process2.wait()
    print("\033[92m[Manager] avai.py đã hoàn thành\033[0m")

if __name__ == "__main__":
    main()
