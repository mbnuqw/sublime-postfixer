# Postfixer

Postfix completions plugin for Sublime Text 3.


## Usage examples

![python example](https://raw.githubusercontent.com/mbnuqw/sublime-postfixer/master/docs/py.gif)

![js example](https://raw.githubusercontent.com/mbnuqw/sublime-postfixer/master/docs/js.gif)


## Installation

### Manual

```
git clone git@github.com:mbnuqw/sublime-postfixer.git
cd sublime-postfixer
python build.py
```

### Setup key binding

```json
{ "keys": ["whatever"], "command": "postfix" },
```

### Writing custom snippets

- Open fixes:
    - Menu: Preferences -> Package Settings -> Postfixer -> Snippets
    - or Open command palette -> search 'Postfixer: Snippets'
- Edit snippets and save file
- Reload snippets:
    - Menu: Preferences -> Package Settings -> Postfixer -> Reload Snippets
    - or Open command palette -> search 'Postfixer: Reload Snippets'


## License

MIT