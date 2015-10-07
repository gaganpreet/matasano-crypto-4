import util
import urllib

class RandomCTR():
    def __init__(self):
        self.key = util.random_string(16)

    def encrypt(self, text):
        prepend = 'comment1=cooking%20MCs;userdata='
        append = ';comment2=%20like%20a%20pound%20of%20bacon'

        return util.ctr_encrypt(prepend + urllib.quote(text) + append, self.key)

    def decrypt(self, text):
        return util.ctr_decrypt(text, self.key)

def is_compromised(s):
    if s.find(';admin=true;') != -1:
        return True
    return False

def flip_bit(c, i):
    return chr(ord(c) ^ (1 << i))

def modify_bit_string(s, char_index, bit_index):
    ''' Flip the bit at bit_index in the character at char_index in s '''
    return s[:char_index] + flip_bit(s[char_index], bit_index) + s[char_index+1:]

if __name__ == '__main__':
    ''' This is similar to the CBC bit flipping in set 2'''
    ctr = RandomCTR()

    to_insert = '3admin-true'

    encrypted = ctr.encrypt(to_insert)
    print 'String is compromised: %s' % (is_compromised(ctr.decrypt(encrypted)))

    ''' I found the characters 3 and - to modify manually, using this:
           for i in xrange(255):
              if bitCount(i ^ ord(';')) == 1:
                          print chr(i), repr(i)

        More info in cbc_bit_flipping.py
    '''

    print 'Modifying bits'
    encrypted = modify_bit_string(encrypted, 32, 3)
    encrypted = modify_bit_string(encrypted, 38, 4)

    print 'String is compromised: %s' % (is_compromised(ctr.decrypt(encrypted)))
