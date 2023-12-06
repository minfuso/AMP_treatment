# amp\_launch

Module allowing to generate `amp-atomistics` input files for launching or relaunching calculations. This module aims to be launched using the `PBS` script described in this section. If you want to write your own `PBS` script, please be carefull to include the automatic parallel configuration descripted on the previous section. Indeed, this module uses the `PARALLEL` keyword in the `amp-atomistics` script in order to handle correctly the parallelization when running on super computers using `PBS`.

## The `Launch` object

Writing correct `amp-atomistics` inputs is not a trivial task. Indeed, some parameters are 'hidden', and can not be set easely. The `launch` module from the `amppcmt` parckage is provided in order to help the users to write correct input files when using `amp-atomistics` thorugh the `Launch` object.

The `Launch` object is a class that can be loaded as:

```python
from amppcmt.launch import Launch
```

When calling this object, several arguments are needed. Here are the list of all the arguments that you can pass through this class:

- `traj_name` (str) 

    Name of the trajectory file (training set)

- `amp_param` (str, optional)

    Name of the amp-parameters to restart
    the calculation. Defaults to None.

- `hiddenlayers` (tuple, optional)

    Number of hiddenlayers and neurones, following the amp-atomistics format. Defaults to (10,10).

- `checkpoints` (int, optional)

    Checkpoint frequency. 
    Defaults to -100.

- `forces` (bool, optional)
    
    Force training. If set to False,
    the neural network is not trained with forces. 
    Defaults to False.

- `convergence_parameters` (dict, optional)
    
    Convergence parameters
    for the lossfunction. Following the amp-atomistics format
    Defaults to None (default parameters).

- `initial_calc` (bool, optional)

    Set it to True if you are launching 
    a new calculation, to false to restart a calculation. 
    Defaults to True.

- `test` (bool, optional)
    
    Used for debbuging. Set it to True to test
    on your local computer or super computer. 
    Defaults to False.

- `filename` (str, optional)
    
    Name of the amp-atomistics generated 
    input file. Defaults to 'amp_launch.py'.

The module uses two different `jinja2` templates: one for testing, the other for production. Each files are located in the module directroy (`launch`) and imported to the binari files by `MANIFEST.in`.

> Note that in the current version of the package, only `PBS` launching is supported. In addition, you need to have a custom `PBS` launched, as detailled in the `PBS` section.

### Creating a Launch instance

To create a `Launch` instance, just build the object as:

```python
test = Launch(
    traj_name = 'CO_disso_traj', # Name of the trajectory file
    hiddenlayers = (10, 10), # Number of hiddenlayers and neurones
    checkpoints = -100, # Checkpoint frequency
    forces = False, # Force training?
    initial_calc = True, # Initial or relaunching a calculation?
    convergence_parameters = { # All the parameters for convergencee
        'energy_rmse':0.001,
        'force_rmse': None,
        'energy_maxresid': None,
        'force_maxresid': None
    },
    filename = 'test_first_calc.py', # Name of the python amp launch file
    test = False # Put it to true to not launch the calculation (testing)
    )
```

Here, the `Launch` class is stored in the test variable. The calculation is set to run on the `CO_disso_traj.traj` file, with two hiddenlayers composed by 10 neurones each, training only on energies with an energy RMSE of 0.001 for convergence. This is an initial calculation (`initial_calc = True`, and the generated script will be called `test_first_calc.py`. 

The `checkpoints` variable, defaulting to -100, plays a pivotal role. When assigned a positive value, it triggers the periodic overwrite of checkpoint parameters every 100 steps, facilitating real-time model refinement. Alternatively, a negative value, like the default, retains and saves all distinct checkpoints, an advantageous feature for assessing the Root Mean Squared Error (RMSE) evolution across training and test sets relative to epochs.

### Relaunching a calculation

To resume a previously halted calculation, users can leverage the `amp_param` variable and set `initial_calc` to True when creating a `Launch` instance. The `amp_param` variable should be assigned the file name containing the desired amp parameters for restarting the calculation. It allows users to seamlessly pick up where they left off, utilizing the specified parameters from the provided file. Here is a concrete example:

```python

test_relaunch = Launch(
    traj_name = 'CO_disso_traj', # Name of the trajectory file
    amp_param = 'amp-untrained-parameters.amp', # Name of the amp parameters file
    hiddenlayers = (10, 10), # Number of hiddenlayers and neurones
    checkpoints = -100, # Checkpoint frequency
    forces = False, # Force training?
    initial_calc = False, # Initial (true) or relaunching a calculation (False)?
    convergence_parameters = { # All the parameters for convergencee
        'energy_rmse':0.001,
        'force_rmse': None,
        'energy_maxresid': None,
        'force_maxresid': None
    },
    filename = 'test_second_calc.py', # Name of the python amp launch file
    test = True # Put it to true to not launch the calculation (testing)
    )

```
Here, by specifying `initial_calc` as `False` and providing the file name containing the amp parameters with `amp_param`, the `Launch` object facilitates the seamless continuation of the calculation, utilizing the specified parameters from the designated file.

## Generating `amp-atomistics` input files

Once the `Launch` class is instantiated and relevant parameters are configured, users can harness the power of the `generate_input()` method to generate input files for `amp` calculations. This method streamlines the process, considering the specified parameters and producing an input file ready for execution.

For example, after creating a `Launch` instance named `test`, you can use the following command:

```python
test.generate_input()
```

The `generate_input()` method on the `test` instance will create an `amp-atomistics` input file based on the specified parameters. It simplifies the workflow, ensuring that the input file is accurately configured for the intended calculations, whether for an initial run or a relaunch of a previous computation.