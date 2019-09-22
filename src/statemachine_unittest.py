
import unittest

from statemachine import StateMachine

class StateMachineTests(unittest.TestCase):
    def test_starts_in_initial_state(self):
      sm = StateMachine()
      a = sm.DefineInitialState('a')
      b = sm.DefineState('b')

      sm.DefineTransition(a, b)

      walker = sm.Start()
      self.assertEquals(a, walker.GetState())

    def test_accepts_move_with_transition(self):
      sm = StateMachine()
      a = sm.DefineInitialState('a')
      b = sm.DefineState('b')

      sm.DefineTransition(a, b)

      walker = sm.Start()
      self.assertTrue(walker.MoveTo(b))
      self.assertEquals(b, walker.GetState())

    def test_rejects_move_without_transition(self):
      sm = StateMachine()
      a = sm.DefineInitialState('a')
      b = sm.DefineState('b')
      c = sm.DefineState('c')

      sm.DefineTransition(a, b)
      sm.DefineTransition(b, c)

      walker = sm.Start()
      self.assertFalse(walker.MoveTo(c))
      self.assertEquals(a, walker.GetState())

    def test_rejects_move_to_self_without_transition(self):
      sm = StateMachine()
      a = sm.DefineInitialState('a')
      b = sm.DefineState('b')

      sm.DefineTransition(a, b)

      # There is no transition from a to a, so MoveTo() should return false,
      # however we should still be in state a after.
      walker = sm.Start()
      self.assertFalse(walker.MoveTo(a))
      self.assertEquals(a, walker.GetState())

    def test_accept_move_to_self_with_transition(self):
      sm = StateMachine()
      a = sm.DefineInitialState('a')
      sm.DefineTransition(a, a)

      walker = sm.Start()
      self.assertTrue(walker.MoveTo(a))
      self.assertEquals(a, walker.GetState())


if __name__ == '__main__':
    unittest.main()
