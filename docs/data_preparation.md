# Data preparation

Before training a neural network model, we need to prepare the data set. In the case of
neural network for atomistic calculations, ones need to configure a training and test
set in the correct format. In this section, we will introduce the tools allowing to do
that in the `amp` package framework.

## Data splitting

The `amp` (in opposition with `aenet`) package do not split the reference data set into
a training and a testing set. Therefore, to perform well data validation after the training
of the neural network, we first need to split the reference data set into these two sets.
One solution given here is to use the `amp_split` module given in this code.

## amp\_split

`amp_split` is a set of python scripts that allows to split a reference data set (`traj` file format)
into two different set: the training and the testing set (`traj` file format). 

In this version, `amp_split` is composed only by one Class: `Train_test_split`. This Class takes several
arguments:

- `trajectory` (str): Name of the data set file (`.traj` file)
- `training_set_percentage` (float, optional): Percentage of the training set. Default to 0.75

As output, we obain three different file:

- `[trajectory_filename]_train.traj`: File containing the data for the training set
- `[trajectory_filename]_test.traj`: File containing the data for the testing set
- `amp_split.log`: Logfile containing execution time and terminal prompt

## How to use

First, we need to generate the `Train_test_split object`

```python
# Warning: Need additional code to read the module. 
# See examples/amp_split/example_split.ipynb
#
# Importing the module
from amp_split import Train_test_split

trajectory = Train_test_split(
    trajectory = [trajectory_name],
    training_set_percentage=0.75
)
```

where `trajectory_name` is the name of the reference trajectory file. 
At this point, the split has not been down. In order to perform a split of
these configurations using randomly selectect configurations, we call the
`split_sets_random()` method from the Class. It can be done as:

```python
# Splitting the trajectories

trajectory.split_sets_random()
```

At this point, the output files are written in the current working directory.

## Example

An example can be found in the examples: `scripts/examples/amp_split/example_split.ipynb`.


