import inputgenerator

__expected = inputgenerator.randomstring()


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def check(message):
    equal = message == __expected
    right = 0
    wrong = 0
    for i in range(len(__expected)):
        if i >= len(message) or __expected[i] != message[i]:
            wrong += 1
        else:
            right += 1
    return right, wrong, equal, len(__expected), len(message)


def stats(messages):
    isequal = []
    rightpct = []
    for msg in messages:
        right, wrong, equal, expectedlen, msglen = check(msg[0])
        isequal.append(equal)
        rightpct.append(right/float(expectedlen))
    return mean(isequal), mean(rightpct)
