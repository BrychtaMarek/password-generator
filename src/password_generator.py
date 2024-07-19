

import random
import string
from src.config import Config


class PasswordGenerator():
    def __init__(self) -> None:   
        """Initializes Password generator
        """           
        self.MIN_PASSWORD_LENGTH = Config.MIN_PASSWORD_LENGTH
        self.MAX_PASSWORD_LENGTH = Config.MAX_PASSWORD_LENGTH
        
    def validate_parameters(self, length: int, *included_char_types: bool) -> bool:
        """Validates parameters selected by the user

        Args:
            length (int): password length
            included_char_types (bool): character types required to be present in password - minimum 1

        Returns:
            [bool]: true if the parameter combination is valid
        """ 
        # Password must be between min and max length and contain at least 1 char type       
        if length >= self.MIN_PASSWORD_LENGTH and length <= self.MAX_PASSWORD_LENGTH and any(included_char_types):
            return True
        else:
            return False    
    
    def generate_password(self, length: int = 8, include_digits: bool = False, include_upper: bool = False, include_lower: bool = True, include_special_chars: bool = False) -> str:
        """Generates the password based on user selected parameters

        Args:
            length (int, optional): Required password length. Defaults to 8.
            include_digits (bool, optional): If digits are required in password. Defaults to False.
            include_upper (bool, optional): If Upper characters are required in password. Defaults to False.
            include_lower (bool, optional): If Lower characters are required in password. Defaults to True.
            include_special_chars (bool, optional): If special characters are required in password. Defaults to False.

        Raises:
            ValueError: Returns ValueError when given parameters are invalid

        Returns:
            str: Generated password which complies to parameters given by user
        """ 
        # Validate parameters given by user      
        if not self.validate_parameters(length, include_digits, include_lower, include_special_chars, include_upper):
            raise ValueError('Invalid combination of parameters')
        else:
            # List of all characters to generate from
            characters_to_use = []
            # List of the randomly selected characters which must be included
            required_characters = []

            # Add values to the lists
            if include_digits:
                digits = string.digits
                characters_to_use += digits
                required_characters.append(random.choice(digits))
            if include_upper:
                upper_chars = string.ascii_uppercase
                characters_to_use += upper_chars
                required_characters.append(random.choice(upper_chars))
            if include_lower:
                lower_chars = string.ascii_lowercase
                characters_to_use += lower_chars
                required_characters.append(random.choice(lower_chars))
            if include_special_chars:
                special_chars = string.punctuation
                characters_to_use += special_chars
                required_characters.append(random.choice(special_chars))

            # Select random characters from the charset
            random_characters = [random.choice(characters_to_use) for _ in range(int(length) - len(required_characters))]
            
            # Build final password characters
            password_characters = random_characters + required_characters
            
            # Randomly change the order of pwd characters
            random.shuffle(password_characters)
            
            # Make the password string from the list
            password = ''.join(password_characters)

            return password