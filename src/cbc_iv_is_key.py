import urllib
import util
import string

class InvalidString(Exception):
    pass


class AES():
    def __init__(self): 
        self.key = util.random_string(16) 
        self.iv = self.key
          
    def encrypt(self, text):
        ''' Encrypt text with AES 128 CBC with a chosen random key
        '''
        prepend = 'comment1=cooking%20MCs;userdata='
        append = ';comment2=%20like%20a%20pound%20of%20bacon'

        return util.cbc_encrypt(prepend + urllib.quote(text) + append, self.key, self.iv)
    
    def decrypt(self, text):
        ''' Decrypt text with AES 128 CBC with a chosen random key
        ''' 
        s = util.cbc_decrypt(text, self.key, self.iv)
        if s.strip(string.printable):
            raise InvalidString, s 
        return s


def main():
    aes = AES()
    text = 'a' * 16 * 3

    encrypted = aes.encrypt(text)

    blocks_encrypted = util.get_blocks(encrypted, 16)
    blocks_encrypted[0] = blocks_encrypted [2] = blocks_encrypted[1]
    blocks_encrypted[1] = '\0' * 16
    
    modified_encrypted = ''.join(blocks_encrypted)

    try:
        decrypted = aes.decrypt(modified_encrypted)
    except InvalidString as e:
        decrypted = str(e)

    blocks_decrypted = util.get_blocks(decrypted, 16)
    print 'Recovered key/IV: ', repr(util.string_xor(blocks_decrypted[0], blocks_decrypted[2]))


if __name__ == '__main__':
    main()
