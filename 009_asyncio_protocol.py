import asyncio
 
class EchoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
 
    def data_received(self, data):
        self.transport.write(data)
 
async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(EchoProtocol, '127.0.0.1', 8888)
    await server.serve_forever()
 
if __name__ == "__main__":
    asyncio.run(main())