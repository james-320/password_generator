import configparser
import os
import random

class PwGenerator:
    """ 
    A class to define a password generator. The generator is configurable via
    a settings.txt file which is read each time the script is run.

    SETTINGS
    --------
    num_of_words
    min_word_length
    max_word_length
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.punctuation = '.'
        self.config_values = {'min_word_length' : 5,
                              'max_word_length' : 10,
                              'number_of_words' : 2,
                              'number_of_digits' : 2,
                              'number_of_punctuation' : 2,
                              'number_of_passwords' : 5
                              }

    def run(self):
        print(' ------------------------- ')
        print('|Secure Password Generator|')
        print(' ------------------------- \n')
        self.configure_generator()
        self.clean_wordlist()
        self.write_passwords()
        print()

    def input_settings_choice(self, text):
        # User input to modify settings or not.
        while True:
            change_choice = input(text)
            try:
                if change_choice.upper() == 'Y' or 'N':
                    change_choice = change_choice.upper()
                    return change_choice
            except Exception as e:
                print(e)

    def input_number(self, text):
        # User input to modify settings or not.
        while True:
            num = input(text)
            try:
                num = int(num)
                if num > 0:
                    return num
            except Exception as e:
                print(e)
    
    def configure_generator(self):
        """Accesses settings.txt and updates config options."""
        # Automatic load of last used settings.
        if os.path.isfile('settings.txt'):
            self.config.read('settings.txt')
            # Update object with last_used values.
            for k in self.config['last_used']:
                self.config_values[k] = int(self.config['last_used'][k])
            print('Previous settings restored successfully.\n')
        
        # User manual entry of settings.
        if self.input_settings_choice(
        'Would you like to modify the default settings Y|N? '
        ) == 'Y':
            self.config_values['min_word_length'] = (
                self.input_number(
                    '\nEnter the minimum number of characters in each word: '
                )
            )
            self.config_values['max_word_length'] = (
                self.input_number(
                    'Enter the maximum number of characters in each word: '
                )
            )
            self.config_values['number_of_words'] = (
                self.input_number(
                    'Enter the number of words to be included: '
                )
            )
        
        # Update last_used values.
        for k in self.config_values:
            self.config['last_used'][k] = str(self.config_values[k])
        with open('settings.txt', 'w') as configfile:
            self.config.write(configfile)
        

    def clean_wordlist(self):
        with open('words.txt') as infile:
            with open('words_cleaned.txt', 'w') as outfile:
                for line in infile:
                    if (len(line) - 1 >= self.config_values['min_word_length']
                    and len(line) - 1 <= self.config_values['max_word_length']
                    and line[:-2].isalpha()):
                        outfile.write(line.lower())

    def generate_pw(self):
        password = ''
        # PW begins with a set number of random digits.
        for i in range(self.config_values['number_of_digits']):
            password += str(random.randint(0, 9))
        # Add a set number of random words.
        with open('words_cleaned.txt') as infile:
            words = infile.readlines()
            password += random.choice(words).strip('\n').title()
            for i in range(self.config_values['number_of_words'] - 1):
                password += random.choice(words).strip('\n')
        # Add a set number of punctuation characters.
        password += '.' * self.config_values['number_of_punctuation']

        self.password = password

    def write_passwords(self):
        print('\nYour Passwords Are:')
        print('-------------------\n')
        with open('passwords.txt', 'w') as outfile:
            for i in range(self.config_values['number_of_passwords']):
                self.generate_pw()
                outfile.write(self.password + '\n')
                print(self.password)


# Main code
if __name__ == "__main__":
    pw_gen = PwGenerator()
    pw_gen.run()