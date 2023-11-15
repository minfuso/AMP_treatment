"""
Modules allowing to extract AMP results in four different files.
    - amp_energies.dat
    - amp_forces.dat
    - src_energies.dat
    - src_forces.dat
where amp or src corresponds respectively to the neural network and source
data, as much forces as energies. It uses the same output formatting that
the one found for aeneth data treatment.
"""

# IMPORTATIONS

import os
import shutil
from ase.io import iread
from ase import Atoms
from amp import Amp
import numpy as np

# CLASSES


class Calc:
    def __init__(
        self,
        amp_filename: str,
        traj_filename: str,
        generated_traj_filename: str,
        amp_energies_outfilename: str = "amp_energies.dat",
        amp_forces_outfilename: str = "amp_forces.dat",
        src_energies_outfilename: str = "src_energies.dat",
        src_forces_outfilename: str = "src_forces.dat",
    ):
        """
        Class allowing to extract AMP results in four different files.

            - amp_energies.dat
            - amp_forces.dat
            - src_energies.dat
            - src_forces.dat

        where amp or src corresponds respectively to the neural network and
        source data, as much forces as energies. It uses the same output
        formatting that the one found for aeneth data treatment.

        Args:
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
        """
        self.amp_filename = amp_filename
        self.traj_filename = traj_filename
        self.generated_traj_filename = generated_traj_filename
        self.amp_energies_outfilename = amp_energies_outfilename
        self.amp_forces_outfilename = amp_forces_outfilename
        self.src_energies_outfilename = src_energies_outfilename
        self.src_forces_outfilename = src_forces_outfilename

        self.trajectory = []
        self.species = []
        self.src_energies = []
        self.src_forces = []
        self.amp_energies = []
        self.amp_forces = []

        self.src_time_counter = 0
        self.src_nb_points = 0

        self.read_trajectories()

        self.calc = Amp.load(self.amp_filename)

    def read_trajectories(self):
        """
        Read the corresponding trajectories using the ase.io iread method
        """
        self.trajectory = iread(self.traj_filename)
        self.generated_trajectory = iread(self.generated_traj_filename)

    def extract_src_energies(self, atoms):
        """
        Extract source energy data from an atom object
        """
        self.src_energies.append(atoms.get_potential_energy())

    def extract_amp_energies(self, atoms):
        """
        Extract amp energy data from an atom object
        """
        self.amp_energies.append(atoms.get_potential_energy())

    def extract_src_forces(self, atoms):
        """
        Extract source forces data from an atom object
        """
        self.src_forces.append(atoms.get_forces())

    def extract_amp_forces(self, atoms):
        """
        Extract source forces data from an atom object
        """
        self.amp_forces.append(atoms.get_forces())

    def extract_src_data(self, atoms):
        """
        Extract energies and forces for the source atom trajectory object
        """
        self.extract_src_energies(atoms)
        self.extract_src_forces(atoms)
        self.src_nb_points = len(self.src_energies)

    def extract_amp_data(self, atoms):
        """
        Extract energies and forces for the amp atom trajectory object
        """
        self.extract_amp_energies(atoms)
        self.extract_amp_forces(atoms)
        self.amp_nb_points = len(self.amp_energies)

    def extract_data(self):
        """
        Extract data for src and amp sets. Launch extract_src_data and
        extract_amp_data after reading each frame.
        """
        # Extracting for src files
        for src_atoms in self.trajectory:
            if not self.species:
                self.species = src_atoms.get_chemical_symbols()
            self.extract_src_data(src_atoms)

        # Extracting for amp files
        for atoms in self.generated_trajectory:
            amp_atoms = Atoms(
                symbols=atoms.get_chemical_symbols(),
                positions=atoms.get_positions(),
                calculator=self.calc,
            )
            self.extract_amp_data(amp_atoms)

        # Converting forces into numpy array for handling information
        # easely
        self.src_forces = np.array(self.src_forces)
        self.amp_forces = np.array(self.amp_forces)

    def write_energies(self, which="src"):
        """
        Write the energies for the given type of file,
        ruled by the argument 'which'

        Args:
            - which (str, optional): Determine which file is written.
                Defaults to 'src'.
        """
        if which == "src":
            print("writing energies for the src file")
            outfile = open(self.src_energies_outfilename, "w")
            nb_points = self.src_nb_points
            energies = self.src_energies
        else:
            print("writing energies for the amp file")
            outfile = open(self.amp_energies_outfilename, "w")
            nb_points = self.amp_nb_points
            energies = self.amp_energies
        for item in range(nb_points):
            outfile.write("{0:>12} {1:>15.8f}\n".format(item + 1, energies[item]))
        outfile.close()

    def write_forces(self, which="src"):
        """
        Write the forces for the given type of file,
        ruled by the argument 'which'

        Args:
            - which (str, optional): Determine which file is written.
                Defaults to 'src'.
        """
        if which == "src":
            print("writing forces for the src file")
            outfile = open(self.src_forces_outfilename, "w")
            forces = self.src_forces
            nb_points = self.src_nb_points

        else:
            print("writing forces for the amp file")
            outfile = open(self.amp_forces_outfilename, "w")
            forces = self.amp_forces
            nb_points = self.amp_nb_points

        atom_counter = 0
        for nb_traj in range(nb_points):
            for atom_force in forces[nb_traj]:
                outfile.write(
                    "{0:>3} {1:>15.8f} {2:>15.8f} {3:>15.8f}\n".format(
                        atom_counter + 1, atom_force[0], atom_force[1], atom_force[2]
                    )
                )
                atom_counter += 1
            atom_counter = 0
            outfile.write("\n")
        outfile.close()

    def write_data(self, which="src"):
        """
        Write both forces and energies for a given file type,
        ruled by the argument which
        Args:
            which (str, optional): Determine which file is written.
                Defaults to 'src'.
        """
        self.write_energies(which=which)
        self.write_forces(which=which)

    def write_all_data(self):
        """
        Write both energies and forces for amp and src files
        """
        self.write_energies(which="src")
        self.write_forces(which="src")
        self.write_energies(which="amp")
        self.write_forces(which="amp")

    def predict(self):
        """
        Predict the energies according to the input files
        Launch the extract_data followed by the write_all_data methods.
        """
        self.extract_data()
        self.write_all_data()

    def clean(self, logfile=True):
        """

        Clean the unwanted ampdb databases

        Args:
            logfile (bool, optional): _description_. Defaults to True.
        """
        DIR_LIST = (
            "amp-fingerprint-primes.ampdb",
            "amp-fingerprints.ampdb",
            "amp-neighborlists.ampdb",
        )
        # Clean the directories
        for dir in DIR_LIST:
            try:
                shutil.rmtree(dir)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        # Delete the logfile if asked
        if logfile:
            # Try to delete the file.
            try:
                os.remove("amp-log.txt")
            except OSError as e:
                # If it fails, inform the user.
                print("Error: %s - %s." % (e.filename, e.strerror))


