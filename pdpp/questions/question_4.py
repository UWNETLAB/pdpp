from questionary import prompt
from click import clear as click_clear
from pdpp.styles.prompt_style import custom_style_fancy
from pdpp.pdpp_class_base import BasePDPPClass
from pdpp.languages.language_enum import Language

def q4(task: BasePDPPClass) -> str:
    """
    This question is used to determine the language of the source code this step will run. 
    This needs documentation badly, because I'm not entirely certain what it does at the moment.
    
    """

    click_clear()

    extension_list = []

    for entry in task.src_files:
        extension_list.append(str(entry).split('.')[-1].lower())

    language_list = []

    for entry in extension_list:
        if entry == 'py':
            language_list.append(Language.PYTHON.value)
        elif entry == 'r' or entry == 'rscript':
            language_list.append(Language.R.value)
        else:
            language_list.append('???')


    if len(set(language_list)) != 1 or '???' in language_list:
        
        message = ("""Note that pdpp does not currently support automating tasks that 
        contain scripts written in more than one programming language.

        If this step contains source code from multiple languages,
        please separate all source code written in dissimilar 
        languages into different steps. 

        If all of this step's source code is written in the same
        pdpp-supported language, you can indicate the appropriate
        language below.

        If the programming language you would like to use is not 
        indicated below, or you would like to use more than one programming 
        language in the same step, consider creating a custom pdpp step using
        the 'pdpp custom' command. 

        Select the programming language used:
        """)
        
        question_4 = [{
            'type': 'list',
            'name': 'language',
            'message': message,
            'choices': [
                {
                    'name': Language.PYTHON.value
                },
                {
                    'name': Language.R.value
                }
            ],
        }]

        return prompt(question_4, style=custom_style_fancy)["language"]

    else:
        return language_list[0]
    
