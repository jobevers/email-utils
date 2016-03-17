import subprocess


def printMsg(msg, headers=('Date', 'From', 'To')):
    has_html = False
    plain_part = None
    for header in headers:
        print '{}: {}'.format(header, msg[header])
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            plain_part = part
        if part.get_content_type() == 'text/html':
            has_html = True
            printHtmlPart(part)
            break
    if not has_html and plain_part:
        print plain_part


def printHtmlPart(part):
    html = part.get_payload(decode=True)
    proc = subprocess.Popen(
        ['lynx', '-force_html', '-stdin', '-dump', '-nolist'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    stdout, _ = proc.communicate(html)
    print stdout

    
