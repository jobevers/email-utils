import mailbox

def isMbox(filename):
    """Returns True if `filename` is an mbox file.

    Uses simple heuristics to make the determination.
    """
    with open(filename) as f:
        line = f.readline()
        return re.match('From - ', line)


class MultiMbox(object):
    def __init__(self, *mboxes):
        self.mboxes = mboxes

    def itervalues(self):
        for mbox in self.mboxes:
            for msg in mbox.itervalues():
                yield msg
        
    @classmethod
    def load(cls, filenames):
        mboxes = [mailbox.mbox(f) for f in filenames if isMbox(f)]
        return cls(*mboxes)


def saveMsgsToNewMbox(msgs, filename):
    mbox = mailbox.mbox(filename)
    for msg in msgs:
        mbox.add(msg)
    mbox.close()
