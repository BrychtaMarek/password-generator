from decimal import ROUND_HALF_DOWN, Decimal
from zxcvbn import zxcvbn
from src.config import Config
import hashlib
import string
import requests



class PasswordEvaluator():
    """Initializes PasswordEvaluator
    """    
    def __init__(self) -> None:
        
        self.PASSWORD_LENGTH_RATING = Config.PASSWORD_LENGTH_RATING
        self.SEQUENCE_LENGTH = Config.SEQUENCE_LENGTH
        self.PASSWORD_BREACH_CHECK_API = Config.PASSWORD_BREACH_CHECK_API        
        
    def external_password_evaluation(self, password: str) -> int:
        """Evaluates password by the external library

        Args:
            password (str): password to be evaluated
            
        Raises:
            ValueError: if password is empty

        Returns:
            int: rounded score: int(1 - 4)
        """
        if not password:
            raise ValueError('Empty password')        
        # Get the external library result
        result = zxcvbn(password=password)
        # Take only the score from result
        score = float(result['score'])
        # Return rounded score
        return Decimal(score).to_integral_value(rounding=ROUND_HALF_DOWN)      
    
    def internal_password_evaluation(self, password: str) -> int:
        """Evaluates the password by the internal algorithm

        Args:
            password (str): password to be evaluated

        Returns:
            int: rounded score: int (1 - 4)
        """        
        criteria_scores = {}
        # Calculate password scores for multiple criteria
        criteria_scores['length'] = self.evaluate_length(len(password)) * 6 # Length is more important
        criteria_scores['repetition'] = self.evaluate_repetition(password)
        criteria_scores['variety'] = self.evaluate_variety(password) * 2
        criteria_scores['sequence'] = self.evaluate_sequence(password)
        
        print(criteria_scores)
        # Calculate average score
        score = sum(criteria_scores.values()) / (float(len(criteria_scores)) + 6) # + 6 because of added weights
        print(f'Score {score}' )
        if score < 2:
            return 1
        # Return rounded average score
        return Decimal(score).to_integral_value(rounding=ROUND_HALF_DOWN)    
    
    def is_breached(self, password: str) -> bool:
        """check if the password is known to be breached on Have I been pwned site

        Args:
            password (str): password to check

        Raises:
            ValueError: if the password is empty
            ConnectionError: if the response code is not 200 and password cannot be checked

        Returns:
            bool: True if the password is breached
        """        
        if not password:
            raise ValueError('Empty password')
        # Encode password to be able to encrypt the password
        password_encoded = password.encode('utf-8')
        # Encrypt password for the comparison of hash prefix
        encryption = hashlib.sha1(password_encoded)
        hash = encryption.hexdigest().upper()
        hash_prefix = hash[0:5]
        # request hashes with the same hash prefix from Have I been pwned? site
        try:
            response = requests.get(self.PASSWORD_BREACH_CHECK_API + hash_prefix)
            if response.status_code == 200:
                # Iterate through the returned hashes and compare with our hash
                for line in response.iter_lines(decode_unicode=True):
                    # If our hash is equal to returned hash, password is breached
                    if (hash_prefix + line.split(':')[0]) == hash:
                        return True              
                else:
                    return False
        except ConnectionError:
            raise ConnectionError('Connection Error')

    def evaluate_length(self, password_length: int) -> int:
        """Evaluates password length based on the configuration of evaluator

        Args:
            password_length (int): Length of the password

        Returns:
            score: int (1 - 4)
        """        
        if password_length >= self.PASSWORD_LENGTH_RATING['strong']:
            return 4
        elif password_length >= self.PASSWORD_LENGTH_RATING['moderate']:
            return 3
        elif password_length > self.PASSWORD_LENGTH_RATING['weak']:
            return 2
        else:
            return 1
        
    def evaluate_repetition(self, password: string) -> int:
        """Evaluates the password from the character repetition criteria, the score is lower if character is repeated too much

        Args:
            password (string): password to be evaluated

        Returns:
            int: score: int (1 - 4)
        """        
        length = len(password)
        # Calculate the occurence for each char
        characters = {}
        for char in password:
            if char not in characters:
                characters[char] = 1
            else:
                characters[char] += 1
                
        # Get the maximum occurence value        
        max_repetitions = max(characters.values())
        
        # Calculate the score based on the maximum occurence of single character
        if max_repetitions >= length / 1.3:
            return 1
        if max_repetitions >= length / 1.6:
            return 2
        if max_repetitions >= length / 2:
            return 3
        else:
            return 4

    def evaluate_variety(self, password: string) -> int:
        """Evaluates the password by the variety of character types, the score is lower if there is less character types

        Args:
            password (string): password to be evaluated

        Returns:
            int: score: int (1 - 4)
        """        
        contains_lower = False
        contains_upper = False
        contains_digit = False
        contains_special = False
        
        # Count the character types used in password
        for char in password:
            if char in string.ascii_lowercase:
                contains_lower = 1
            elif char in string.ascii_uppercase:
                contains_upper = 1
            elif char in string.digits:
                contains_digit = 1
            elif char in string.punctuation:
                contains_special = 1
        
        # Calculate score        
        score = contains_lower + contains_upper + contains_digit + contains_special
        
        return score

    def evaluate_sequence(self, password: string) -> int:
        """Evaluates the password by the criteria of containing character sequences, if there are long sequences of characters, the score is lower

        Args:
            password (string): password to be evaluated

        Returns:
            int: score: int (1 - 4)
        """        
        pwd_length = len(password)
        
        # Store the number of detected sequences
        sequences = 0
        # Length of the longest sequence detected
        longest_sequence = 0

        # Iterate through password and detect sequences
        # Do this twice for original password and for reversed password (to check reverse sequence e.g. 98765)
        for _ in range(2):
            # Previous character to detect the sequence for current character
            previous_character = ''
            # Currently detected sequence
            sequence = ''
            # For second iteration, check the sequence from reversed password
            if _ == 1:
                password = password[::-1]
            index = 2
            for char in password:
                if not previous_character:
                    previous_character = char
                    continue
                # Compare ascii values of previous and current character, if the difference is 1, there is a sequence
                if ord(char) - 1 == ord(previous_character):
                    # Add also previous character if sequence is starting
                    if not sequence:
                        sequence = previous_character
                    # Add character to the current detected sequence
                    sequence += char
                    # Reassign previous character for the next iteration
                    previous_character = char
                    # Based on configuration, if the current length of the detected sequence characters equals to the configured length of sequence, raise the number of sequences
                    if len(sequence) == self.SEQUENCE_LENGTH:
                        sequences += 1
                    # If we are at the end of string, we have to save the sequence length
                    if index == len(password):
                        if len(sequence) > longest_sequence:
                            longest_sequence = len(sequence)
                    index += 1
                # Sequence finished
                else:
                    previous_character = char
                    # Store the length of the detected sequence if its the new longest
                    if len(sequence) > longest_sequence:
                        longest_sequence = len(sequence)
                    # Reset the sequence of characters
                    sequence = ''
                    index += 1
           
        if longest_sequence == pwd_length:
            return 1
        elif longest_sequence >= pwd_length / 2:
            return 2
        elif longest_sequence > pwd_length / 3:
            return 3
        else:
            return 4    
