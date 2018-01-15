# asyncapp

Simple object-oriented asynchronous application wrapper.

## Main features
- Based on standard "asyncio" library
- Python3 compatible
- Simplified and robust stopping of coroutines
- No warnings during application stopping (a common newbies issue)
- Some simplified IO async tools like tcp server and serial port

## Library instalation
```
sudo pip install asyncapp
```

## Usage:
```python
from asyncapp import AsyncApp

import asyncio

class TestAsyncApp(AsyncApp):
    def on_start(self, loop):
        asyncio.ensure_future(self.my_loop('fast', 4, 0.3))
        asyncio.ensure_future(self.my_loop('slow', 2, 1.0))
        print('started')

    def on_stop(self, loop):
        print('stopped')

    async def my_loop(self, name, iters, delay):
        while self.is_run():
            await asyncio.sleep(delay)
            print(name, iters)
            iters -= 1
            if iters == 0:
                self.stop()

if __name__ == '__main__':
    app = TestAsyncApp()
    app.start()
```
