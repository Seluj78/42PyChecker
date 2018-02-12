# 42PyChecker

<!-- Need an image here -->

## We're actively looking for contributors !
Shoot me an email at <<jlasne@student.42.fr>> or on slack (42Born2Code) `jlasne` !

#### Uses
The script is designed as a reminder:
* author file terminated by a Line Feed
* count and files name
* code's standard
* required and forbidden functions
* macro definitions
* static variables & functions declarations
* makefile rules

Extra tests may also be performed:
* memory leaks detection
* speed test comparison
* Unit Tests

Complete unit tests are handled through external frameworks whose sources are automatically downloaded, configured and updated in background when you run the script:
* [**moulitest**](https://github.com/yyang42/moulitest), developed by [@yyang42](https://github.com/yyang42) and other contributors
* [**libftest**](https://github.com/jtoty/Libftest), developed by [@jtoty](https://github.com/jtoty)
<!--* [**libft-unit-test**](https://github.com/alelievr/libft-unit-test), developed by [@alelievr](https://github.com/alelievr)-->
<!--* [**fillit_checker**](https://github.com/anisg/fillit_checker), developed by [@anisg](https://github.com/anisg)-->
* [**Maintest**](https://github.com/QuentinPerez/Maintest), developed by [@QuentinPerez](https://github.com/QuentinPerez) and other contributors
<!--* [**42ShellTester**](https://github.com/we-sh/42ShellTester), developed by [@gabkk](https://github.com/gabkk) and [@jgigault](https://github.com/jgigault)-->

## Install & launch
This script requires python 3.6 or above to work.
```bash
git clone https://github.com/seluj78/42PyChecker --recursive ~/42PyChecker
cd ~/42PyChecker && python3 ./42PyChecker.py
```

## non-interactive mode
The non-interactive mode enables you to launch a test suite without any prompt.
You must specify the two options `--project` and `--path`.
Here is an example of use with the project `libft`:
```bash
python3 ~/42PyChecker/42PyChecker.py --project=libft --path=/Users/admin/Projects/libft/
```

## options

#### `--project` + *`$PROJECT`*

Required for non-interactive mode.  
Specify the name of the project you want to test.  
e.g.: `python3 ./42PyChecker.py --project=libft`.  
Must be one of the following values: `42commandements`, `libft` or `other`.

#### `--path` + *`$PATH`*

Required for non-interactive mode.  
This option has no effect when used without the option `--project`.  
Specify the absolute path of directory of your project.  
e.g.: `python3 ./42PyChecker.py --project=libft --path=/Users/admin/Projects/libft/`.

##### `--no-author`, `--no-norm`, `--no-makefile`, `--no-forbidden-functions`, `--no-static`, `--no-moulitest`, `--no-maintest`, `--no-libftest`, `--no-extra`

Disable a specific test.

##### `--no-tests`
This will disable all testing suites but run the other tests.

#### `--show-c` and `--show-w`
These options will display respectively the License and the Warranty.

## official team and credits

42PyChecker is an open source project distributed under licence [GNU-3.0](https://github.com/Seluj78/42PyChecker/blob/master/LICENSE).

Originally developed by Jules Lasne [@seluj78](https://github.com/seluj78) <<jules.lasne@gmail.com>>

Huge thanks to the original author and main inspiration, Jean Michel Gigault [@jgigault](https://github.com/jgigault) and his incredible [42FileChecker](https://github.com/jgigault/42FileChecker)

## contribute

If you want to be part of the project, to fix and to improve 42PyChecker, please follow the guide lines [**Contributing to 42PyChecker**](https://github.com/seluj78/42PyChecker/wiki/Contributing-to-42PyChecker), or if you want your own unit testing framework to be integrated in the 42PyChecker, just let me know at **jlasne@student.42.fr**.
