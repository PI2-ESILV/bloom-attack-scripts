import struct
import socket
import time
import hashlib
import binascii
from BloomFilter import BloomFilter

magic = "f9beb4d9"

def makeMessage(magic,command,payload):
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[0:4]
    return magic.decode("hex")+struct.pack('12sI4s',command,len(payload),checksum)+payload

def makeVersionPayload():#variable a changer si bbesoin
    version = 70002
    services = 0
    timestamp = int(time.time())

    addr_you = "127.0.0.1"
    services_you = 0
    port_you = 8333

    addr_me = "127.0.0.1"
    services_me = 0
    port_me = 8333

    nonce = 0

    user_agent_bytes = 0
    start_height = 0
    relay = 1

    #https://bitcoin.org/en/developer-reference#version
    #contenu obligatoire du message version
    payload = b"";
    payload += struct.pack("i",version)
    payload += struct.pack("Q",services)
    payload += struct.pack("q",timestamp)
    payload += struct.pack("Q",services_you)
    payload += struct.pack(">16s",addr_you.encode('utf-8'))
    payload += struct.pack(">H",port_you)
    payload += struct.pack("Q",services_me)
    payload += struct.pack(">16s",addr_me.encode('utf-8'))
    payload += struct.pack(">H",port_me)
    payload += struct.pack("Q",nonce)
    payload += struct.pack("B",user_agent_bytes)
    payload += struct.pack("i",start_height)
    payload += struct.pack("B",relay)
    return payload
    
def makeFilterloadPayload(publicKeyHash, scriptHash, transactionID):
    filter = BloomFilter(3, 0.01, 0, 1)
    filter.add(publicKeyHash)
    filter.add(scriptHash)
    filter.add(transactionID)
    print(len(filter.bit_array))
    payload = filter.serialize()
    return payload

def sendMessage(magic,command,payload,IP):
    ip = socket.gethostbyname(IP)
    port = 8333
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connected to node...")
    
    sock.connect((ip,port))

    msg = makeMessage(magic,"version",payload)
    print("sending version packet")
    sock.send(msg)

def waitAnswer():
    while 1:
        msg = sock.recv(2**10)
        if not msg:
            print("done")
            exit()
        else:
            print(msg.encode("hex"))


Version = makeVersionPayload() 
FilterLoad = makeFilterloadPayload("1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs", "3P14159f73E4gFr7JterCCQh9QjiTjiZrG",
                     "40eee3ae1760e3a8532263678cdf64569e6ad06abc133af64f735e52562bccc8")