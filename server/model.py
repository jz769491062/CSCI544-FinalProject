def evaluate(msg):
    evaluation = "pass"
    confidence = 1
    return evaluation

def mockEval(msg):
    if msg == 'beep':
        return "fail"
    return "pass"
def checkMessage(msg):
    return mockEval(msg)