import sys
import pprint
import collections


def generate():
    def add_word(transitions, word):
        for i, c in enumerate(word):
            transitions[word[:i]][c] = word[: i + 1]

    def compile(transitions):
        tmap = dict()
        for t in transitions:
            if t not in tmap:
                tmap[t] = len(tmap)
            for c in transitions[t]:
                if transitions[t][c] not in tmap:
                    tmap[transitions[t][c]] = len(tmap)
        comp = dict()
        for t in transitions:
            for c in transitions[t]:
                comp[(tmap[t], c)] = tmap[transitions[t][c]]
        return comp, tmap

    s_tr = collections.defaultdict(dict)
    add_word(s_tr, "do()")
    add_word(s_tr, "don't()")
    add_word(s_tr, "mul(")
    for i in range(10):
        cur_str = str(i)
        s_tr["mul("][cur_str] = "mul(*"
        s_tr["mul(*"][cur_str] = "mul(*"
        s_tr["mul(*,"][cur_str] = "mul(*,*"
        s_tr["mul(*,*"][cur_str] = "mul(*,*"
    s_tr["mul(*"][","] = "mul(*,"
    s_tr["mul(*,*"][")"] = "mul(*,*)"

    c_tr, t_map = compile(s_tr)

    pprint.pprint(c_tr)
    pprint.pprint(t_map)


if __name__ == "__main__":
    solution1 = 0
    solution2 = 0
    do = True

    # State constants
    class t:
        start = 0
        do = 4
        dont = 9
        mul = 13
        mul1 = 14
        mul1f = 15
        mul2 = 16
        mul2f = 17

    # Transition map
    cTr = {
        (t.start, "d"): 1,
        (1, "o"): 2,
        (2, "("): 3,
        (3, ")"): t.do,
        (2, "n"): 5,
        (5, "'"): 6,
        (6, "t"): 7,
        (7, "("): 8,
        (8, ")"): t.dont,
        (t.start, "m"): 10,
        (10, "u"): 11,
        (11, "l"): 12,
        (12, "("): t.mul,
    }

    # Add transitions for digits
    for r in "0123456789":
        cTr[(t.mul, r)] = t.mul1
        cTr[(t.mul1, r)] = t.mul1
        cTr[(t.mul1f, r)] = t.mul2
        cTr[(t.mul2, r)] = t.mul2

    cTr[(t.mul1, ",")] = t.mul1f
    cTr[(t.mul2, ")")] = t.mul2f

    state = 0
    mul = 0
    cur = 0
    s_pos = 0

    for line in sys.stdin:
        line = line.rstrip("\n")
        for i, c in enumerate(line):
            if (state, c) in cTr:
                state = cTr[(state, c)]
            elif (0, c) in cTr:
                state = cTr[(0, c)]
            else:
                state = 0

            if state == t.do:
                do = True
            elif state == t.dont:
                do = False
            elif state == t.mul:
                s_pos = i
            elif state == t.mul1f:
                mul_str = line[s_pos + 1 : i]
                mul = int(mul_str)
                s_pos = i
            elif state == t.mul2f:
                cur_str = line[s_pos + 1 : i]
                cur = int(cur_str)
                solution1 += mul * cur
                if do:
                    solution2 += mul * cur

    print(solution1)
    print(solution2)
