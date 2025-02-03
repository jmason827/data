import asyncio, urllib.parse

# --- Business Functions ---
async def f1(data): 
    await asyncio.sleep(1)
    return f"Result of f1 with {data}"
async def f2(data): 
    await asyncio.sleep(0.5)
    return f"Result of f2 with {data}"
async def f3(data): 
    await asyncio.sleep(8)
    return f"Result of f3 with {data}"

# --- Request Manager ---
class RequestManager:
    def __init__(self):
        self.req_id = 0
        self.pending = {}

    async def dispatch(self, req_id, fn, data):
        print(f"DISP.{req_id}")
        try:
            result = await fn(data)
        except Exception as e:
            print(f"ERROR in DISP.{req_id}: {e}")
            fut = self.pending.pop(req_id, None)
            if fut:
                fut.set_exception(e)
            return
        print(f"RECV.{req_id}")
        fut = self.pending.pop(req_id, None)
        if fut:
            fut.set_result(result)

    async def process_request(self, fn, data):
        self.req_id += 1
        req_id = self.req_id
        print(f"REQ.{req_id}")
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self.pending[req_id] = fut
        asyncio.create_task(self.dispatch(req_id, fn, data))
        result = await fut
        print(f"RESP.{req_id}: {result}")
        return result

mgr = RequestManager()
funcs = { '/api/f1': f1, '/api/f2': f2, '/api/f3': f3 }

# --- Minimal HTTP Server Handler ---
async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        data = await reader.readuntil(b'\r\n')
    except asyncio.IncompleteReadError:
        writer.close()
        await writer.wait_closed()
        return

    parts = data.decode().strip().split()
    print(f'parts={parts}')
    if len(parts) < 3:
        writer.close()
        await writer.wait_closed()
        return

    method, path, _ = parts
    if method != "GET":
        writer.write(b"HTTP/1.1 405 Method Not Allowed\r\nContent-Length: 0\r\n\r\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    parsed = urllib.parse.urlparse(path)
    fn = funcs.get(parsed.path)
    if not fn:
        writer.write(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    query = urllib.parse.parse_qs(parsed.query)
    req_data = query.get('data', [''])[0]
    try:
        result = await mgr.process_request(fn, req_data)
    except Exception as e:
        body = f"Error: {e}".encode()
        hdr = f"HTTP/1.1 500 Internal Server Error\r\nContent-Length: {len(body)}\r\n\r\n".encode()
        writer.write(hdr + body)
    else:
        body = result.encode()
        hdr = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Content-Type: text/plain\r\n\r\n"
        ).encode()
        writer.write(hdr + body)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    srv = await asyncio.start_server(handle_client, '127.0.0.1', 8642)
    print("Serving on", ", ".join(str(sock.getsockname()) for sock in srv.sockets))
    async with srv:
        await srv.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
