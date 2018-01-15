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

import asyncio

class AsyncServer():
    def __init__(self, app, *args, **kwargs):
        self._app = app
        self._loop = app.get_loop()
        self._close_force = False
        coro = asyncio.start_server(self._service, *args, loop=self._loop, **kwargs)
        self._server = self._loop.run_until_complete(coro)

    def close(self):
        self._close_force = True

    def stop(self):
        self._server.close()
        self._loop.run_until_complete(self._server.wait_closed())

    async def service(self, reader, writer):
        pass

    async def _service(self, reader, writer):
        try:
            while self._app.is_run() and not self._close_force:
                await self.service(reader, writer)
        finally:
            writer.close()
            self._close_force = False


