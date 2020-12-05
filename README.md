# EMSLIBS 2019 contest
## Load scripts
### Python
The script/module was written and tested on Python 3.8 using Linux.
#### Installation and usage
Get the code as a zip archive or clone it from Git:
```commandline
$ git clone https://github.com/JVrabel/EMSLIBS_contest.git
$ cd EMSLIBS_contest
```
---
Package requirements are in `requirements.txt`. To install them
using [pip](https://pypi.org/project/pip/) write into your command line:
```commandline
$ python3 -m pip install -r requirements.txt
```
---
Download datasets (`train.h5` and `test.h5`) from
this [link](https://www.nature.com/articles/s41597-020-0396-8).
Save them into `datasets/` directory and rename them to `contest_TRAIN.h5`
and `contest_TEST.h5`.
---
Import the module into your python script using:
```python
import load_scripts.h5_load_contest as load
```
or
```python
from load_scripts.h5_load_contest import *
```
---
The module offers three types of functions/methods:
- `load_*()` - read dataset file and return result as a _numpy_ vector or matrix
- `[train|test]_to_numpy_pickle()` - read dataset and save result
to disk as a _numpy_ pickle for later use
- `[train|test]_to_pandas_pickle()` - read dataset, create _pandas_
DataFrame and and save it to disk as a _pandas_ pickle for later use