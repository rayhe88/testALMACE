from ase.calculators.calculator import Calculator
from ase.io import write, read
from ase.units import Bohr
#from pynta.utils import name_to_ase_software
import os
import json
import subprocess
import shutil
import numpy as np
import yaml

def name_to_ase_software(software_name):
    """
    go from software_name to the associated
    ASE calculator constructor
    """
    if software_name == "XTB":
        module = import_module("xtb.ase.calculator")
        return getattr(module, software_name)
    else:
        module = import_module("ase.calculators."+software_name.lower())
        return getattr(module, software_name)


class wrapperALMACE(Calculator):
    implemented_properties = ['energy', 'forces']

    def __init__(self, **kwargs):
        Calculator.__init__(self, **kwargs)
        self.python_bin = '/lus/eagle/projects/catalysis_aesp/raymundohe/maceFlow/mace_env311/bin/python'
        self.almace = '/lus/eagle/projects/catalysis_aesp/raymundohe/testPyntaMultiNode/testOpt/almace.py'

        if 'host' in kwargs:
            self.host = kwargs['host']
            self.conect = True
        else:
            self.host = 'localhost'
            self.conect = False

        if 'opt_method' in kwargs:
            self.opt_method = kwargs['opt_method']
        else:
            self.opt_method = None

        if 'sub_software' in kwargs:
            self.sub_software = kwargs['sub_software']
        else:
            self.sub_software = 'Espresso'

        if 'sub_software_kwargs' in kwargs:
            self.sub_software_kwargs = kwargs['sub_software_kwargs']
        else:
            print(" You need a DFT software for ALMACE")


        if 'storage' in kwargs:
            self.storage = kwargs['storage']
        else:
            self.storage = None

        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            self.debug = False

    def calculate(self, atoms, properties, system_changes):
        Calculator.calculate(self, atoms, properties, system_changes)

        # Create the input
        atoms.write('input.xyz')

        cwd_path = os.getcwd()

        if self.sub_software_kwargs is not None:
            file_yaml = os.path.join(cwd_path,'sub_software.yaml')

            with open(file_yaml, 'w') as file:
                yaml.dump(self.sub_software_kwargs, file)

        if self.opt_method == 'MDMin':
            self.Training = False
        else:
            self.Training = True

        if self.debug:
            print(" Current directory",cwd_path)
            print(" runing in the host : ",self.host)

        if self.Training == True:
            if self.conect == True:
                import subprocess
                with subprocess.Popen(['ssh','-T', self.host],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True) as p:
                    output, error = p.communicate(f""" cd {cwd_path}
                    echo `pwd`
                    module use /soft/modulefiles
                    module load conda
                    module load PrgEnv-nvhpc nvhpc cudatoolkit-standalone/11.8.0
                    module load cray-hdf5
                    module list
                    conda activate /lus/eagle/projects/catalysis_aesp/raymundohe/maceFlow/mace_env311
                    export MPICH_GPU_SUPPORT_ENABLED=0

                    {self.python_bin} {self.almace} input.xyz {cwd_path} {self.storage} {self.sub_software} sub_software.yaml
                    """)
                    #print(output)
                    #print(error)
            else:
                import subprocess
                command = f'{self.python_bin} {self.almace} input.xyz {cwd_path} {self.storage} {self.sub_software} sub_software.yaml'
                subprocess.run(command, shell=True)

            with open("input.json", "r") as file:
                data_json = json.load(file)
            self.results['energy'] = data_json['energy']
            self.results['forces'] = np.array(data_json['forces'])
            atoms.info['energy'] = self.results['energy']
            atoms.arrays['forces'] = self.results['forces']

        else:
            print(" >> Entramos a DFT no pasamos por ALMACE")
            atoms.calc = name_to_ase_software(self.sub_software)(**self.sub_software_kwargs)
            atoms.info['energy'] =  atoms.get_potential_energy()
            atoms.arrays['forces'] = atoms.get_forces()
            self.results['energy'] = atoms.info['energy']
            self.results['forces'] = atoms.arrays['forces']

            write('almaceDFT000.xyz', atoms)

            if self.storage is not None:
                if not os.path.exists(self.storage):
                    os.makedirs(self.storage)

                src = os.path.join(os.getcwd(), "almaceDFT000.xyz");
                dst = os.path.join(self.storage, "almaceDFT000.xyz");

                if os.path.exists(dst):
                    count = 1
                    while True:
                        new_name = f"almaceDFT{count:03d}.xyz"
                        new_path = os.path.join(self.storage, new_name)
                        if not os.path.exists(new_path):
                            dst = new_path
                            break
                        count +=1
                shutil.copy(src, dst)

        return atoms
