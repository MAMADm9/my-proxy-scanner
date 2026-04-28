import asyncio
import socket
from urllib.parse import urlparse, parse_qs

async def check_proxy(proxy_url):
    try:
        # پاکسازی لینک برای استخراج آدرس
        clean_url = proxy_url.strip().replace('tg://', 'http://').replace('https://', 'http://')
        parsed = urlparse(clean_url)
        query = parse_qs(parsed.query)
        
        server = query.get('server', [None])[0]
        port_str = query.get('port', ['8443'])[0]
        port = int(port_str)

        if not server: return None

        # تست اتصال TCP (پینگ واقعی)
        conn = asyncio.open_connection(server, port)
        reader, writer = await asyncio.wait_for(conn, timeout=5)
        writer.close()
        await writer.wait_closed()
        return proxy_url
    except:
        return None

async def main():
    try:
        with open('proxies.txt', 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("فایل proxies.txt پیدا نشد!")
        return

    print(f"Starting scan for {len(urls)} proxies...")
    
    # اجرای اسکن به صورت موازی (Parallel)
    tasks = [check_proxy(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    alive_proxies = [res for res in results if res]
    
    with open('alive.txt', 'w') as f:
        for proxy in alive_proxies:
            f.write(proxy + '\n')
    
    print(f"Done! Found {len(alive_proxies)} alive proxies.")

if __name__ == "__main__":
    asyncio.run(main())
