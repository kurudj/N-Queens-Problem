import copy
import io
import unittest
import unittest.mock
import random

def succ(state, static_x, static_y):
    index = 0
    succs = []
    if state[static_x]!=static_y:
        return []
    for i in state:
        deldown = copy.deepcopy(state)
        delup = copy.deepcopy(state)
        if index==static_x and i==state[index]:
            index += 1
        else:
            if deldown[index] in range(1,len(state)):
                deldown[index] -= 1
                succs.append(deldown)
            if delup[index] in range(0,len(state)-1):
                delup[index] += 1
                succs.append(delup)
            index = index+1
    retList = []
    for x in succs:
        if x in retList:
            continue
        else:
            retList.append(x)
    return sorted(retList)

def f(state):
    numAtt = 0
    attackArr = [False] * len(state)
    for i in range(0,len(state)):
        end=False
        if i!=0: #check west
            for j in range(1,len(state)):
                if i-j in range(0,len(state)):
                    if state[i]==state[i-j]:
                        attackArr[i] = True
                        end = True
                if end:
                    break
        if i!=len(state)-1: #check east
            for j in range(1,len(state)):
                if i+j in range(1,len(state)):
                    if state[i]==state[i+j]:
                        attackArr[i] = True
                        end = True
                if end:
                    break
        for j in range(1,len(state)):
            if i-j in range(0,len(state)):
                if state[i-j]-j==state[i]:
                    attackArr[i] = True
                if state[i-j]+j==state[i]:
                    attackArr[i] = True
            if i+j in range(1,len(state)):
                if state[i+j]-j==state[i]:
                    attackArr[i] = True
                if state[i+j]+j==state[i]:
                    attackArr[i] = True
    numAtt = sum(attackArr)
    return numAtt

def choose_next(curr, static_x, static_y):
    if len(succ(curr, static_x, static_y))==0:
        return None
    succs = succ(curr, static_x, static_y)
    succs.append(curr)
    succs = sorted(succs)
    nextState = succs[0]
    for newState in succs:
        if f(newState)<f(nextState):
            nextState = newState
    return nextState

def n_queens(initial_state, static_x, static_y):
    a = initial_state
    message = str(initial_state) + ' - f={}'
    print(message.format(f(initial_state)))
    next_state = choose_next(initial_state, static_x, static_y)
    while f(next_state)!=0:
        if f(a)==f(next_state):
            break
        a = next_state
        message = str(next_state) + ' - f={}'
        print(message.format(f(next_state)))
        next_state = choose_next(next_state, static_x, static_y)
    message = str(next_state) + ' - f={}'
    print(message.format(f(next_state)))
    return next_state

def n_queens_restart(n, k, static_x, static_y):
    random.seed(1)
    state=[0]*n
    list = []
    for y in range(0,k):
        for x in range(0,n):
            if x==static_x:
                state[x] = static_y
                continue
            state[x] = random.randint(0, n-1)
        list.append(n_queens(state,static_x,static_y))
        if f(list[len(list)-1])==0:
            print(list[len(list)-1])
            return list[len(list)-1]
        else:
            continue

class NQueensTest(unittest.TestCase):
    def test_succ_1(self):
        from nqueens import succ

        succ_states = succ([0, 1, 2], 0, 0)
        expected_res = [[0, 0, 2], [0, 1, 1], [0, 2, 2]]
        self.assertEqual(succ_states, expected_res)

    def test_succ_2(self):
        from nqueens import succ

        succ_states = succ([0, 1, 2], 0, 1)
        expected_res = []
        self.assertEqual(succ_states, expected_res)

    def test_f(self):
        from nqueens import f

        self.assertEqual(f([1, 2, 2]), 3)
        self.assertEqual(f([2, 2, 2]), 3)
        self.assertEqual(f([0, 0, 2]), 3)
        self.assertEqual(f([0, 2, 0]), 2)
        self.assertEqual(f([0, 2, 1]), 2)

    def test_choose_next(self):
        from nqueens import choose_next

        self.assertEqual(choose_next([1, 1, 2], 1, 1), [0, 1, 2])
        self.assertEqual(choose_next([0, 2, 0], 0, 0), [0, 2, 0])
        self.assertEqual(choose_next([0, 1, 0], 0, 0), [0, 2, 0])
        self.assertEqual(choose_next([0, 1, 0], 0, 1), None)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def check_n_queens(self, state, must_x, must_y, expected_output, expected_stdout, mock_stdout):
        from nqueens import n_queens

        final_state = n_queens(state, must_x, must_y)
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)
        self.assertEqual(final_state, expected_output)

    def test_n_queens_1(self):
        expected_stdout = "".join([
            "[0, 1, 2, 3, 5, 6, 6, 7] - f=8\n",
            "[0, 1, 2, 3, 5, 7, 6, 7] - f=7\n",
            "[0, 1, 1, 3, 5, 7, 6, 7] - f=7\n"])
        expected_output = [0, 1, 1, 3, 5, 7, 6, 7]

        state, must_x, must_y = [0, 1, 2, 3, 5, 6, 6, 7], 1, 1
        self.check_n_queens(state, must_x, must_y, expected_output, expected_stdout)

    def test_n_queens_2(self):
        expected_stdout = "".join([
            "[0, 7, 3, 4, 7, 1, 2, 2] - f=7\n",
            "[0, 6, 3, 4, 7, 1, 2, 2] - f=6\n",
            "[0, 6, 3, 5, 7, 1, 2, 2] - f=4\n",
            "[0, 6, 3, 5, 7, 1, 3, 2] - f=3\n",
            "[0, 6, 3, 5, 7, 1, 4, 2] - f=0\n"
        ])
        expected_output = [0, 6, 3, 5, 7, 1, 4, 2]

        state, must_x, must_y = [0, 7, 3, 4, 7, 1, 2, 2], 0, 0
        self.check_n_queens(state, must_x, must_y, expected_output, expected_stdout)

if __name__ == "__main__":
    unittest.main()
#n_queens_restart(7, 10, 0, 0)
#n_queens_restart(8, 1000, 0, 0)
