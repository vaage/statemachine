# Sample Usage

## Scenario

To illustrate how to use this utility, suppose you are implementing the builder
pattern for media manifests and and need to restrict call-order of the builder's
methods.

Suppose that we are working to implement the following interface:

```python
class Builder(object):
  def AddAdaptationSet(self):
    return self

  def AsAudio(self, channels, bitrate):
    return self

  def AsVideo(self, height, width, bitrate):
    return self

  def AddStream(self):
    return self

  def AddSegment(self, startTime, duration, data):
    return self

  def Build(self):
    return None
```

## Defining The State Machine

We can define a state machine as below to help us control the use of our
builder. We will show how it can be used after we show how to construct the
the state machine.

```python
sm = StateMachine()

# States
s_root = sm.DefineInitialState('root')
s_add_adaptation_set = sm.DefineState('add adaptation set')
s_as_audio = sm.DefineState('as audio')
s_as_video = sm.DefineState('as video')
s_add_stream = sm.DefineState('add stream')
s_add_segment = sm.DefineState('add segment')
s_build = sm.DefineState('build')


# Transitions
sm.DefineTransition(s_root, s_add_adaptation_set)
sm.DefineTransition(s_root, s_build)
sm.DefineTransition(s_add_adaptation_set, a_as_audio)
sm.DefineTransition(s_add_adaptation_set, a_as_video)
sm.DefineTransition(s_as_audio, s_add_stream)
sm.DefineTransition(s_as_video, s_add_stream)
sm.DefineTransition(s_add_stream, s_add_segment)
sm.DefineTransition(s_add_segment, s_add_segment)
sm.DefineTransition(s_add_segment, s_add_stream)
sm.DefineTransition(s_add_segment, s_add_adaptation_set)
sm.DefineTransition(s_add_segment, s_build)
```

## Using the State Machine

Now that we have our state machine, we can use it in our builder. To keep the
sample code as simple as possible, we'll replace redundent and/or irrelevant
code with "...".

```python
class Builder(object):
  def __init__(self):
    self.__sm = StateMachine()
    self.__s_add_adaptation_set = ...
    ...
    self.__handle = self.__sm.Start()

  def AddAdaptationSet(self):
    self.__MoveTo(self.__s_add_adaptation_set)
    ...
    return self

  def AsAudio(self, channels, bitrate):
    self.__MoveTo(self.__s_as_audio)
    ...
    return self

  def AsVideo(self, height, width, bitrate):
    self.__MoveTo(self.__s_as_video)
    ...
    return self

  def AddStream(self):
    self.__MoveTo(self.__s_add_stream)
    ...
    return self

  def AddSegment(self, startTime, duration, data):
    self.__MoveTo(self.__s_add_segment)
    ...
    return self

  def Build(self):
    self.__MoveTo(self.__s_build)
    ...
    return None

  # Try moving to a new state, if the move is not allowed, raise an exception.
  def __MoveTo(self, state):
    if not self.__handle.moveTo(state):
      at = self.__handle.GetCurrent()
      raise Exception('Cannot move from %s to %s' % (at.name(), state.name())
```
