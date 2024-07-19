import string
import pytest
from src.config import Config
from src.password_generator import PasswordGenerator

@pytest.fixture
def password_generator():
    return PasswordGenerator()
def test_password_length(password_generator):
    assert len(password_generator.generate_password(length=8)) == 8
    assert len(password_generator.generate_password(length=Config.MIN_PASSWORD_LENGTH)) == 4
    assert len(password_generator.generate_password(length=Config.MAX_PASSWORD_LENGTH)) == 50
    with pytest.raises(ValueError):
        password_generator.generate_password(length=-1)
        password_generator.generate_password(length=Config.MIN_PASSWORD_LENGTH - 1)
        password_generator.generate_password(length=Config.MAX_PASSWORD_LENGTH + 1)
    
def test_parameters(password_generator):
    password = password_generator.generate_password(length=4, include_digits=True, include_lower=True, include_special_chars=True, include_upper=True)
    assert any([c.isdigit() for c in password])
    assert any([c.islower() for c in password])
    assert any([c.isupper() for c in password])
    assert any([c in string.punctuation for c in password])
    
    password = password_generator.generate_password(length=10, include_digits=True, include_lower=False, include_special_chars=True, include_upper=True)
    assert any([c.isdigit() for c in password])
    assert all([not c.islower() for c in password])
    assert any([c.isupper() for c in password])
    assert any([c in string.punctuation for c in password])
    
    password = password_generator.generate_password(length=10, include_digits=True, include_lower=True, include_special_chars=True, include_upper=False)
    assert any([c.isdigit() for c in password])
    assert any([c.islower() for c in password])
    assert all([not c.isupper() for c in password])
    assert any([c in string.punctuation for c in password])
    
    password = password_generator.generate_password(length=10, include_digits=True, include_lower=True, include_special_chars=False, include_upper=True)
    assert any([c.isdigit() for c in password])
    assert any([c.islower() for c in password])
    assert any([c.isupper() for c in password])
    assert all([not c in string.punctuation for c in password])
    
    with pytest.raises(ValueError):
        password_generator.generate_password(length=10, include_digits=False, include_lower=False, include_special_chars=False, include_upper=False)
        
def test_validate_parameters(password_generator):
    assert password_generator.validate_parameters(3, True, True, True, True) == False
    assert password_generator.validate_parameters(51, True, True, True, True) == False
    assert password_generator.validate_parameters(10, False, False, False, False) == False
    assert password_generator.validate_parameters(4, True, False, False, False) == True
    assert password_generator.validate_parameters(50, True, False, False, False) == True
    assert password_generator.validate_parameters(3, True, True, True, True) == False