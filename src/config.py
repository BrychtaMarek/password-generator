class Config():
    # Minimum pwd length is 4, else the program will not work correctly
    MIN_PASSWORD_LENGTH = 4
    MAX_PASSWORD_LENGTH = 50
    PASSWORD_LENGTH_RATING = {'joke': 1, 'weak': 6, 'moderate': 10, 'strong': 16}
    SEQUENCE_LENGTH = 3
    PASSWORD_BREACH_CHECK_API = 'https://api.pwnedpasswords.com/range/'     