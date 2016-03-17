import re


def searchHeader(key_regex, value_regex, msg, options=re.IGNORECASE):
    for header_key, value in msg.items():
        if re.search(key_regex, header_key, options):
            if re.search(value_regex, value, options):
                return True
    return False


def searchBody(regex, msg, options=re.IGNORECASE):
    for part in msg.walk():
        if part.get_content_maintype() == 'text':
            text = part.get_payload(decode=True)
            if re.search(regex, text, options):
                return True
    return False


def searchAttachmentFilenames(regex, msg, options=re.IGNORECASE):
    for part in msg.walk():
        filename = part.get_filename()
        if filename:
            if re.search(regex, filename, options):
                return True
    return False


def filterMbox(mbox, msg_cond):
    for msg in mbox.itervalues():
        if msg_cond(msg):
            yield msg
