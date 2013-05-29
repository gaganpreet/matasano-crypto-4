#!/usr/bin/python
import util

class RandomAccessCTR:
    ''' Random access CTR with an edit function to replace any part of plain text with a user provided one '''
    def __init__(self):
        self.key = util.random_string(16)

    def encrypt(self, text):
        return util.ctr_encrypt(text, self.key)

    def edit(self, ciphertext, offset, new_text):
        plaintext = util.ctr_decrypt(ciphertext, self.key)
        new_plaintext = plaintext[:offset] + new_text + plaintext[offset+len(new_text):]
        return self.encrypt(new_plaintext)

def main():
    text = open('ecb_text').read()

    ctr = RandomAccessCTR()
    ciphertext = ctr.encrypt(text)

    new_ciphertext = ctr.edit(ciphertext, 0, 'a'*len(ciphertext))

    keystream = util.string_xor(new_ciphertext, 'a'*len(ciphertext))

    print util.string_xor(keystream, ciphertext)


if __name__ == '__main__':
    main()
