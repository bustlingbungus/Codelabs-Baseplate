Difference between thsi file and the solace-dev-codelab is in package.JSON

`"scripts": {
  "watch": "nodemon --watch BaseCodeLab.md --exec \"claat export -o temp/ BaseCodeLab.md && npx kill-port 9090 && cd temp/BaseCodeLab && claat serve\""
  }`

Why difference, because Windows, and he used Mac which can run Liniux scripts, but Windows is special
