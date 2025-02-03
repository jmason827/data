#!/usr/bin/env python3
import asyncio
import urllib.parse

async def send_request(func, data):
    host, port = '127.0.0.1', 8642
    reader, writer = await asyncio.open_connection(host, port)
    url = f"/api/{func}?data={urllib.parse.quote(data)}"
    req = (
        f"GET {url} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    writer.write(req.encode())
    await writer.drain()
    # Read entire response until EOF
    resp = await reader.read()
    print(f"[{func}] {data} ->\n{resp.decode()}\n")
    writer.close()
    await writer.wait_closed()

async def interactive_client():
    loop = asyncio.get_running_loop()
    print("Interactive Test Client (no aiohttp)")
    print("Enter commands in the format: <f1|f2|f3> <data>")
    print("Type 'quit' or 'exit' to finish.\n")
    while True:
        # Read input in a thread so we don't block the event loop.
        cmd = await loop.run_in_executor(None, input, ">> ")
        if cmd.strip().lower() in {"quit", "exit"}:
            break
        parts = cmd.split(maxsplit=1)
        if not parts or parts[0] not in {"f1", "f2", "f3"}:
            print("Invalid command. Try: f1, f2, or f3 followed by data.")
            continue
        func = parts[0]
        data = parts[1] if len(parts) > 1 else ""
        # Schedule the request concurrently.
        asyncio.create_task(send_request(func, data))

async def main():
    await interactive_client()

if __name__ == '__main__':
    asyncio.run(main())
