
def isVideo(part):
    return part.get_content_type().find('video') >= 0

def isImage(part):
    return part.get_content_type().find('image') >= 0


def saveImage(part, output_dir, counter):
    filename = getFilename(part, counter)
    filename = ensureUniqueFilename(filename, output_dir)
    logging.debug('Saving %s', filename)
    with open(filename, 'wb') as fp:
        fp.write(part.get_payload(decode=True))


def getFilename(part, counter):
    filename = part.get_filename()
    if not filename:
        ext = mimetypes.guess_extension(part.get_content_type())
        if not ext:
            # Use a generic bag-of-bits extension
            ext = '.bin'
        filename = 'image-%03d%s' % (counter, ext)
    return filename


def ensureUniqueFilename(filename, output_dir):
    base, ext = os.path.splitext(filename)
    full_filename = os.path.join(output_dir, filename)
    count = 1
    while True:
        if not os.path.exists(full_filename):
            return full_filename         
        full_filename = os.path.join(output_dir, '{}-{:03d}{}'.format(base, count, ext))
        count += 1


def skipPart(part):
    content_type = part.get_content_type()
    return content_type in (
        'text/plain',
        'text/html',
        'message/delivery-status',
        'message/rfc822',
    )


def savePart(part, output_dir, counter):
    filename = getFilename(part, counter)
    if os.path.splitext(filename)[1] == '.xml':
        return
    filename = ensureUniqueFilename(filename, output_dir)
    logging.debug('Saving %s', filename)
    if os.path.basename(filename) != filename:
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    with open(filename, 'wb') as fp:
        fp.write(part.get_payload(decode=True))
