# Importation
from ase.io import read, Trajectory
import random
from functools import wraps
import time
import logging
import os

# Create and configure logger
print(
    "Log: ", os.getcwd() + "/" + os.path.basename(__file__).split(sep=".")[0] + ".log"
)
logging.basicConfig(
    filename=os.getcwd() + "/" + os.path.basename(__file__).split(sep=".")[0] + ".log",
    format="%(message)s",
    filemode="w",
)
logger = logging.getLogger()

# Logger threshold
logger.setLevel(logging.DEBUG)


# Time decorator -> logger
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f'Function {func.__name__} took {total_time:.4f} seconds')
        logger.debug(f"Function {func.__name__} took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


class Train_test_split:
    @timeit
    def __init__(self, trajectory: str, training_set_percentage: float = 0.75):
        """
        Initialize the class. The purpose is to split a trajectory file into a train and
        a test trajectory files.
        Args:
            trajectory (str): Name of the initial trajectroy file
            training_set_percentage (float, optional): Percentage of the trajectory into
                the training set trajectory. Defaults to 0.75.
        """
        self.trajectory_name = trajectory
        self.trajectory = read(trajectory, index=":")  # Read the trajectory
        self.training_set_percentage = training_set_percentage
        self.total_length = len(self.trajectory)

    def _filename_generation(self):
        """
        Generate the output filenames from the input filename.
        """
        self.test_traj_name = self.trajectory_name.split(sep=".")[0] + "_test.traj"
        self.train_traj_name = self.trajectory_name.split(sep=".")[0] + "_train.traj"

    def traj_get_info(self):
        """
        Get info on the current trajectory file.
        """
        # General info on the trajectory
        print("The trajectory is composed by {} frames".format(self.total_length))
        # Setting variables
        self.nb_training = round(self.training_set_percentage * self.total_length)
        self.nb_test = self.total_length - self.nb_training
        print(
            "The number of frames in the training set is: {}".format(self.nb_training)
        )
        print("The number of frames in the test set is: {}".format(self.nb_test))
        logger.debug(
            "The number of frames in the training set is: {}".format(self.nb_training)
        )
        logger.debug("The number of frames in the test set is: {}".format(self.nb_test))
        # Filenames generation
        self._filename_generation()
        # Printing information about outfiles
        print("The test trajectory is saved as {}".format(self.test_traj_name))
        logger.debug("The test trajectory is saved as {}".format(self.test_traj_name))

    @timeit
    def split_sets_random(self):
        """
        Split the input trajectory into training and test trajectories randomly.
        Inputs are given in the init function.
        """
        # Getting info for the current trajectory
        # Generating filenames
        self.traj_get_info()

        # Randomly selecting configurations for the test set (smaller)
        id_test_list = random.sample(range(0, self.total_length), self.nb_test)

        # Creating test_list_trajectory file
        self.test_traj = Trajectory(filename=self.test_traj_name, mode="w")
        for id in id_test_list:
            frame = self.trajectory[id]
            self.test_traj.write(frame)

        # Creating train_list_trajectory file
        self.train_traj = Trajectory(filename=self.train_traj_name, mode="w")
        for id in range(self.total_length):
            # Passing if id is in the test set
            if id in id_test_list:
                continue
            frame = self.trajectory[id]
            self.train_traj.write(frame)

    def split_sets_time(self):
        """
        Split the input trajectory into training and test trajectories according
        to the simulation time (i.e., the image indexes). Well suited if the
        training set is generated from molecular dynamics.
        Inputs are given in the init function.
        """
        # Getting info for the current trajectory
        # Generating filenames
        self.traj_get_info()

        # Creating train_list_trajectory file
        self.train_traj = Trajectory(filename=self.train_traj_name, mode="w")
        for id in range(self.nb_training):
            frame = self.trajectory[id]
            self.train_traj.write(frame)

        # Creating test_list_trajectory file
        self.test_traj = Trajectory(filename=self.test_traj_name, mode="w")
        for id in range(self.nb_test):
            id = id + self.nb_training
            frame = self.trajectory[id]
            self.test_traj.write(frame)


if __name__ == "__main__":
    print("The python script {} is running as main".format(__file__))
    data = Train_test_split(trajectory="CO_disso.traj", training_set_percentage=0.75)
    data.split_sets_random()
