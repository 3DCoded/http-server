import copy
from http.server import BaseHTTPRequestHandler, HTTPServer

class Server:
    server = None
    addr = None
    
    class Handler(BaseHTTPRequestHandler):
        pass
    _Handler = copy.deepcopy(Handler)
    
    def __init__(self):
        '''Server class for http servers. '''
        pass

    def bind_addr(self, addr):
        '''Bind to server address'''
        if not self.server:
            self.addr = addr
            self.server = HTTPServer(addr, self.Handler)
        else:
            raise ConnectionError('Cannot re-bind Server object. ')

    def bind(self, evt, cmd):
        '''Bind to server event evt and do cmd.
Arguments passed to cmd:
    request (BaseHTTPRequestHandler) - The request'''
        evt = evt.upper()
        if not (evt.startswith('<') and evt.endswith('>')):
            evt = f'<{evt}>'
        name = evt[1:-1]
        name = f'do_{name}'
        def _cmd(self):
            cmd(self)
        _cmd.__name__ = name
        _cmd.__qualname__ = name
        old = _cmd.__code__
        ctype = type(old)
        code = ctype(
            old.co_argcount,
            old.co_posonlyargcount,
            old.co_kwonlyargcount,
            old.co_nlocals,
            old.co_stacksize,
            old.co_flags,
            old.co_code,
            old.co_consts,
            old.co_names,
            old.co_varnames,
            '',
            name,
            0,
            old.co_lnotab,
            old.co_freevars,
            old.co_cellvars
            )
        _cmd.__code__ = code
        setattr(self.Handler, name, _cmd)
        if self.server:
            self.server = HTTPServer(self.addr, self.Handler)

    def unbind(self, evt):
        '''Unbind to server event evt'''
        evt = evt.upper()
        if not (evt.startswith('<') and evt.endswith('>')):
            evt = f'<{evt}>'
        name = evt[1:-1]
        name = f'do_{name}'
        delattr(self.Handler, name)
        if self.server:
            self.server = HTTPServer(self.addr, self.Handler)

    def run(self):
        if self.server:
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.close()
        else:
            raise ConnectionError('Must bind to server in order to run. ')

    def close(self):
        if self.server:
            self.server.socket.close()
        else:
            raise ConnectionError('Must bind to server in order to run. ')

    def reset(self):
        self.server.socket.close()
        self.server = None
        self.addr = None
        self.Handler = self._Handler

    def __repr__(self):
        return f'<Server bind={bool(self.server)} addr={self.addr}>'

    __str__ = __repr__
