

def _get_block(s, count):
    if count <= 0:
        return ''
    buf = ''
    while len(buf) < count:
        buf2 = s.recv(count - len(buf))
        if not buf2:
            # error or just end of connection?
            if buf:
                raise RuntimeError("underflow")
            else:
                return ''
        buf += buf2
    return buf

def _send_block(s, data):
    while data:
        data = data[s.send(data):]

def _get_count(s):
    buf = ''
    while True:
        c = s.recv(1)
        if not c:
            # error or just end of connection/
            if buf:
                raise RuntimeError("underflow")
            else:
                return -1
        if c == '|':
            return int(buf)
        else:
            buf += c

def get_msg(s):
    return _get_block(s, _get_count(s))

def send_msg(s, data):
    _send_block(s, str(len(data)) + '|')
    _send_block(s, data)
