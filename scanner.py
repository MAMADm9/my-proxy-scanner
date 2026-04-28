import asyncio
import socket
import random

# تنظیمات اصلی
TOTAL_PROXIES = 1000000  # تعداد پروکسی که می‌خواهی تولید و تست شود
CONCURRENT_TASKS = 500 # تعداد تست‌های همزمان (سرعت اسکن)
SERVER = 'panel.nirvana-smoke.com'
PORT = 8443

def generate_proxy():
    # تولید یوزرنیم تصادفی شبیه به مدل قبلی شما
    hex_chars = '0123456789abcdef'
    hex_str = ''.join(random.choice(hex_chars) for _ in range(18))
    user = f"Azir_{hex_str}"
    return f"https://t.me/socks?server={SERVER}&port={PORT}&user={user}&pass={user}"

async def check_proxy(proxy_url):
    try:
        # تست اتصال مستقیم به سرور و پورت
        conn = asyncio.open_connection(SERVER, PORT)
        reader, writer = await asyncio.wait_for(conn, timeout=5)
        writer.close()
        await writer.wait_closed()
        return proxy_url
    except:
        return None

async def main():
    print(f"Generating and scanning {TOTAL_PROXIES} proxies...")
    
    alive_proxies = []
    # تست کردن در دسته‌های ۵۰۰ تایی برای فشار نیامدن به شبکه
    for i in range(0, TOTAL_PROXIES, CONCURRENT_TASKS):
        batch = [generate_proxy() for _ in range(CONCURRENT_TASKS)]
        tasks = [check_proxy(url) for url in batch]
        results = await asyncio.gather(*tasks)
        
        # جدا کردن زنده‌ها
        found = [res for res in results if res]
        alive_proxies.extend(found)
        print(f"Processed {i + CONCURRENT_TASKS}... Found so far: {len(alive_proxies)}")

    # ذخیره نتایج
    with open('alive.txt', 'w') as f:
        for proxy in alive_proxies:
            f.write(proxy + '\n')
    
    print(f"Final: Found {len(alive_proxies)} alive proxies.")

if __name__ == "__main__":
    asyncio.run(main())
    
