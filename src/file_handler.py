import os

class FileHandler():
    def save_to_file(self, file_path: str, password: str) -> str:
        """Saves the password into a file

        Args:
            file_path (str): filepath / filename where to save the password
            password (str): password to save

        Raises:
            IOERROR: If saving produces error
            
        Returns:
            str: Returns message to display in GUI
        """ 
        if not file_path:
            raise ValueError('Filepath is mandatory')
        if not password:
            raise ValueError('Nothing to save yet')
        
        file_type = os.path.splitext(file_path)[1]
        if not file_type:
            file_path += '.txt'
            
        try:
            with open(file_path, 'a', encoding="utf-8") as f:
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    f.write('\n')
                f.write(password)
            return f"Password saved in {file_path}"
        except IOError as e:
            raise IOError(f"Error saving file: {str(e)}")