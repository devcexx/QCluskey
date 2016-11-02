# QCluskey

QCluskey is a little project written in Python that implements the Quine-McCluskey algorithm to simplify boolean functions.
### Requirements

 - Python 2 (>=2.7)  **_Not compatible with Python 3_**
 - PyBexpp (It's recommended to grab it from the submodule of this git repository, cloning it with the --recursive argument)

### Usage

The main function of this library is ```qcluskey_simplify``` that allows you to simplify a boolean function. It takes two arguments. The first one is the truth set of the function to simplify. It could be either a list or a set of items. Each element of the set is a string with '0's and '1'es that represents the different states of the variables that makes the original function 1. As an example, a valid truth set will be: ```['0010', '0110', '0001']```. This truth set means that ```f(0,0,1,0) = 1; f(0,1,1,0) = 1 and f(0,0,0,1) = 1.```

The second parameter is the list of the variables. It must be a ordered list of elements, so the script can relation the position of each variable with its value on each element of the truth set. So, if the variable list is ```['a','b','c','d']```, for the first item of the truth set, ```a = 0; b = 0; c = 1; d = 0```, for the second ```a = 0; b = 1; c = 1; d = 0``` and so on.

The result of the function is an object of Operation type, that is defined in PyBexpp, the library where QCluskey relies on. To use and get information from this class, please refer to the documentation of PyBexpp.

The script does not include a main program to execute, so this function has to be manually executed from the Python console. First of all, clone the repositoriy with the ```--recursive``` flag to init the PyBexpp submodule. Then, open a terminal in the directory where the clone of the repository was made, and then open the Python terminal.
```
$ cd QCluskey
$ python2
```

Now, suppose that we have the boolean function ```f(x,y,z,t) = x'y'z't' + x'y'z't + xy'z't' + x'yzt' + xy'z't + xyz't' + xyzt'```. The truth set of this function is clearly ```{0000, 0001, 1000, 0110, 1001, 1100, 1110}```. With this information, we can now simplify the function:
```
>>> from qcluskey import *
>>> fx = qcluskey_simplify(['0000', '0001', '1000', '0110', '1001', '1100', '1110'], ['x','y','z','t'])
>>> fx.common_notation()
"xz't'+yzt'+y'z'"
```

Now, thanks to the Quine McCluskey algorithm, we were able to simplify the expression ```f(x,y,z,t) = x'y'z't' + x'y'z't + xy'z't' + x'yzt' + xy'z't + xyz't' + xyzt'``` to ```f(x,y,z,t) = xz't'+yzt'+y'z'```

Also you can, calculate the truth set of the result operation, evaluate it, or even parse an expression an then let the computer to calculate its truth set to finally simplifying it using this algorithm. For anything of these, please refer to the documentation of PyBexpp.

### License
This software is under the GNU GPL v3 license. This mean, in a nutshell, that you can freely use and distribute open source software that uses this library, but you cannot use it for commercial purposes or closed source projects. For more details about this license, please refer to the file ```LICENSE``` present in this repository.