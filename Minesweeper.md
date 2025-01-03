author: Caden Spokas
summary:
id: Minesweeper
tags:
categories:
environments: Web
status: Published
feedback link: https://github.com/bustlingbungus/Codelabs-Baseplate/tree/Minesweeper

# Minesweeper

## Overview

### Table Of Contents

1. This page
2. Environment setup

### Final Game:

![Final Minesweeper Game](img/finalGame.png)

## Setting Up Environment

### VSCode and Python

We will be using VSCode to create the Python code for this project. These can be downloaded here:
* [VSCode](https://code.visualstudio.com/download)
* [Python](https://www.python.org/downloads/) 

> aside positive
> If you use some IDE other than VSCode, that should be fine!

### Make sure to check this box here:

![Python Instruction](img/pythonAddToPath.png)

### Pygame 

This project will use an API called `pygame` to create a window and render things onto it. To get pygame, just type the following command in a VSCode terminal:

For Windows:

``` bash
py -m pip install -U pygame --user
```

For Mac:

``` bash
python3 -m pip install -U pygame --user
```

Create a new folder on your computer for this project, and open it in VSCode.

## Get Project Baseplate

Download the baseplate files for this project [here](https://drive.google.com/file/d/1CjUvyzGQz7cn7O13nAkKgWaxJavK40ij/view?usp=sharing). Extract this file anywhere, and open the extracted folder in VSCode.

The folder will contain three .py files, `main`, `Cell`, and `Functions`. It will also contain two .png images, and one .ttf font. These are the assets we will use for Minesweeper.

`main.py` contains some code for opening a window with pygame. When creating the game, this will be the file that we actually run.