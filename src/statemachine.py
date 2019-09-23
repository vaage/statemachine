
class State:
    def __init__(self, name, description):
        self.__name = name
        self.__description = description

    def get_name(self):
        '''Get the state's name.'''
        return self.__name

    def get_description(self):
        '''Get the state's description.'''
        return self.__description


class Walker:
    '''The walker allows multiple independent systems to track their state with a
    shared state machine.
    '''
    def __init__(self, starting_state, can_move_between):
        assert starting_state is not None, 'The starting state cannot be None.'
        assert can_move_between is not None, '|canMoveBetween| cannot be None.'

        self.__current_state = starting_state
        self.__can_move_between = can_move_between

    def move_to(self, state):
        '''Try moving to a new state.

        Request that the walker moves from its current state to a new state. The
        walker will only accept |state| as the new current state if the state
        machine allows the transition.

        Args:
            state: State, the state that we want to walker to move to.
        Returns:
            boolean, True if the walker successfuly moved to |state| and False
                if the walker was unable to move to |state.
        '''
        assert state is not None, 'We cannot move to a null state.'

        if self.__can_move_between(self.__current_state, state):
            self.__current_state = state
            return True

        return False

    def get_state(self):
        '''Get the current state.

        Get the state that the walker is currently at in the state machine.
        Initially, this would return the intial state, but any successfuly calls
        to MoveTo() will change what this returns.

        Returns:
            State, the current state in the state machine that the walker points
                to.
        '''
        return self.__current_state


class StateMachine:
    def __init__(self):
        self.__initial_state = None
        self.__states = []
        self.__out_transitions = {}  # Map State to set<State>

    def define_initial_state(self, name, description=''):
        '''Add the initial state.

        Create and add the initial state for the state machine. This must be
        called and should not be called more than once.

        Args:
            name: string, The name of the state.
            description: string, A description for this state. This is optional
                but should never be None.

        Returns:
            State, the new state.
        '''
        assert self.__initial_state is None, 'Only set initial state once.'
        self.__initial_state = self.__create_new_state(name, description)
        return self.__initial_state

    def define_state(self, name, description=''):
        '''Create and add a new state to the state machine.

        Args:
            name: string, The name of the state.
            description: string, A description for this state. This is optional
                but should never be None.

        Returns:
            State, the new state.
        '''
        return self.__create_new_state(name, description)

    def define_transition(self, start, destination):
        '''Create and add a new transition.

        Create and add a new transition between |start| and |destination|. If there
        already exists a transition between |start| and |destination| this will be
        a no-op.

        Args:
            start: State, the state that leads to |destination|.
            destination: State, the state that this transition leads to.
        '''
        self.__out_transitions[start].add(destination)

    def start(self):
        '''Start tracking progress through the state machine.

        Create a new Walker in order to track progress through the state machine.

        Return:
            Walker, a new walker for moving through this state machine.
        '''
        def can_move_between(state_a, state_b):
            assert state_a is not None, 'We cannot move away from a None state.'
            assert state_b is not None, 'We cannot move toward a None state.'
            return state_b in self.__out_transitions[state_a]

        return Walker(self.__initial_state, can_move_between)

    def __create_new_state(self, name, description):
        assert name is not None, 'State names cannot be None.'
        assert description is not None, 'Use "" instead of None for description.'

        state = State(name, description)
        self.__states.append(state)

        # Create the transitions entry for the new state now because so that we
        # can assume it already exists in DefineTransition()
        self.__out_transitions[state] = set()
        return state
