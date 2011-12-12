# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .base import apply_target, BasePool
from threading import Thread

class TaskPool(BasePool):

    def __init__(self, *args, **kwargs):
        super(TaskPool, self).__init__(*args, **kwargs)
        from twisted.internet import reactor
        self.reactor = reactor
        self.reactor_thread = None

    def on_start(self):
        def run_reactor():
            self.reactor.run(installSignalHandlers=False)
        self.reactor_thread = Thread(target=run_reactor)
        self.reactor_thread.start()

    def on_stop(self):
        self.reactor.stop()

    def on_apply(self, target, args=None, kwargs=None, callback=None,
            accept_callback=None, **_):
        self.reactor.callFromThread(apply_target, target, args, kwargs,
                           callback, accept_callback)
