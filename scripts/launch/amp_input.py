from amp import Amp
from amp.descriptor.gaussian import Gaussian
from amp.model.neuralnetwork import NeuralNetwork

#=============================================================================
#   AMP_run.py
#   Description: 
#=============================================================================
#=============================================================================
# initializing some variables
#=============================================================================
traj_name = 'trajectory.traj'
#=============================================================================
# training NN
#=============================================================================
calc = Amp(descriptor=Gaussian(),
           model=NeuralNetwork(hiddenlayers=(10, 10)), PARALLEL)

calc.model.lossfunction.parameters['convergence'].update(
	{'energy_rmse':0.1,
	 'energy_maxresid': 0.1,
	 'force_rmse':0.1})

calc.train(images=traj_name)
