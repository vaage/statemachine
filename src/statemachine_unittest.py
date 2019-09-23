
import unittest

from statemachine import StateMachine

class StateMachineTests(unittest.TestCase):
    def test_starts_in_initial_state(self):
        state_machine = StateMachine()
        state_a = state_machine.define_initial_state('a')
        state_b = state_machine.define_state('b')

        state_machine.define_transition(state_a, state_b)

        walker = state_machine.start()
        self.assertEqual(state_a, walker.get_state())

    def test_accepts_move_with_transition(self):
        state_machine = StateMachine()
        state_a = state_machine.define_initial_state('a')
        state_b = state_machine.define_state('b')

        state_machine.define_transition(state_a, state_b)

        walker = state_machine.start()
        self.assertTrue(walker.move_to(state_b))
        self.assertEqual(state_b, walker.get_state())

    def test_rejects_move_without_transition(self):
        state_machine = StateMachine()
        state_a = state_machine.define_initial_state('a')
        state_b = state_machine.define_state('b')
        state_c = state_machine.define_state('c')

        state_machine.define_transition(state_a, state_b)
        state_machine.define_transition(state_b, state_c)

        walker = state_machine.start()
        self.assertFalse(walker.move_to(state_c))
        self.assertEqual(state_a, walker.get_state())

    def test_rejects_move_to_self_without_transition(self):
        state_machine = StateMachine()
        state_a = state_machine.define_initial_state('a')
        state_b = state_machine.define_state('b')

        state_machine.define_transition(state_a, state_b)

        # There is no transition from a to a, so move_to() should return false,
        # however we should still be in state a after.
        walker = state_machine.start()
        self.assertFalse(walker.move_to(state_a))
        self.assertEqual(state_a, walker.get_state())

    def test_accept_move_to_self_with_transition(self):
        state_machine = StateMachine()
        state_a = state_machine.define_initial_state('a')
        state_machine.define_transition(state_a, state_a)

        walker = state_machine.start()
        self.assertTrue(walker.move_to(state_a))
        self.assertEqual(state_a, walker.get_state())


if __name__ == '__main__':
    unittest.main()
