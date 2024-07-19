import pytest
from src.password_evaluator import PasswordEvaluator
from src.config import Config

@pytest.fixture
def password_evaluator():
    return PasswordEvaluator()

def test_external_evaluation(password_evaluator):
    assert password_evaluator.external_password_evaluation('AAAA') == 0
    assert password_evaluator.external_password_evaluation('aaaa') == 0
    assert password_evaluator.external_password_evaluation('AAAA1234') == 1
    assert password_evaluator.external_password_evaluation('AaAa_1234') == 2
    assert password_evaluator.external_password_evaluation('abcAaA123###') == 3
    assert password_evaluator.external_password_evaluation('abcAaA123###-----asdsdas') == 4
    with pytest.raises(ValueError):
        password_evaluator.external_password_evaluation('')
        
def test_internal_evaluation(password_evaluator):
    assert password_evaluator.internal_password_evaluation('abcd') == 1
    assert password_evaluator.internal_password_evaluation('a1C*') == 2
    assert password_evaluator.internal_password_evaluation('a1C*zzz') == 3
    assert password_evaluator.internal_password_evaluation('abcd12**CCCC') == 3
    assert password_evaluator.internal_password_evaluation('abcd12**CCCCaabb') == 4
    assert password_evaluator.internal_password_evaluation('abcdefghijk') == 2
    assert password_evaluator.internal_password_evaluation('ABCDEFGH') == 1
    assert password_evaluator.internal_password_evaluation('abcd') == 1
    
def test_is_breached(password_evaluator):
    assert password_evaluator.is_breached('admin') == True
    assert password_evaluator.is_breached('784defwefs221fdc5asd4as6d48496532666') == False
    with pytest.raises(ValueError):
        password_evaluator.is_breached('')
    
def test_evaluate_sequence(password_evaluator):
    assert password_evaluator.evaluate_sequence('abcdefgh') == 1
    assert password_evaluator.evaluate_sequence('abaaabcdef') == 2
    assert password_evaluator.evaluate_sequence('abcdfffff') == 3
    assert password_evaluator.evaluate_sequence('abctttrrrt') == 4
    assert password_evaluator.evaluate_sequence('ABCDEFGH') == 1
    assert password_evaluator.evaluate_sequence('ABAAABCDEF') == 2
    assert password_evaluator.evaluate_sequence('ABCDFFFFF') == 3
    assert password_evaluator.evaluate_sequence('ABCTTTRRRT') == 4
    assert password_evaluator.evaluate_sequence('hgfedcba') == 1
    assert password_evaluator.evaluate_sequence('fedcbaaaba') == 2
    assert password_evaluator.evaluate_sequence('fffffdcba') == 3
    assert password_evaluator.evaluate_sequence('trrrtttcba') == 4
    assert password_evaluator.evaluate_sequence('HGFEDCBA') == 1
    assert password_evaluator.evaluate_sequence('FEDCBAAABA') == 2
    assert password_evaluator.evaluate_sequence('FFFFFDCBA') == 3
    assert password_evaluator.evaluate_sequence('TRRRTTTCBA') == 4
    
def test_evaluate_variety(password_evaluator):
    assert password_evaluator.evaluate_variety('aaaa') == 1
    assert password_evaluator.evaluate_variety('AAAA') == 1
    assert password_evaluator.evaluate_variety('1234') == 1
    assert password_evaluator.evaluate_variety('****') == 1
    assert password_evaluator.evaluate_variety('aaAA') == 2
    assert password_evaluator.evaluate_variety('aa11') == 2
    assert password_evaluator.evaluate_variety('AA11') == 2
    assert password_evaluator.evaluate_variety('**11') == 2
    assert password_evaluator.evaluate_variety('**AA') == 2
    assert password_evaluator.evaluate_variety('**aa') == 2
    assert password_evaluator.evaluate_variety('*Aaa') == 3
    assert password_evaluator.evaluate_variety('*A11') == 3
    assert password_evaluator.evaluate_variety('*a11') == 3
    assert password_evaluator.evaluate_variety('aA11') == 3
    assert password_evaluator.evaluate_variety('a*AA') == 3
    assert password_evaluator.evaluate_variety('aA*1') == 4
    
def test_evaluate_length(password_evaluator):
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['joke']) == 1
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['weak'] - 1) == 1
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['weak']) == 2
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['weak'] + 1) == 2
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['moderate'] - 1) == 2
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['moderate']) == 3
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['moderate'] + 1) == 3
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['strong'] - 1) == 3
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['strong']) == 4
    assert password_evaluator.evaluate_length(Config.PASSWORD_LENGTH_RATING['strong'] + 1) == 4
    
    
def test_evaluate_repetition(password_evaluator):
    assert password_evaluator.evaluate_repetition('aaaaaaaaa') == 1
    assert password_evaluator.evaluate_repetition('aaaaaaabb') == 1
    assert password_evaluator.evaluate_repetition('aaaaaabbb') == 2
    assert password_evaluator.evaluate_repetition('aaaaabbbb') == 3
    assert password_evaluator.evaluate_repetition('aaaabbbbb') == 3
    assert password_evaluator.evaluate_repetition('aaabbbccc') == 4
