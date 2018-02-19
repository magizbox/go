import pexpect

p = pexpect.spawn('gnugo --mode gtp')
p.sendline('genmove black')
p.expect(pexpect.EOF, timeout=10000)
print(0)