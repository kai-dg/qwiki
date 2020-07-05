# Qwiki
Quick custom wikis. A clean way to organize information quickly.

## Setup
Windows: Run `dist/qwiki_app.exe`
Mac/Linux: You need to compile it yourself with PyInstaller
    - Run `python -m PyInstaller qwiki_app.py --onefile --noconsole`
    - Or run `python -m pyinstaller qwiki_app.py --onefile --noconsole`

## TODOs
Strict Tag System:
    List of added tags can only be used to tag a page
    When adding a tag:
        Available tags: sushi | indian | thai | burgers
Partial query:
    Partial matching of a search: http://docs.peewee-orm.com/en/latest/peewee/query_operators.html?highlight=partial#query-operators
Manual text file parser:
    Parses a text file to make a page
