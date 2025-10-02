import asyncio
import struct
 
class CustomProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
 
    def data_received(self, data):
        parsed_data = self.parse_custom_protocol(data)
        self.transport.write(parsed_data)
 
    def parse_custom_protocol(self, data):
        # Unpack a 4-byte integer from the beginning of data
        str_len = struct.unpack("!I", data[:4])[0]
         
        # Extract the string of the given length
        received_str = data[4: 4 + str_len].decode('utf-8')
         
        print(f"Received string: {received_str}")
         
        # For demonstration, just echo back the received string
        return data
 
async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(CustomProtocol, '127.0.0.1', 8888)
    await server.serve_forever()
 
if __name__ == "__main__":
    asyncio.run(main())