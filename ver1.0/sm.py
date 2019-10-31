"""The SM class implementation"""

class SM(object):
    # state Machine definition
    startState = None

    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return nextState, nextState

    def start(self):
        self.state = self.startState

    def get_state(self):
        return self.state

    def step(self, inp):
        s, o = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs if not self.done(self.state)]

    def run(self, n=10):
        return self.transduce([None] * n)

    def done(self, state):
        return False