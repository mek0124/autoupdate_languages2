# AutoUpdate Languages 2

An asynchronous python package that maintains an updated list of programming languages by scraping [Programming Languages](programminglanguages.info) every 90 days. This application is designed to be a background task loop and is ran asynchrounously.

## Installation

```bash
pip install autoupdate-languages2
```

## Usage
> ONLY `.txt` FILE IS AVAILABLE AS OUTPUT AT THIS TIME!

<details>
<summary>
To run the package as a background task in general or in your application
</summary>

```python
from autoupdate_languages2 import AutoUpdateLanguages2


if __name__ == '__main__':
  # Direct Call to the start method to start the loop
  AutoUpdateLanguages2().start()

  # OOP call
  auto_update_langs = AutoUpdateLanguages2()
  # call the start method to start the loop
  auto_update_langs.start()
```

</details>


<details>
<summary>
To use the package as an api call to create a file within the current directory of where your file was executed from
</summary>

```python
from autoupdate_languages2 import AutoUpdateLanguages2
import os

def create_lang_list_file():
  curr_dir = os.path.abspath(os.path.dirname(__file__)) # current path of where this file was executed
  output_dir = os.path.join(curr_dir, "output") # add the output dir './output/
  output_file = os.path.join(output_dir, "lang_list.txt") # add the desired file to the path -> only .txt works at this time

  auto_update_langs = AutoUpdateLanguages2()
  all_langs = auto_update_langs.generate_file(output_file)

create_lang_list_file()
```

</details>

<details>
<summary>
To use the python package as an api call to get the list of known programming languages
</summary>

> Be careful with how often you query this as this does a fresh webscrape on each query.
> It is best to use the `.generate_file(file_path)` method to generate the file one time
> and then work with the data from there!


```python
from autoupdate_languages2 import AutoUpdateLanguages2

auto_update_langs = AutoUpdateLanguages2()

lang_list = auto_update_langs.get_lang_list()
```

</details>

## Features
- Automatically updates language list monthly
- Lightweight and easy to use

