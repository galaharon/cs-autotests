# CSE Autotests

This is a script written to run automated testing for the lab exercises. Anyone can contribute tests - please see the Contributing section for more information.

## Prerequisites

You will need Python3 installed to run this script. To check that Python is installed, open a terminal and run

```
python3 --version
```

If Python is installed correctly you should see output similar to the following:
```
Python 3.5.3
```

If you do not have Python 3 installed, download and install Python3 from [here](https://www.python.org/downloads/).

## Set-Up

### If you are on a CSE System
The script is available at `~z5164705/public_html/autotest.py`. This is a handful to type, so you can set up a short cut command to use every time. If you do not have a bin directory in your home directory yet, you can create one using `mkdir ~/bin`

Navigate to your bin directory:
```
cd ~/bin
```
Then create the autotest file:
```
echo '~z5164705/public_html/autotest.py "$@"' > autotest
chmod +x autotest
```
This will create a command called `autotest` you can run. To test it out, try run
```
autotest --help
```

If you get a bunch of information on the autotest then you did it right!

### If you are not on a CSE System
Not implemented yet

## Using the Script

### If you are on a CSE System
Navigate to the directory which contains the files you want to test. Make sure you compile your files before you run the script. To run all the tests for a lab, use:
```
autotest <class> <lab>
```
For example to run all the tests for CS1521 lab01 you can run:
```
autotest cs1521 lab01
```

### If you are not on a CSE System
Not implemented yet

### Arguments
To enable challenge tests add `-c` or `--challenge`. To run a particular exercise add `-e [exercise]`. To see a list of available exercises use `-l` or `--list`. To run a specific test use `-t [test name]` (remember to use quotes around the name if it contains spaces).
