
class State(object):
  def __init__(self, name, description):
    self.__name = name
    self.__description = description

  def GetName(self):
    return self.__name

  def GetDescription(self):
    return self.__description


class Walker(object):
  '''The walker allows multiple independent systems to track their state with a
  shared state machine.
  '''
  def __init__(self, startingState, canMoveBetween):
    assert startingState is not None, 'The starting state cannot be None.'
    assert canMoveBetween is not None, '|canMoveBetween| cannot be None.'

    self.__currentState = startingState
    self.__canMoveBetween = canMoveBetween
 
  def MoveTo(self, state):
    '''Try moving to a new state.

    Request that the walker moves from its current state to a new state. The
    walker will only accept |state| as the new current state if the state
    machine allows the transition.

    Args:
      state: State, the state that we want to walker to move to.
    Returns:
      boolean, True if the walker successfuly moved to |state| and False if the
        walker was unable to move to |state.
    '''
    assert state is not None, 'We cannot move to a null state.'

    if self.__canMoveBetween(self.__currentState, state):
      self.__currentState = state
      return True

    return False

  def GetState(self):
    '''Get the current state.

    Get the state that the walker is currently at in the state machine.
    Initially, this would return the intial state, but any successfuly calls
    to MoveTo() will change what this returns.

    Returns:
      State, the current state in the state machine that the walker points
        to.
    '''
    return self.__currentState


class StateMachine(object):
  def __init__(self):
    self.__initialState = None
    self.__states = []
    self.__outTransitions = {}  # Map State to set<State>

  def DefineInitialState(self, name, description=''):
    '''Add the initial state.

    Create and add the initial state for the state machine. This must be called
    and should not be called more than once.

    Args:
      name: string, The name of the state.
      description: string, A description for this state. This is optional but
        should never be None.

    Returns:
      State, the new state.
    '''
    assert self.__initialState is None, 'Don\'t define multiple initial states.'
    self.__initialState = self.__CreateNewState(name, description)
    return self.__initialState

  def DefineState(self, name, description=''):
    '''Create and add a new state to the state machine.

    Args:
      name: string, The name of the state.
      description: string, A description for this state. This is optional but
        should never be None.

    Returns:
      State, the new state.
    '''
    return self.__CreateNewState(name, description)

  def DefineTransition(self, start, destination):
    '''Create and add a new transition.

    Create and add a new transition between |start| and |destination|. If there
    already exists a transition between |start| and |destination| this will be
    a no-op.

    Args:
      start: State, the state that leads to |destination|.
      destination: State, the state that this transition leads to.

    '''
    self.__outTransitions[start].add(destination)

  def Start(self):
    '''Start tracking progress through the state machine.

    Create a new Walker in order to track progress through the state machine.

    Return:
      Walker, a new walker for moving through this state machine.
    '''
    def CanMoveBetween(stateA, stateB):
      assert stateA is not None, 'We cannot move away from a None state.'
      assert stateB is not None, 'We cannot move toward a None state.'

      return stateB in self.__outTransitions[stateA]

    return Walker(self.__initialState, CanMoveBetween)

  def __CreateNewState(self, name, description):
    assert name is not None, 'State names cannot be None.'
    assert description is not None, 'Use "" instead of None for description.'

    state = State(name, description)
    self.__states.append(state)

    # Create the transitions entry for the new state now because so that we can
    # assume it already exists in DefineTransition()
    self.__outTransitions[state] = set()

    return state

