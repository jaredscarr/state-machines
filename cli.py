"""
CLI for state machine code for Fundamentals of Computer Science
for Professor Eric Lloyd.

DFA language: (a+b)c*
NFA language: (a | b)*abb
"""
from __future__ import annotations
import random
import click


class State:
    """State Class."""
    def handle_event(self, event: str, **kwargs) -> State:
        """Return next state or None."""
        pass

    def __str__(self) -> str:
        """Return the name of this State class."""
        return self.__class__.__name__

    def __eq__(self, other: State) -> bool:
        """Override default equality."""
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


# DFA Class Group Q0 - Q2
class Q0(State):
    """Start state. If the input is 'a' or 'b' return the next state otherwise return None."""
    def handle_event(self, event: str) -> State:
        """Return next state or None."""
        if event == 'a' or event == 'b':
            return Q1()


class Q1(State):
    """If the event is 'c' then return the next state otherwise return None."""
    def handle_event(self, event: str) -> State:
        if event == 'c':
            return Q2()


class Q2(State):
    """
    Final state. As long as the input continues to be a 'c' stay in this state.
    Otherwise return None.
    """
    def handle_event(self, event: str) -> State:
        if event == 'c':
            return self


# NFA Class Group
class NFAQ0(State):
    """
    Start state.
    If string is empty stay in this state.
    If event is 'a' or 'b' move to next state.
    Otherwise return None.

    If testing then this behavior is controlled with seeding.
    """
    def handle_event(self, event: str, **kwargs) -> State:
        if kwargs and 'test' in kwargs:
            if 'seed' in kwargs:
                random.seed( kwargs['seed'] )
            else:
                random.seed(0)
        if event == " " or event == 'b':
            return self
        if event == 'a':
            state_choice = random.randint(1, 2)
            if state_choice == 1:
                return self
            if state_choice == 2:
                return NFAQ1()


class NFAQ1(State):
    """Next state."""
    def handle_event(self, event: str, **kwargs) -> State:
        if event == 'b':
            return NFAQ2()


class NFAQ2(State):
    def handle_event(self, event: str, **kwargs) -> State:
        """If the event is 'b' return the next state or return None."""
        if event == 'b':
            return NFAQ3()


class NFAQ3(State):
    def handle_event(self, event: str, **kwargs) -> State:
        """If there is another event at this point the input is invalid."""
        return


class StateMachine:
    """State machine logic."""
    def dfa(self, input: str) -> bool:
        """Run the DFA with language: (a+b)c*"""
        if input == '':
            click.echo('Invalid')
            return False
        start = Q0()
        next_state = start.handle_event(input[0])
        # check the first state is valid
        if not next_state:
            click.echo('Invalid')
            return False
        # loop through the rest of the input
        for ch in input[1:]:
            next_state = next_state.handle_event(ch)
            if not next_state:
                click.echo('Invalid')
                return False

        if next_state != Q2():
            click.echo('Invalid')
            return False
        click.echo('Valid')
        return True

    def nfa(self, input: str, test: bool):
        """
        Run the NFA with language: (a | b)*abb
        For the sake of simplicity this will select
        a random choice given multiple state results.
        """
        if input == '':
            click.echo('Invalid')
            return False
        
        start = NFAQ0()
        next_state = start.handle_event(input[0], test=test, seed=1 if test and len(input) > 3 else 0)
        # check the first state is valid
        if not next_state:
            click.echo('Invalid')
            return False

        for i, ch in enumerate(input[1:]):
            # For testing this forces the input into q0 until released when input reaches length of 3
            # then will allow it a chance to move to q1 if appropriate
            # this allows for testing of inputs that should be valid but may not always be valid
            if test and len(input) - (i + 1) > 3:
                next_state = next_state.handle_event(ch, test=test, seed=1)   
            else:
                next_state = next_state.handle_event(ch, test=test)
            if not next_state:
                click.echo('Invalid')
                return False
        if next_state != NFAQ3():
            click.echo('Invalid')
            return False
        click.echo('Valid')
        return True


@click.command()
@click.option('--input', required=True, help='Enter input to send to dfa for validation.')
@click.option(
    '--type', 
    type=click.Choice(['dfa', 'nfa'],
    case_sensitive=False),
    default='dfa',
    help='Defaults to DFA.'
)
@click.option(
    '--test/--not-test',
    help='For NFA only Forces behavior to be that it will loop in q0\n' +
    'until reaching the final 3 characters of input\n' + 
    'and will then will attempt to push into q1.'
)
def run(input: str, type: str, test: bool) -> bool:
    """
    State Machine Simulator.\n
        DFA with language: (a+b)c*\n
        NFA with language: (a | b)*abb\n
    """
    machine = StateMachine()
    if type.upper() == 'DFA':
        return machine.dfa(input)
    if type.upper() == 'NFA':
        return machine.nfa(input, test)


if __name__ == '__main__':
    run()
