import asyncio
import struct
 
async def custom_protocol_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
     
    # Prepare data: 4-byte length followed by the string
    test_str = "Hello, World!"
    data = struct.pack("!I", len(test_str)) + test_str.encode('utf-8')
     
    writer.write(data)
    await writer.drain()
     
    # Read echoed data
    received_data = await reader.read(100)
     
    # Close the connection
    writer.close()
    await writer.wait_closed()
 
    # Unpack received data
    str_len = struct.unpack("!I", received_data[:4])[0]
    received_str = received_data[4: 4 + str_len].decode('utf-8')
     
    print(f"Received echoed string: {received_str}")
 
async def main():
    await custom_protocol_client()
 
if __name__ == "__main__":
    asyncio.run(main())