if __name__ == "__main__":
    """
    Determine the actions if the module is launched as main and not imported
    """
    # Constants
    AMP_FILENAME = "/Users/infuso/Documents/CALC/Machin-learning/CO_dissociation/10_10/amp-untrained-parameters.amp"
    TRAJ_FILENAME = "/Users/infuso/Documents/CALC/Machin-learning/CO_dissociation/10_10/CO_disso.traj"
    GENERATED_TRAJ_FILENAME = "/Users/infuso/Documents/CALC/Machin-learning/CO_dissociation/10_10/CO_disso.traj"
    AMP_ENERGIES_OUTFILENAME = "amp_energies.dat"
    AMP_FORCES_OUTFILENAME = "amp_forces.dat"
    SRC_ENERGIES_OUTFILENAME = "src_energies.dat"
    SRC_FORCES_OUTFILENAME = "src_forces.dat"

    print("Module launched as main")

    data = Calc(
        amp_filename=AMP_FILENAME,
        traj_filename=TRAJ_FILENAME,
        generated_traj_filename=GENERATED_TRAJ_FILENAME,
        amp_energies_outfilename=AMP_ENERGIES_OUTFILENAME,
        amp_forces_outfilename=AMP_FORCES_OUTFILENAME,
        src_energies_outfilename=SRC_ENERGIES_OUTFILENAME,
        src_forces_outfilename=SRC_FORCES_OUTFILENAME,
    )

    data.predict()

    data.clean()
