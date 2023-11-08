# Importation
from ase.io import read, Trajectory
import random
from functools import wraps
import time
import logging
import os

# Create and configure logger
print('Log: ', os.getcwd()+'/'+os.path.basename(__file__).split(sep=".")[0] + ".log")
logging.basicConfig(
    filename=os.getcwd()+'/'+os.path.basename(__file__).split(sep=".")[0] + ".log", format="%(message)s", filemode="w"
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

    @timeit
    def split_sets_random(self):
        """
        Split the input trajectory into training and test trajectories. Inputs are given
        in the init function.
        """
        print("The trajectory is composed by {} frames".format(self.total_length))
        nb_training = round(self.training_set_percentage * self.total_length)
        nb_test = self.total_length - nb_training
        print("The number of frames in the training set is: {}".format(nb_training))
        print("The number of frames in the test set is: {}".format(nb_test))
        logger.debug("The number of frames in the training set is: {}".format(nb_training))
        logger.debug("The number of frames in the test set is: {}".format(nb_test))

        # Randomly selecting configurations for the test set (smaller)
        id_test_list = random.sample(range(0, self.total_length), nb_test)

        # Generating filenames
        test_traj_name = self.trajectory_name.split(sep=".")[0] + "_test.traj"
        train_traj_name = self.trajectory_name.split(sep=".")[0] + "_train.traj"

        # Creating test_list_trajectory file
        self.test_traj = Trajectory(filename=test_traj_name, mode="w")
        for id in id_test_list:
            frame = self.trajectory[id]
            self.test_traj.write(frame)
        print("The test trajectory is saved as {}".format(test_traj_name))
        logger.debug("The test trajectory is saved as {}".format(test_traj_name))


        # Creating train_list_trajectory file
        self.train_traj = Trajectory(filename=train_traj_name, mode="w")
        for id in range(self.total_length):
            # Passing if id is in the test set
            if id in id_test_list:
                continue
            frame = self.trajectory[id]
            self.train_traj.write(frame)
        print("The train trajectory is saved as {}".format(train_traj_name))
        logger.debug("The train trajectory is saved as {}".format(train_traj_name))


if __name__ == "__main__":
    print("The python script {} is running as main".format(__file__))
    data = Train_test_split(trajectory="CO_disso.traj", training_set_percentage=0.75)
    data.split_sets_random()
