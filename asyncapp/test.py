#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2018 Marcin Borowicz <marcinbor85@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from asyncapp import AsyncApp
from asyncapp import AsyncServer

import asyncio

class TestAsyncServer(AsyncServer):
    async def service(self, reader, writer):
        try:
            data = await asyncio.wait_for(reader.read(100), timeout=1)
        except asyncio.TimeoutError:
            return
        if data[0] == ord('q'):
            self.close()
            return
        writer.write(data)
        try:
            data = await asyncio.wait_for(writer.drain(), timeout=1)
        except asyncio.TimeoutError:
            return

class TestAsyncApp(AsyncApp):
    def on_start(self, loop):
        asyncio.ensure_future(self.my_loop('fast', 40, 0.3))
        asyncio.ensure_future(self.my_loop('slow', 20, 1.0))
        self.server = TestAsyncServer(self, '127.0.0.1', 8080)
        print('started')

    def on_stop(self, loop):
        self.server.stop()
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


