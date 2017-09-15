import inputgenerator
import statistics

__expected = inputgenerator.randomstring(300)


def check(message):
    equal = message == __expected
    right = 0
    wrong = 0
    for i in range(len(__expected)):
        print(i)
        if __expected[i] == message[i]:
            right += 1
        else:
            wrong += 1
    return right, wrong, equal, len(__expected), len(message)


def stats(messages):
    isequal = []
    rightpct = []
    for msg in messages:
        right, wrong, equal, expectedlen, msglen = check(msg)
        isequal.append(equal)
        rightpct.append(right/float(expectedlen))
    return statistics.mean(isequal), statistics.mean(rightpct)
