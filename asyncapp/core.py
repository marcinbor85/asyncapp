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

class AsyncApp():
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self._force_stop = False

    def start(self):
        self.on_start(self._loop)
        self._execute()

    def stop(self):
        if self._force_stop == False:
            self._loop.stop()
    
    def on_start(self, loop):
        pass

    def on_stop(self, loop):
        pass

    def get_loop(self):
        return self._loop

    def is_run(self):
        return not self._force_stop

    def _execute(self):
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self._force_stop = True

            while True:
                tasks = asyncio.Task.all_tasks()
                pending = [t for t in tasks if not t.cancelled() and not t.done()]
                gather = asyncio.gather(*pending)
                try:
                    self._loop.run_until_complete(gather)
                except asyncio.CancelledError:
                    continue
                except KeyboardInterrupt:
                    continue
                break
            
            self.on_stop(self._loop)
            self._loop.close()


