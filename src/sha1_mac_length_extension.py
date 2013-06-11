import sha1_mac
import struct
from binascii import unhexlify
from impl import sha1

def get_glue_padding(byte_len):
    ''' Get glue padding string used for sha1 hash
        Arguments:
            byte_len: number of bytes in the message
    '''
    bit_len = byte_len * 8

    glue_padding = '\x80'
    glue_padding += '\x00' * ((56 - (byte_len + 1) % 64) % 64)
    glue_padding +=  struct.pack('>Q', bit_len)
    
    return glue_padding

def extend_message(message, extension, init, key_len):
    ''' Length based extension attack on a sha1 keyed authentication code 
        Arguments:
            message: Original message
            extension: Message to append
            init: list of sha1 init variables
            key_len: length of key
    '''

    original_len = key_len + len(message)
    glue_padding = get_glue_padding(original_len)
    original_len += len(glue_padding)

    new_message = message + glue_padding + extension

    new_hash = sha1.sha1(extension, init, original_len)
    
    return (new_message, new_hash)

if __name__ == '__main__':
    mac = sha1_mac.MAC()

    message = 'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
    extension = ';admin=true'
    hash_ = mac.mac(message)

    print '''Hash for %s is: '%s' '''%(repr(message), hash_)

    init = struct.unpack('>' + 'I'*5, unhexlify(hash_))

    for i in xrange(40):
        print 'Trying key_len', i, 
        try:
            new_message, new_hash = extend_message(message, extension, init, i) 
        except struct.error:
            continue
        if mac.verify(new_message, new_hash):
            print
            print 'Original key length: %s'%i
            print 'New messsage: %s,\nNew hash: %s'%(repr(new_message), new_hash)
            break
        else:
            print '- invalid'

