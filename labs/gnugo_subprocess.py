import subprocess


args = 'gnugo --mode gtp'
p = subprocess.Popen(args.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)


def readlines(stdout, line):
    output = []
    for i in range(line):
        output.append(stdout.readline())
    return output

p.stdin.write('version\n')
p.stdin.flush()
o = readlines(p.stdout, 2)
print(o)

p.stdin.write('name\n')
p.stdin.flush()
o = readlines(p.stdout, 2)
print(o)

for i in range(50):
    print(i)
    p.stdin.write('genmove black\n')
    p.stdin.flush()
    o = readlines(p.stdout, 2)
    print(o)

    p.stdin.write('genmove white\n')
    p.stdin.flush()
    o = readlines(p.stdout, 2)
    print(o)

    p.stdin.write('list_stones black\n')
    p.stdin.flush()
    o = readlines(p.stdout, 2)
    print(o)

    p.stdin.write('list_stones white\n')
    p.stdin.flush()
    o = readlines(p.stdout, 2)
    print(o)
print(0)
