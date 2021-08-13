FuckItPy
========
### Python Error Steamroller

FuckItPy uses state-of-the-art technology to make sure your python code runs whether your compiler likes it or not.

Technology
----------

Through a process known as *Exec-Rinse-Reload-And-Repeat*, FuckItPy repeatedly execs your code, detecting errors and slicing those lines out of the script.

We take a step forward than famous FuckItJs and our competitor [Fuckitpy](https://github.com/ajalt/fuckitpy) that we save your code in real time so your code runs perfectly next time.

And we eliminate shitty code in your imports too!

In addition, we don't think any well behaved script should run more than 30s, so we consider it an error and handle it elegantly.

Installation
------------
```shell script
pip install fuckitpy
```

Usage
---

```shell script
fuckitpy path_to_your_shitty_script_file
```
```python
from fuckitpy.fuckitpy import clean_py

if __name__ == '__main__':
    clean_py('broke.py')
```
Q&A
---
Best code removes all your errors and any questions you may ask.

*We don't practically care what file has been rewritten,even system files cannot stop our best code optimization tech*