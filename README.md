<!-----



Conversion time: 0.219 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β44
* Sat May 10 2025 09:27:23 GMT-0700 (PDT)
* Source doc: app_highlighter_readme
----->


**<span style="text-decoration:underline;">Simple screen region highlighter</span>**

**Install:**

```bash

iex (New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/Unnamed10110/simpleHighlighter_Unnamed10110/master/install_highlighter.ps1')
```
![Demo](https://github.com/Unnamed10110/simpleHighlighter_Unnamed10110/blob/master/Animation.gif)


**Usage**:
After installing, when you want to highlight a part of the screen press ctrl + Numpad7, then you can select multiple sreen regions. Press ctrl + z to undo or  Esc to quit .

![Demo](https://github.com/Unnamed10110/simpleHighlighter_Unnamed10110/blob/master/usage_animation.gif)


**Dependencies:**



* . PWSH
* . Winget
* . Python
* . PyQt5
* . Autho Hotkey V2

  . You should run the created file run_highlighter.ahk everytime the computer restarts or add it to the startup to make it run automatically at startup (win + r and, type: shell:startup + enter, paste a shortcut to the run_highlighter.ahk file).
