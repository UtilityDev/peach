import json
import sys
import os
from colorama import Fore, Back, Style, colorama_text
from random_emoticon import get_emoticon

# syntax for creating environment
create_syntax = ['create', '-c']

# expected number of arguments1
expected_args = 4

languages = []

# opens json file for reading
f = open('options.json')
data = json.load(f)

# throws error
def throw_err(txt, clr=Fore.RED):
    print(f"{clr}{get_emoticon()} whoops, {txt} {get_emoticon()}")
    print(Fore.RESET)

# function for thro_
# checks if we have enough arguments
def check_args():
    if len(args) != expected_args:
        throw_err(f"got {str(len(args))} arguments but expected {str(expected_args)}!")
        return False
    else:
        return True

# gets the file extension for the given language
def get_extension(language):
    language = language.lower()

    for lang in data['languages']:
        if lang['name'].lower() == language:
            return lang['extension']

def create_file(name, content=''):
    f = open(name, 'w') ; f.write(content) ; f.close()
    return f

# creates a folder with the given name at the given location
# and creates a file for the chosen programming language
def create_environment(name, location, language, git=False):
    # checks if the path exists
    if os.path.exists(location):
        # changes directory to that path
        os.chdir(location)

        # creates file with the given filename
        os.mkdir(name)

        # change path to the given path
        os.chdir(os.path.join(name))

        # creates main file in the given directory
        create_file(f'main.{get_extension(language)}')

        # generate git boilerplate files
        if git:
            create_file('.gitignore')
            create_file('README.md')

        # printing success message
        print(Fore.GREEN + language.title() + " environment successfully generated! (☞ﾟヮﾟ)☞") ; print(Fore.RESET)
    else:
        # if the path does NOT exist, throw an error
        throw_err(location + " is not a valid path!")

args = sys.argv # just so I don't have to type 'sys.argv' all the time, hehe
use_git = False # if we want to generate git boilerplate or not
def main():
    # loops through every language in the json file
    # and lowers the names
    for lang in data['languages']:
        languages.append(lang['name'].lower())

    # if we have the right amount of arguments
    if check_args() is True:
        # if we have '-c' or 'create' as an argument
        if args[1].lower() in create_syntax:
            # if the language we entered is a valid language
            if args[2].lower() in languages:
                # sets the chosen language to the language we entered in
                use_git = args[3].lower() == '--use-git'

                chosen_language = args[2]
                print("✨ Creating a " + chosen_language.title() + " masterpiece! ✨")

                # asks user for folder name and location (to be used in create_environment function)
                try:
                    folder_name = str(input('Project name: '))
                    folder_loc = str(input("Where do you want to place your project? (full path): "))

                    # checking if we actually entered in a name or not
                    if folder_name != '':
                        create_environment(folder_name, folder_loc, chosen_language, use_git)
                    else:
                        throw_err('project name cannot be empty!')
                except KeyboardInterrupt:
                    print('\n')
                    throw_err('interrupted!!')
            else:
                # throws an error if we haven't chosen a valid language
                throw_err("that language doesn't exist!")

if __name__ == '__main__':
    main()