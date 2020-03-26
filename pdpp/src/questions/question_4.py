import questionary
from questionary import Separator, Choice, prompt
from click import clear as click_clear
from os.path import isdir
from os import listdir, walk

def q4(source_code, custom_style_fancy):


    click_clear()

    language_list = []

    for entry in source_code:
        if entry[-3:] == '.py':
            language_list.append('Python')
        elif entry[-2:] == '.R' or entry[-2:] == '.r':
            language_list.append('R')
        else:
            language_list.append('???')


    if len(set(language_list)) != 1 or '???' in language_list:
        
        message = ("""
        Note that pdpp does not currently support steps that 
        contain scripts written in more than one programming language.

        If this step contains source code from multiple languages,
        please separate all source code written in dissimilar 
        languages into different steps. 

        If all of this step's source code is written in the same
        pdpp-supported language, you can indicate the appropriate
        language below.

        Select the programming language used:
        """)
        
        question_4 = [{
            'type': 'list',
            'name': 'language',
            'message': message,
            'choices': [
                {
                    'name': 'Python'
                },
                {
                    'name': 'R'
                }
            ],
        }]

        return prompt(question_4, style=custom_style_fancy)["language"]

    else:
        return language_list[0]
    
