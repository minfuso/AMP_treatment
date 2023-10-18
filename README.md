# AMP-PCMT

This Git repository aims to provide useful information and codes for `amp-atomistics` projects. 

---

# Table of contents
<!-- TOC -->

- [AMP-PCMT](#amp-pcmt)
- [Table of contents](#table-of-contents)
    - [Using PBS](#using-pbs)
        - [Automatically guess the parallel configuration](#automatically-guess-the-parallel-configuration)
            - [Generate the core dictionnary](#generate-the-core-dictionnary)
            - [Insert the core dictionary](#insert-the-core-dictionary)
        - [Examples and template scripts](#examples-and-template-scripts)

<!-- /TOC -->

---

## Using `PBS`

The `amp` code official documentation states that the code will guess the parallel configuration of the environnement using the function `amp.utilities.assign_cores()`. However, the code only support the `Slurm` job scheduler. Consequently, `amp` can not automatically guess the parallel configuration. The latter has to be done by hand, in the `python` script, using the following formalism:

```python

cores = { localhost: n_cores }

```
where `localhost` is the name of the node and `n_cores` is the number of cores used for parallel calculations. 

Howewer, the node names and the number of cores are determined after using the `qsub` command from `PBS`. Thus, it is mandatory to automatically determine the parallel configuration and write it using the good format in the python launch file. In the following, we will discuss the proposed commands to answer this issue as well as examples and template scripts.

<a href="#top">Back to top</a>

### Automatically guess the parallel configuration

Using `PBS`, we have access to several variables. The one that we will use is the `$PBS_NODEFILE`. It provides a list in the column format contining `n_core` lines. For each line, the name of the node is written. Therefore, if we count the occurences of each unique line in the `$PBS_NODEFILE` variable, we can have the number of cores that are used for each node. Then, we can format this information to match a python dictionnay one, to finally increment it in the python script.

<a href="#top">Back to top</a>

#### Generate the `core` dictionnary

The command to obtain the `core` information to provide to `amp` is the following:

```bash

export CORES=$(uniq -c $PBS_NODEFILE | awk '{print "\x27"$2"\x27:", $1","}' | sed -e '$ s/.$//' -e "\$a}" -e '1 i\cores = {' | sed ':a;N;$!ba;s/\n/ /g')

```

We can decompose it in order to better understand what is the purpose of each segment of the line. In addition, we will start with a `$PBS_NODEFILE` containing 16 `u-0-8` cores and 2 `u-0-9` ones.

- `uniq -c $PBS_NODEFILE` counts the occurences of each unique line in `$PBS_NODEFILE`. Following the example, the output should look like this:

```python
16 u-0-8
2 u-0-9
```

- `awk '{print "\x27"$2"\x27:", $1","}'` takes the secind column and wraps it with single quote (`'`), appends a colon (`:`), print the first column followed by a coma (`,`). Thus, the output in our example looks like:

```python
'u-0-8': 16,
'u-0-9': 2,
```

The following sed command can be further decomposed to understand it. 

- `sed -e '$ s/.$//'` deletes the last character of the last line
- `(sed -e) "\$a}"` appends a braket at the end of the last line
- `(sed -e) '1 i\cores = {'` insert `cores = {` at the beginnin

 In our example, the file becomes:
```python
cores = {
'u-0-8': 16,
'u-0-9': 2
}    
```

- `sed ':a;N;$!ba;s/\n/ /g'` This `sed` command uses a loop over `a` and is iterated for each line (`N`) except the last one (`$!`). It replaces the new line character (`\n`) by a space. Overall, this command concatenates the input to a single line. In our example, the file becomes:

```python
cores = { 'u-0-8': 16, 'u-0-9': 2 }    
```

which is the aimed format for the `amp` parallelization declaration.

<a href="#top">Back to top</a>

#### Insert the `core` dictionary

The last step is to implement this line in the correct area of the `amp` python code. The strategy is to have a model `amp` input files in which we set a specific pattern. We propose to call the `amp` input file `amp_input.py` that contains the specific pattern `PARALLEL` to the location of the `core` dictionnary. The corresponding line in `amp_input.py` can be written:

```python
calc = Amp(descriptor=Gaussian(),
           model=NeuralNetwork(hiddenlayers=(10, 10)), PARALLEL)
```

Then, we need to replace the pattern `PARALLEL` by the `core` dictionnary generated in the previous section. Thus, in the `PBS` file, we can use a sed command to implement it:

```bash
sed -e "s/PARALLEL/$CORES/g" amp_input.py > amp_input_launched.py
```

This command replaces the `PARALLEL` pattern by the `core` dictionnay stored previously in the `$CORE` bash variable. The output is then stored in a new file called `amp_input_launched.py`. In the latter file, the previously shown line becomes:

```python
calc = Amp(descriptor=Gaussian(),
           model=NeuralNetwork(hiddenlayers=(10, 10)), cores = { 'u-0-6': 16 })
```

when setting the calculation to run on 16 cores on the node u-0-6. 

Finally, we can use the `amp` code on plateforms handling only `PBS` job scheduler.

<a href="#top">Back to top</a>

### Examples and template scripts

You can find in the `scripts/launch/` directory all you need to launch AMP calculations using PBS on Sakura. The model file (see previous sections) is called `amp_input.py`, and the `PBS` file is `amp.pbs`. All the personal variables (such as the name) are replaced by general variables. Do not forget to change them to make it work properly.

<a href="#top">Back to top</a>

---