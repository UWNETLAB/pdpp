## Overview

pdpp is a command-line tool for Python3.6+ which faciliates automation, collaboration, and analytical reproducibility for academic data science projects.

<br>

## An Inspiring Video

This project found its genesis when the team from [Dr. John McLevey's Netlab][Netlab] ran headlong into the [following video][Ball Video], showing a conference presentation by [Dr. Patrick Ball][Ball].

[![Patrick Ball: Principled Data Processing](https://img.youtube.com/vi/ZSunU9GQdcI/0.jpg)](https://www.youtube.com/ZSunU9GQdcI)

In it, Dr. Ball outlines a set of principles designed to liberate data scientists from the morass of ambiguity, stale documentation, and mutual incomprehensibility that usually stymies their collaborative efforts.

Dr. Ball's recommendations include:

- Breaking data cleaning and analysis processes into a (comparatively) large number of small, discrete 'tasks' and creating a separate directory for each
- Using _GNU Make_ to automate the entire project
- Using accompanying YAML markdown files to contain project constants
- Using a uniform subdirectory structure for each of the task directories:
    - src, which contains all of the source code for the task
    - input, where the scripts in the src subdirectory get their input data from
    - output, where the scripts in the src subdirectory place their outputs
    
Taken together, Dr. Ball's recommendations help the project assume the following qualities:

1. Self-Contained - using small, discrete tasks as the [quanta of your workflow][workflow] means that everything you need to understand how a particular task produces the output that it does can be found in a single directory.
1. Self-Documenting - giving task directories short, descriptive names, permits anyone examing your project can ascertain a rough understanding of what a given task does at a glance.
1. Reproducible - automation allows others to compile your project and produce outputs using an identical set of processes.

<br>

## Implementing Dr. Ball's Workflow in Python 3

Instead of make, we use doit, a python-scripted automation suite.

Because doit uses the term 'task' in a specific way, we have decided to use 'step' to refer to the quanta of our workflow in pdpp

<br>

## Installing pdpp

Once it's on PYPI, that is!

```
pip install pdpp
```

<br>

## A Sample Workflow using pdpp and GNU/Git Bash

(1)
Start by making a project directory on your operating system of choice, and then navigate to it.

```
mkdir ball_test && cd ball_test
```

(2)
Then, in the empty directory, create your first 'step' directory.

```
ball step -s extract_csv
```

(3)
You can see the directory structure that pdpp has implemented (Not all operating systems have the 'tree' command, so if this doesn't work, don't worry about it).

```
tree

.
|-- dodo.py
`-- extract_csv
    |-- dodo.py
    |-- input
    |-- output
    `-- src
```


(4)
You'd normally have some kind of data soruce for your project - deposit it in the input directory inside your first step directory; your source code will access it later.

```
touch extract_csv/input/raw_data.csv
```


(5)
At this point, you'd generally create a script of some sort that would read in the data from the input directory and produce some kind of output. We'll create dummies representing these steps.

```
touch extract_csv/src/extract_csv.py && touch extract_csv/output/extracted_data.csv
```


(6)
You can now use pdpp to create a 'run' step which will automate the hypothetical process of running extract_csv.py and producing extracted_data.csv. To do this, use the 'ball run' command from the project-level directory, and supply it with the name of the directory you'd like to 'run' and the language the task's script was written in (python, in this case). 

```
ball run -s extract_csv -l Python
```


(7)
To show how to link multiple tasks together, let's repeat the process with a new step directory. This time, we'll copy the outputs from the previous step (extract_csv) and feed them into this step as the inputs. We'll do this using a hard link.


```
ball step -s analyze_data

ln extract_csv/output/extracted_data.csv analyze_data/input/extracted_data.csv

touch analyze_data/src/analyze_data.py && touch analyze_data/output/model_output.md
```

(8)
Then, we'll identify analyze_data as a runnable step, just as we did with extract_csv in step 6.

```
ball run -s analyze_data -l Python
```

(9)
Now, we can link the two tasks together. The extracted_data.csv file appears in both the output of the extract_csv task AND the input of the analyze_data task; the `ball link` command will recognize this and make the output of the former a dependency of the latter.

```
ball link -s extract_csv -t analyze_data
```

(10)
At this point, a real project with a similar setup would be fully automated and ready to run. This would be done by evoking the `doit` command from the project directory. For more information on the `doit` automation package, see the [doit documentation][doit]. 
 

```
doit
```

(11)
Finally, pdpp can create some visualizations of your project's structure. The first command will produce a visualization showing how the steps are linked to one another, alongside the source code contained in each step. The second shows the files which comprise each step's dependencies (file -> step) as well as each step's outputs (step -> file)

```
ball graph -f source

ball graph -f file
```

<br>

## Things you can do with pdpp

All of the following commands are available without arguments: if they are entered without, you will be prompted for the inputs. 

### Step 

```
ball step -s [directory]
```

The `ball step` command is used to create a new step directory with the name specified. The step directory will contain input, output, and src directories, as well as a step-specific dodo.py file (part of the `doit` implementation). `.gitkeep` files will be included in each of the created directories to ensure their preservation via version control software. The step command will also check to see if the project is initialized; if not, it will create a project-level `dodo.py` and `.gitignore` file. 

### Run

```
ball run -s [directory] -l [language]
```

The `ball run` command is used to automate the process of running the scripts in a given step's src directory. Using this command will formalize the step's dependencies (contained in the input directory), target outputs (contained in the output directory), and the actions necessary to produce said outputs (usually involving running the scripts in the src directory). The scripts contained in the src directory must be written in a uniform language, which must be specified. 


### Link

```
ball link -s [source directory] -t [target directory]
```

The `ball link` command is used to automate the process of moving the contents of one step's output directory to another step's input directory. This command also formalizes the two steps' relationships with one another. This command is intended to be used **after** users have already populated both steps' respective directories with the necessary inputs and outputs (via either direct copying, hard links, or symbolic links. Our preferred approach, and the only one which pdpp has been extensively tested with, is hard linking). The `ball link` command will then detect which of the source step's outputs appear in the target step's input directory, and formalize this relationship. 


### Source

```
ball source -s [directory] -l [language]
```

The `ball source` command is always invoked as part of the `ball run` command, but can be run separately. It is used to automate the process of running the contents of a step's src directory, and should be used whenever changes to the contents of a step's src directory are made.


### Graph

```
ball graph -f [flavour]
```

Each linked step in your project is either dependent upon, or a dependency for, another step in your project. The `ball graph` can be used to visualize your project's dependency structure. It has four modes (or 'flavours'): file, source, sparse, and all.

`Sparse` mode only graphs the dependencies between steps.

`Source` mode graphs the dependencies between steps, and also includes representations of each step's source code.

`File` mode graphs the dependencies between steps and individual files - this can be useful to get an overview of which steps produce which files, and where those files are then used elsewhere in the project.

`All` mode includes the functionality of both `Source` and `File` modes (Warning: this can get messy).


### Doit

```
doit
```

While not technically a part of the package, pdpp is built around the `doit` automation suite. Use the `doit` shell command to run/compile/execute your automated project:

[doit]: http://pydoit.org/contents.html
[workflow]: https://hrdag.org/2016/06/14/the-task-is-a-quantum-of-workflow/
[Netlab]: http://networkslab.org/page/about/
[Ball Video]: https://www.youtube.com/ZSunU9GQdcI
[Ball]: https://hrdag.org/people/patrick-ball-phd/