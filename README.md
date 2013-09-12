cppmagic
========

A simple IPython extension that runs C++ code and shows the output. Supports command-line input to g++.

Example output
--------------

http://nbviewer.ipython.org/urls/raw.github.com/dragly/cppmagic/master/example.ipynb

Installation
------------

Simply download and try the example.ipynb notebook that you'll find in the root folder of this repository.

Usage
-----

Run the following commands in one cell. This will download the cppmagic module and load it.

    %install_ext https://raw.github.com/dragly/cppmagic/master/cppmagic.py
    %load_ext cppmagic
    
Then create a new cell like this:

    %%cpp
    #include <iostream>
    using namespace std;

    class MyClass {
    public:
        int a;
        MyClass() {
            a = 10;
        }
    };

    int main() {
        MyClass B;
        cout << B.a << endl;
        return 0;
    }
    
