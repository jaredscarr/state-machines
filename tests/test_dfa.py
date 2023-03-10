import pytest
from click.testing import CliRunner
import cli as cli


runner = CliRunner()


@pytest.mark.parametrize('test_input, expected',
    [
        ('ac', 'Valid'),
        ('bc', 'Valid'),
        ('acc', 'Valid'),
        ('bcc', 'Valid'),
        ('accc', 'Valid'),
        ('bccc', 'Valid'),
        ('bccccccccccccccccccccccc', 'Valid')
    ]
)
def test_valid_input_dfa(test_input, expected):
    response = runner.invoke(cli.run, ['--input', test_input])
    assert response.exit_code == 0
    assert 'Valid' in response.output


@pytest.mark.parametrize('test_input, expected',
    [
        ('a', 'Valid'),
        ('b', 'Valid'),
        ('ab', 'Invalid'),
        ('abc', 'Invalid'),
        ('defg', 'Invalid'),
        ('abccccccd', 'Invalid'),
        ('abcd', 'Invalid'),
        ('ccccccccc', 'Invalid'),
        ('c', 'Invalid')
    ]
)
def test_invalid_input_dfa(test_input, expected):
    response = runner.invoke(cli.run, ['--input', test_input])
    assert response.exit_code == 0
    assert 'Invalid' in response.output


@pytest.mark.parametrize('test_input, expected',
    [
        ('abb', 'Valid'),
        ('aabb', 'Valid'),
        ('babb', 'Valid'),
        ('aaabb', 'Valid'),
        ('bbabb', 'Valid'),
        ('ababb', 'Valid'),
        ('     ababb', 'Valid'),
        (' abbbbbbbbabb', 'Valid'),
    ]
)
def test_valid_input_nfa(test_input, expected):
    response = runner.invoke(cli.run, ['--input', test_input, '--type' ,'nfa', '--test'])
    assert response.exit_code == 0
    assert 'Valid' in response.output


@pytest.mark.parametrize('test_input, expected',
    [
        ('', 'Invalid'),
        (' ', 'Invalid'),
        ('         ', 'Invalid'),
        ('a', 'Invalid'),
        ('b', 'Invalid'),
        ('aaaaabbbbbb      z', 'Invalid'),
        (' aabbc', 'Invalid'),
        ('defg', 'Invalid'),
        ('abccccccd', 'Invalid'),
        ('abcd', 'Invalid'),
        ('ccccccccc', 'Invalid'),
        ('c', 'Invalid'),
        (' abbbbbbbb', 'Valid'),
        (' abbbbbbbba', 'Valid'),
    ]
)
def test_invalid_input_nfa(test_input, expected):
    response = runner.invoke(cli.run, ['--input', test_input, '--type', 'nfa'])
    assert response.exit_code == 0
    assert 'Invalid' in response.output
