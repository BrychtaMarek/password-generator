from tkinter import *
from tkinter import ttk
from os import path
from src.config import Config
from src.password_generator import PasswordGenerator
from src.password_evaluator import PasswordEvaluator
from src.file_handler import FileHandler
class PasswordGeneratorGUI():
    def __init__(self, root: Tk, title: str) -> None:
        self.root = root
        self.root.title(title)
        
        self.password_generator = PasswordGenerator()
        self.password_evaluator = PasswordEvaluator()
        self.file_handler = FileHandler()

        # Main frame
        self.mainframe = ttk.Frame(root, padding = '3 3 12 12')
        self.mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(0, weight = 1)

        # GUI Variables
        self.generated_password = StringVar(value='')
        self.file = StringVar()
        self.length = StringVar()
        self.lower = BooleanVar(value=True)
        self.upper = BooleanVar()
        self.digits = BooleanVar()
        self.special = BooleanVar()
        self.check_breached = BooleanVar()
        self.pwd_evaluation_method = StringVar(value='internal')
        
        # Add listener to password input to trigger evaluation
        self.generated_password.trace_add('write', self.evaluate_password)
        # Add listener to file input
        self.generated_password.trace_add('write', self.validate_save_input)
                
    def create_widgets(self):
        # Generate password
        self.btn_generate = ttk.Button(self.mainframe, text='Generate password', width=36, command=lambda: self.generated_password.set(self.password_generator.generate_password(int(self.length.get()), self.digits.get(), self.upper.get(), self.lower.get(), self.special.get())))
        self.btn_generate.grid(column=2, row=1, sticky=(W))
        self.btn_generate.state(['disabled'])
        self.txt_generated_password = ttk.Entry(self.mainframe, width=36, textvariable=self.generated_password)
        self.txt_generated_password.grid(column=2, row=2, sticky=(W))       
        # Copy to clipboard
        self.btn_clipboard = ttk.Button(self.mainframe, width=36, text='Copy to clipboard', command=self.copy_to_clipboard)
        self.btn_clipboard.grid(column=2, row=3, sticky=(W)) 
        self.lbl_clipboard = ttk.Label(self.mainframe, text='')
        self.lbl_clipboard.grid(column=3, row=3, sticky=(W))
        # Validation text
        self.parameter_validation_label = ttk.Label(self.mainframe, text='',)
        self.parameter_validation_label.grid(column=3, row=1, sticky=(W, N))    
        # Breach info
        self.breach_info = ttk.Label(self.mainframe, text='')
        self.breach_info.grid(column=4, row=2, sticky=(W, S))   
        # Save to file
        self.txt_file = ttk.Entry(self.mainframe, validatecommand=(self.root.register(self.validate_save_input), '%P'), validate='key', textvariable=self.file, width=36).grid(column=2, row=5, sticky=(W))
        self.btn_save = ttk.Button(self.mainframe, text='Save pwd to file', width=36,command=lambda: self.save_password())
        self.btn_save.grid(column=2, row=4, sticky=(W))
        self.validate_file_save = ttk.Label(self.mainframe, text='')
        self.validate_file_save.grid(column=3, row=5, sticky=(W))
        self.btn_save.state(['disabled'])   
        # Password evaluation
        self.lbl_password_evaluation = ttk.Label(self.mainframe, text='')
        self.lbl_password_evaluation.grid(column=3, row=2, sticky=(W))    
        # User parameters
            # Length
        self.length_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.length, validatecommand=(self.root.register(self.validate_length), '%P'), validate='key')
        self.length_entry.grid(column=1, row=1, sticky=(E))
        self.length_label = ttk.Label(self.mainframe, text='Password length')
        self.length_label.grid(column=1, row=1, sticky=(W))
            # Include options
        self.check_lower = ttk.Checkbutton(self.mainframe,width=40, variable=self.lower, text='Include lower case symbols').grid(column=1, row=2, sticky=(W))
        self.check_upper = ttk.Checkbutton(self.mainframe, variable=self.upper, text='Include upper case symbols').grid(column=1, row=3, sticky=(W))
        self.check_digits = ttk.Checkbutton(self.mainframe, variable=self.digits, text='Include numbers').grid(column=1, row=4, sticky=(W))       
        self.check_special = ttk.Checkbutton(self.mainframe, variable=self.special, text='Include special symbols').grid(column=1, row=5, sticky=(W))
            # Check pwd breach
        self.btn_check_breach = ttk.Checkbutton(self.mainframe, variable=self.check_breached, text='Check the password breach').grid(column=1, row=6, sticky=(W))
            # Evaluation algorithms radio
        self.lbl_evaluation_method = ttk.Label(self.mainframe, text='Way of password evaluation')
        self.lbl_evaluation_method.grid(column=1, row=7, sticky=(W))
        self.radio_internal_pwd_evaluation = ttk.Radiobutton(self.mainframe, text='Internal', variable=self.pwd_evaluation_method, value='internal')
        self.radio_internal_pwd_evaluation.grid(column=1, row=8, sticky=(W))
        self.radio_external_pwd_evaluation = ttk.Radiobutton(self.mainframe, text='Third party', variable=self.pwd_evaluation_method, value='external')
        self.radio_external_pwd_evaluation.grid(column=1, row=8, sticky=(E))
        
        # Bind enter to generate button
        self.root.bind('<Return>', lambda event: self.btn_generate.invoke())
        # Default focus on length input
        self.length_entry.focus()
        
    def validate_length(self, length: str) -> bool:
        """Validates the length input and shows validation message to user

        Args:
            length (str): length input value

        Returns:
            bool: Always returns True to keep validation running all the time
        """     
        # Do not show validation message if length is a number in valid range
        if (length.isdigit() and int(length) in range(Config.MIN_PASSWORD_LENGTH, Config.MAX_PASSWORD_LENGTH + 1)):
            self.length_label.config(
                text='Password length',
                foreground='black'
                )
            # Enable generate button
            self.btn_generate.state(['!disabled'])
            # Return True to still keep validating
            return True
        # Show validation message if length is out of allowed range
        elif (length.isdigit() and (int(length) < Config.MIN_PASSWORD_LENGTH or int(length) > Config.MAX_PASSWORD_LENGTH)):
            self.length_label.config(
                text=f'Length must be between {Config.MIN_PASSWORD_LENGTH} and {Config.MAX_PASSWORD_LENGTH}',
                foreground='red'
                )
            # Keep generate button disabled until valid range is given
            self.btn_generate.state(['disabled'])
            # Return True to still keep validating
            return True
        # Length must be a number
        else:
            self.length_label.config(
                text=f'Length must be a number',
                foreground='red'
                )
            # Keep the button disabled if number is not given
            self.btn_generate.state(['disabled'])
            # Return True to still keep validating
            return True
    
    def evaluate_password(self, *args: tuple) -> bool:
        """Displays the password evaluation to the user

        Returns:
            bool: Always returns True to keep validating
        """  
        password = self.generated_password.get()      
        if not password:
            return True
        # Check if password is breached if needed    
        if self.check_breached.get():
            try:
                if self.password_evaluator.is_breached(password):
                    self.breach_info.configure(text='Password is breached, do not use', foreground='red')
                    return True
            except ConnectionError:
                self.breach_info.configure(text='Could not connect to Have I been pwned api', foreground='orange')
                return True
        
        # Determine evaluation method
        if self.pwd_evaluation_method.get() == 'internal':
            result = self.password_evaluator.internal_password_evaluation(password)
        else:
            result = self.password_evaluator.external_password_evaluation(password)
                    
        # Display evaluation text on GUI    
        if result == 4:
            self.lbl_password_evaluation.configure(text='Strong', foreground='green')
        elif result == 3:
            self.lbl_password_evaluation.configure(text='Moderate', foreground='black')
        elif result == 2:
            self.lbl_password_evaluation.configure(text='Weak', foreground='orange')
        elif result == 1:
            self.lbl_password_evaluation.configure(text='Not a password', foreground='red')
        return True
        
    def add_style(self) -> None:
        """adds general styling to Tkinter GUI
        """        
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx = 5, pady = 5)
            
    def validate_save_input(self, file_path: str, *args: tuple) -> bool:
        """Validates the save to file input
        
        Args:
            file_path (str): file input value
            *args (tuple): tkinter trace_add arguments

        Returns:
            bool: Returns True to keep validating
        """   
        
        password = self.generated_password.get() 
        # Validation for saving file
        if not file_path:
                self.validate_file_save.configure(text='File name / path is mandatory', foreground='red')
                self.btn_save.configure(state=['disabled'])
                return True
        elif not password:
                self.validate_file_save.configure(text='Generate or type password first', foreground='red')
                self.btn_save.configure(state=['disabled'])
                return True
        else:
            self.btn_save.configure(state=['!disabled'])
            self.validate_file_save.configure(text='', foreground='black') 
            return True
        
    def save_password(self) -> bool:
        """Saves password

        Returns:
            bool: True if file was successfully saved
        """   
        
        file_path = self.file.get()
        password = self.generated_password.get() 
        
        try:
        # Save file and show success msg
            message = self.file_handler.save_to_file(file_path, password)
            self.validate_file_save.configure(text=message, foreground='green')
            return True
        # Show error to user
        except (ValueError, IOError) as e:
            self.validate_file_save.configure(text=str(e), foreground='red')
            return False  
        
    def copy_to_clipboard(self) -> None:
        """Copies the value of generated password to clipboard
        """  
        # First clear clipboard and then append the actual input value      
        self.root.clipboard_clear()
        self.root.clipboard_append(self.txt_generated_password.get().rstrip())
        self.lbl_clipboard.configure(text='Copied!', foreground='green')
        