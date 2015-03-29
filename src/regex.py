"""
Regular expression can be modelled by non-deterministic finite state automata (NFAs). As there are potentially multiple
transitions from each state of the automaton, the next state cannot be computed deterministically . Instead all the
possible transitions must be examined and considered at the same time.

The NFA is represented by a digraph which models the states of the NFA and their transitions. Each character of the
pattern of length M becomes a node in the digraph.

At each step of the NFA simulation we must keep track of all the possible transitions to future states that can take
place from the current state. In graph terms this corresponds to the multiple source reachability problem, i.e. which
nodes are reachable from a starting set S of nodes. This is an application of the DFS algorithm for each starting
node in S.

To implement regular expressions we can built the NFA that corresponds to the regular expression and then feed the
input text to the NFA and follow it until we reach either the end state or the end of the input.

In this simplified version of regular expressions, we only handle parenthesis, the * wildcard and the OR | operator.
We use an operator stack to keep track of the operators. Upon a ( or a | we push the operator on the stack. Upon a
) we pop the operators from the top of the stack until we pop the matching left parenthesis (.

The running time for the construction of the NFA is O(M) since for each of the M characters of the pattern we create
one digraph node and add up to 3 epsilon transitions and execute 1 or 2 stack operations.

The running time of the simulation is O(T*M) as there are T passes for an input text of length T and we perform a DFS
in each pass. The DFS itself takes time proportional to O(M) as there are O(M) nodes and edges.
"""

from graph_utils import Digraph

class SimpleRegEx:
    def __init__(self, pattern):
        self.pat = pattern
        self.end_state = len(pattern)
        self.__build_nfa()

        # stores a flag per node indicating if the last DFS operation reached the corresponding node
        self._marked = [False for _ in range(self.nfa.V())]

    def matches(self, text):
        # find the epsilon transitions from the origin state
        self.__dfs_cycle([0])

        current_states = self.__get_reachable_states()
        if self.end_state in current_states:
            return True

        # compute the next set of reachable states for each input character
        for i in range(len(text)):
            new_states = []

            for state in current_states:
                if text[i] == self.pat[state] or self.pat[state] == '.':
                    new_states.append(state+1)

            self.__dfs_cycle(new_states)
            current_states = self.__get_reachable_states()
            if self.end_state in current_states:
                return True

            if len(current_states) == 0:
                return False

        return self.end_state in current_states

    def __get_reachable_states(self):
        return [i for i in range(self.end_state + 1) if self._marked[i]]

    def __build_nfa(self):
        op_stack = []
        self.nfa = Digraph(len(self.pat) + 1)

        # tracks the last left parenthesis
        leftPar = -1

        for i in range(self.end_state):
            ch = self.pat[i]

            if ch == '(':

                # add an epsilon transition to the next character and push the operator for later processing
                self.nfa.add_edge(i, i+1)
                op_stack.append(i)
                leftPar = i

            elif ch == '|' and leftPar >= 0:

                # add a transition from the left parenthesis node to the first node after the OR (|) operator
                self.nfa.add_edge(leftPar, i+1)
                op_stack.append(i)

            elif ch == ')':

                # add a transition from the node right after the | operator to the right parenthesis node
                last_op = op_stack.pop()
                while self.pat[last_op] == '|':
                    self.nfa.add_edge(last_op, i)
                    last_op = op_stack.pop()

                leftPar = last_op
                self.nfa.add_edge(i, i+1)

                # handles the case (...)*
                if i < self.end_state - 1 and self.pat[i+1] == '*':
                    self.nfa.add_edge(leftPar, i+1)
                    self.nfa.add_edge(i+1, leftPar)

            elif ch == '*':
                # always add a transition to the next node as the star operator can match a zero input
                self.nfa.add_edge(i, i+1)

                # handles the case of a star operator after a simple symbol, e.g. ab*
                if i > 0 and self.pat[i-1] != ')':
                    self.nfa.add_edge(i, i-1)
                    self.nfa.add_edge(i-1, i+1)

        assert len(op_stack) == 0

    def __dfs_cycle(self, states):
        self._marked = [False for _ in range(self.nfa.V())]
        for s in states:
            self.__dfs(s)


    def __dfs(self, v):
        self._marked[v] = True
        for w in self.nfa.edges(v):
            if not self._marked[w]:
                self.__dfs(w)

if __name__ == "__main__":

    re = SimpleRegEx("abc")
    assert re.matches("abc")

    re = SimpleRegEx("ab.")
    assert re.matches("abd")

    re = SimpleRegEx("a*")
    assert re.matches("a")
    assert re.matches("")
    assert re.matches("aaaaaaaaaaaa")

    re = SimpleRegEx("(Hello|Hola) G(.)*s")

    while True:
        text = raw_input('Give a text: ')
        print re.matches(text)
