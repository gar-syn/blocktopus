import asyncio
import signal
import logging
from concurrent.futures import ThreadPoolExecutor

"""
A server for passing on real-time data from CGQuant via TCP.
Requirements: Python 3.8 only
On the computer that is running the CGQuant software, run:
python server.py
to start the server. Use Ctrl+C to stop it, or close the command prompt.
Ensure that CGQuant is started before starting the server.
Make sure the server is stopped before closing CGQuant.
In octopus, use the Aquila CGQ machine block with the CGQ (tcp) connection block.
"""

HOST = '0.0.0.0'
PORT = 8082
PIPE_FILE = r'\\.\pipe\CGQuantDataPipe'

clients = set()

class PipeReader ():
    def __init__ (self, pipe):
        self.running = False
        self.pipe = pipe
        self.pool = ThreadPoolExecutor(1)

    def read_pipe (self):
        i = 0

        with open(self.pipe, 'r') as f:
            while self.running:
                line = f.readline()

                ## Uncomment for debugging
                ## Cycle Input number:
                # line = line[0:35] + str(i % 3) + line[36:]
                # i += 1
                ## Change Base number:
                # line = line[0:25] + '1' + line[26:]

                for client in clients:
                    client.transport.write(line.encode('utf-8'))
                
                print(f"-> {line:39.39}... ({len(clients)} clients)")
    
    def run (self):
        loop = asyncio.get_running_loop()
        self.running = True
        self._thread = loop.run_in_executor(self.pool, self.read_pipe)

        def report_error (future):
            if future.exception():
                print (future.exception())
        
        self._thread.add_done_callback(report_error)
    
    def cancel (self):
        self.running = False
    
    async def wait_cancel (self):
        self.cancel()
        await self._thread


class StreamPipeDataProtocol (asyncio.Protocol):
    def connection_made(self, transport):
        print ('client connected')
        self.transport = transport
        clients.add(self)

    def data_received(self, data):
        print('received', data)

    def connection_lost (self, reason):
        print('disconnected')
        clients.remove(self)


async def main(host, port):
    loop = asyncio.get_running_loop()

    pipe = PipeReader(PIPE_FILE)
    pipe.run()

    server = await loop.create_server(StreamPipeDataProtocol, host, port)
    
    async def shutdown(*args):
        """Cleanup tasks tied to the service's shutdown."""
        logging.info("Stopping server pipe")
        await server.wait_closed()

        logging.info("Closing pipe")
        await pipe.wait_cancel()

    try:
        await server.serve_forever()
    except asyncio.exceptions.CancelledError:
        pass
    finally:
        await shutdown()


loop = asyncio.get_event_loop()

try:
    logging.info(f"Server running on port {PORT}")
    asyncio.run(main(HOST, PORT))
except KeyboardInterrupt:
    pass
finally:
    loop.close()