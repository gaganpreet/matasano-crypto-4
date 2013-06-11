import sha1
import util

class MAC:
    ''' SHA1 based MAC generator '''
    def __init__(self):
        self.key = util.random_string(20)

    def mac(self, text):
        return sha1.sha1(self.key + text)

    def verify(self, text, _hash):
        return _hash == self.mac(text)

if __name__ == '__main__':
    mac = MAC()

    s = 'Little Wing'

    print mac.mac(s)

    print mac.verify(s, mac.mac(s))
