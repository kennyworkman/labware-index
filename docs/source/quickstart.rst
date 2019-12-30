.. _quickstart:

Download
--------

Setting up the Labware Index tool should be a relatively quick process. 

- Grab the source code from its home on git 

:: 

  git clone https://github.com/kennyworkman/labware-index

- Navigate to the project direcotry and build `pyindex` as a local package
  using the `setup.py` file in the repo. (Activate a virtual environment if desired):
 
:: 

  cd labware-index
  python3 setup.py install

- Download extraneous dependencies for testing and using the GUI:
 
:: 

  pip3 install -r requirements.txt

That's it. You should be all set!

Testing
-------

Unit testing is implemented with `pytest`. Every method in the `pyindex`
package was implemented in isolation using a rigorous test-driven approach, guaranteeing
essential functionality and safe-guarding against potential edge cases.

To run the suite of unit tests:

- Navigate to the `tests` directory and run pytest:

::

  cd tests 
  pytest

Verbose feedback from the testing suite should be provided in terminal. If tests fail, make sure the Download steps were followed correctly. Consider rebuilding the package from source. `pytest` uses the locally built package sitting in your virtual environment to run its testing suite.
