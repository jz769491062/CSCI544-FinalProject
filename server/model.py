def mockEval(msg):
    if msg == 'beep':
        return 1
    if msg == 'bweep':
        return 0.8
    return 0
def checkMessage(msg):
    return mockEval(msg)