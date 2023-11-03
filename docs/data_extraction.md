# Data extraction

After running `amp` calculations, ones want to extract the data from the `amp` calculator (i.e., the neural network). According to the [official documentation](https://amp.readthedocs.io/en/latest/useamp.html), it can be done mostly through the `ase` package. In this section, all the methods built to extract or related to data extraction using the `amp` calculator are presented.

## The Amp loading method

In `ase`, to perfom calculations, we use a calculator object named `calc` by convention. When the calculator is assigned to the `Atom` object, we can perform potential energy calculations using the `get_potential_energy()` method. To compute potential energy using the `amp` neural network, the same scheme is used. 

First, the `amp` neural network has to be loaded in the `ase` one. Do to so, we will use the `Amp` class provided by the `amp-atomistics` package. For example, if I want to load the `amp_calc.amp` neural network, the code is the following:

```python
# Loading amp_calc.amp as a calculator 

from amp import Amp

calc = Amp.load('amp_calc.amp')
```

Now, the `amp` calculator can be assigned to any `ase` `Atom` class and can compute the corresponding potential energy.

## Data validation

When handling neural network training, one significant step is testing. Usually, a neural network is trained using a set of data called *training set*. Once the training done, we want to measure its performance by computing its accuracy on the *training set* but also on a set of data that is unknown to the model, called the *testing set*. 

To perform such step, one need to extract the potential energy for all the features present in both the training and the testing set. Usually, we use *ab initio* values as reference, called *src* in our module. Once those data aquired, we need to compute the potential energy using our neural network and compare them. 

To facilitate those steps, we propose a general method called `amp_extract`, that will be discussed in the next section.

### amp_extract

`amp_extract` is a set of `python` scripts that allows to extract, predict and write the results on brut data files. To have the details about all the functions inside this module, please check the **module documentation** section. 

In this version, `amp_extract` is composed by only one class: `Calc`. This class allows you to extract, predict, and write all the values needed for the neural network testing step. The class takes several arguments, some mandatories and other optional. Here are the arguments:

**Input arguments**

  - `amp_filename` (str): Filename for the amp calc object (*.amp, neural network)
  - `traj_filename` (str): Filename for the trajectory (*.traj, training set trajectory)
  - `generated_traj_filename` (str):
  Filename for the generated (AMP) trajectory (*.traj, testing set trajectory)

**Output arguments**

  - `amp_energies_outfilename` (str, optional):
  Outfile name for the amp energies. Defaults to 'amp_energies.dat'.
  - `amp_forces_outfilename` (str, optional):
  Outfile name for the amp forces. Defaults to 'amp_forces.dat'.
  - `src_energies_outfilename` (str, optional):
  Outfile name for the source energies. Defaults to 'src_energies.dat'.
  - `src_forces_outfilename` (str, optional):
  Outfile name for the source forces. Defaults to 'src_forces.dat'.

By default, it can produces three different files:

- amp_energies.dat
- amp_forces.dat
- src_energies.dat
- src_forces.dat

where amp or src corresponds respectively to the neural network (testing set) and
source data (reference testing set) It uses the same output
formatting that the one found for `aeneth` data treatment.

### How to use

First, we need to generate the `Calc` object:

```python
# Libraries imported in the module
from ase.io import iread
from ase import Atoms
from amp import Amp
import numpy as np

# Importing the module
from amp_extract import Calc

# Defining the Calc object
data = Calc(
        amp_filename = AMP_FILENAME,
        traj_filename = TRAJ_FILENAME,
        generated_traj_filename = GENERATED_TRAJ_FILENAME,
        amp_energies_outfilename = AMP_ENERGIES_OUTFILENAME,
        amp_forces_outfilename = AMP_FORCES_OUTFILENAME,
        src_energies_outfilename = SRC_ENERGIES_OUTFILENAME,
        src_forces_outfilename = SRC_FORCES_OUTFILENAME 
    )
```
where the words in full capitals are the path of the corresponding file. On initialization, the `Calc` class read all the trajectories (from reference and for the testing set using the `iread` method from `ase`. It corresponds to parse each step of the trajectory as a generator. Then, the memory is not overload when parsing huge trajectories. It also read the neural network using the `load` method from the `Amp` class.

Once we have this object, we can use those significant methods:

- `extract_data()`

    This method extract and compute all the forces and energies for the given trajectories. You can access through the class as `amp_energies = data.amp_energies` or `src_forces = data.src_forces` for example.

- `write_all_data()`

    This method will write all the forces and energies for the given trajectories in an `aeneth` like format. 

- `predict()`

    This method just chain both of the previously stated methods. It allows you to extract, predict and write all the forces and energies in one line.

## Example

One jupyter notebook example is present in the example folder, in the amp_example directory.

## Troubleshooting

- **FileNotFound error for `amp` calculator file**: 

    Try to indicate the relative/full path for the `amp_filename` argument. Issue can be linked to `Amp.load()` method.

