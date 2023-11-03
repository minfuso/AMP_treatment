<a id="scripts/extract/amp_extract"></a>

# amp\_extract

Modules allowing to extract AMP results in four different files.

* amp_energies.dat
* amp_forces.dat
* src_energies.dat
* src_forces.dat

where amp or src corresponds respectively to the neural network and source
data, as much forces as energies. It uses the same output formatting that
the one found for aeneth data treatment.

<a id="scripts/extract/amp_extract.Calc"></a>

## Calc Objects

```python
class Calc()
```

<a id="scripts/extract/amp_extract.Calc.__init__"></a>

#### \_\_init\_\_

```python
def __init__(amp_filename: str,
             traj_filename: str,
             generated_traj_filename: str,
             amp_energies_outfilename: str = 'amp_energies.dat',
             amp_forces_outfilename: str = 'amp_forces.dat',
             src_energies_outfilename: str = 'src_energies.dat',
             src_forces_outfilename: str = 'src_forces.dat')
```

Class allowing to extract AMP results in four different files.

- amp_energies.dat
- amp_forces.dat
- src_energies.dat
- src_forces.dat

where amp or src corresponds respectively to the neural network and
source data, as much forces as energies. It uses the same output
formatting that the one found for aeneth data treatment.

**Arguments**:

  - amp_filename (str): Filename for the amp calc object
  - traj_filename (str): Filename for the trajectory
  - generated_traj_filename (str):
  Filename for the generated (AMP) trajectory
  - amp_energies_outfilename (str, optional):
  Outfile name for the amp energies. Defaults to 'amp_energies.dat'.
  - amp_forces_outfilename (str, optional):
  Outfile name for the amp forces. Defaults to 'amp_forces.dat'.
  - src_energies_outfilename (str, optional):
  Outfile name for the source energies. Defaults to 'src_energies.dat'.
  - src_forces_outfilename (str, optional):
  Outfile name for the source forces. Defaults to 'src_forces.dat'.

<a id="scripts/extract/amp_extract.Calc.read_trajectories"></a>

#### read\_trajectories

```python
def read_trajectories()
```

Read the corresponding trajectories using the ase.io iread method

<a id="scripts/extract/amp_extract.Calc.extract_src_energies"></a>

#### extract\_src\_energies

```python
def extract_src_energies(atoms)
```

Extract source energy data from an atom object

<a id="scripts/extract/amp_extract.Calc.extract_amp_energies"></a>

#### extract\_amp\_energies

```python
def extract_amp_energies(atoms)
```

Extract amp energy data from an atom object

<a id="scripts/extract/amp_extract.Calc.extract_src_forces"></a>

#### extract\_src\_forces

```python
def extract_src_forces(atoms)
```

Extract source forces data from an atom object

<a id="scripts/extract/amp_extract.Calc.extract_amp_forces"></a>

#### extract\_amp\_forces

```python
def extract_amp_forces(atoms)
```

Extract source forces data from an atom object

<a id="scripts/extract/amp_extract.Calc.extract_src_data"></a>

#### extract\_src\_data

```python
def extract_src_data(atoms)
```

Extract energies and forces for the source atom trajectory object

<a id="scripts/extract/amp_extract.Calc.extract_amp_data"></a>

#### extract\_amp\_data

```python
def extract_amp_data(atoms)
```

Extract energies and forces for the amp atom trajectory object

<a id="scripts/extract/amp_extract.Calc.extract_data"></a>

#### extract\_data

```python
def extract_data()
```

Extract data for src and amp sets. Launch extract_src_data and
extract_amp_data after reading each frame.

<a id="scripts/extract/amp_extract.Calc.write_energies"></a>

#### write\_energies

```python
def write_energies(which='src')
```

Write the energies for the given type of file,
ruled by the argument 'which'

**Arguments**:

  - which (str, optional): Determine which file is written.
  Defaults to 'src'.

<a id="scripts/extract/amp_extract.Calc.write_forces"></a>

#### write\_forces

```python
def write_forces(which='src')
```

Write the forces for the given type of file,
ruled by the argument 'which'

**Arguments**:

  - which (str, optional): Determine which file is written.
  Defaults to 'src'.

<a id="scripts/extract/amp_extract.Calc.write_data"></a>

#### write\_data

```python
def write_data(which='src')
```

Write both forces and energies for a given file type,
ruled by the argument which

**Arguments**:

- `which` _str, optional_ - Determine which file is written.
  Defaults to 'src'.

<a id="scripts/extract/amp_extract.Calc.write_all_data"></a>

#### write\_all\_data

```python
def write_all_data()
```

Write both energies and forces for amp and src files

<a id="scripts/extract/amp_extract.Calc.predict"></a>

#### predict

```python
def predict()
```

#### clean

```python
def clean(logfile=True)
```

Clean the unwanted ampdb databases

**Arguments**:

- `logifile` _bool, optional_ - Determine if the logfile is deleted. Defaults to True.

<a id="scripts/extract/amp_extract.Calc.clean"></a>

