# CodeLab Baseplate

This is a copy of [Johnathan Wong's](https://github.com/JwongtheCodyBoy) CodeLab baseplate, but for some reason I was having trouble creating a branch when using a fork of [this](https://github.com/JwongtheCodyBoy/Codelabs-Baseplate) repo, so I just made my own repository.

Create a fork of this (or the aforementioned repo) to access the CodeLab baseplate.


## To Make an Actual CodeLab:

1. Create a new branch by running:

``` bash
git checkout -b YourBranch
```

2. Rename `BaseCodeLab.md` to `YourCodeLabName.md`.
3. Go to `YourCodeLabName.md`. Change the `feedback link` (line 8) to the link to the branch.
4. Go to `package.json`. Change `url` (line 11) to the link to the branch. Change each instance of `BaseCodeLab` in line 7 to `{YourCodeLabName}Codelab`
5. Run

``` bash
npm install
```

in the terminal.

6. After running npm once, you should not have to run it again for the current codelab. To look at the CodeLab while editing, run

``` bash
npm run watch
```

to open the codelab in a web browser.
  - In VSCode, pressing `Ctrl+Shift+B` to run default build tasks, which automatically runs `npm run watch`.
7. After closing the CodeLab in your web browser, press `Ctrl+C` in the terminal to end the task before the next use.