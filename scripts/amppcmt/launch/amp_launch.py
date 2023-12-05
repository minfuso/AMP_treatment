from amp import Amp
from amp.descriptor.gaussian import Gaussian
from amp.model.neuralnetwork import NeuralNetwork
from jinja2 import Template

class Launch():
    
    def __init__(
        self,
        traj_name:str,
        amp_param:str = None,
        hiddenlayers:tuple = (10,10),
        checkpoints:int = -100,
        forces:bool = False,
        convergence_parameters:dict =
            # {
            # 'energy_rmse':0.001,
            # 'force_rmse': None,
            # 'energy_maxresid': None,
            # 'force_maxresid': None
            # },
            None,
        initial_calc:bool = True,
        test:bool = False,
        filename:str = 'amp_launch.py'):
        
        self.traj_name = traj_name
        self.amp_param = amp_param
        self.hiddenlayers = hiddenlayers
        self.checkpoints = checkpoints
        self.forces = forces
        self.initial_calc = initial_calc
        self.test = test
        self.filename = filename
        # Assigning default convergence parameters value
        default_convergence_parameters = {
            'energy_rmse':0.001,
            'force_rmse': None,
            'energy_maxresid': None,
            'force_maxresid': None
        }
        self.convergence_parameters = default_convergence_parameters
        # Updating default values by personal ones
        if convergence_parameters is not None:
            for key, value in convergence_parameters.items():
                self.convergence_parameters[key] = value
        
    def generate_input(self):
        template = Template(open('scripts/amppcmt/launch/template_script.jinja2').read())
        rendered_script = template.render(
                traj_name = self.traj_name,
                amp_param = self.amp_param,
                initial_calc = self.initial_calc,
                hiddenlayers = self.hiddenlayers,
                checkpoints = self.checkpoints,
                convergence_parameters = self.convergence_parameters,
                test = self.test
        )
        with open(self.filename, 'w') as file:
            file.write(rendered_script)
            
if __name__ == '__main__':
    test = Launch(
        traj_name = 'Cluster_test/Test_relaunch/Train.traj',
        amp_param = 'Cluster_test/Test_relaunch/amp-untrained-parameters.amp',
        hiddenlayers = (10, 10),
        checkpoints = -100,
        forces = False,
        initial_calc = False,
        convergence_parameters = {
            'energy_rmse':0.001,
            'force_rmse': None,
            'energy_maxresid': None,
            'force_maxresid': None
        },
        filename = 'test_first_calc.py',
        test = True
        )
    
    test.generate_input()