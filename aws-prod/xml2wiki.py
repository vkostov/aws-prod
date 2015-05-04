import sys, re

# Advance until next '<' char; returns tag name
def next_tag(output=True):
    global buffer, lastChar, fout
    while len(buffer) > 0 and buffer[0] != "<":
        presentChar = buffer[0]
        if presentChar != "":
            lastChar = presentChar

        if output:
            print(presentChar, end='')

        buffer = buffer[1:]
    if buffer == "":
        return  # EOF

    tag = ""
    while buffer[0] != ">":
        tag = tag + buffer[0]
        buffer = buffer[1:]
    buffer = buffer[1:]
    return tag[1:]


def contentUntil(searchString):
    global buffer

    if searchString.startswith('</?'):
        return ""

    content = ""
    while not buffer.startswith(searchString):
        content += buffer[0]
        buffer = buffer[1:]
    buffer = buffer[len(searchString):]
    return content


def main(args):
    if len(args) < 2:
        print('Usage python xml2wiki.py <input.xml>')
        exit(2)

    global buffer, lastChar
    fin = open(args[1], 'r')
    buffer = fin.read()

    while len(buffer) > 0:
        tagName = next_tag()
        if tagName.startswith('/'):
            print(']]', end='')
        else:
            print('[[' + tagName + '|', end='')
    fin.close()


if __name__ == '__main__':
    main(sys.argv)