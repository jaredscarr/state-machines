# State Machines

### Installation

1. `python3 -m venv venv`
2. [Activate your environment](https://docs.python.org/3.9/library/venv.html?highlight=venv)
3. `python3 -m pip install --upgrade pip`
4. `pip install -r requirements.txt`

### Verify ###

`python3 cli.py --help`

### Basic Commands

`python3 cli.py --help`

**Deterministic Finite Acceptor**

`python3 cli.py --input <replace with input>`

**Non-deterministic Finite Acceptor**

`python3 cli.py --input <replace with input> --type nfa`

This acceptor has multiple possible state outcomes determined at random so this tool offers an
option to test input that may sometimes be considered valid and other times invalid. For example,
provided the input _aabb_ this could end up in q0, q1, or q3. The test option allows for the
most optimistic path thus proving that this input could possibly be valid. In this case, since
the length of the input is > 3 it will hold the state in q0 until the length of the unprocessed
input is 3. At this point it will attempt to push the state to q1 (seed random). If the input is
valid it will move forward. If it continues to be valid as it processes then it will end up in a
valid terminal state.

`python3 cli.py --input <replace with input> --type nfa --test`

### Run Tests

`python -m pytest`
