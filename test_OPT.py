from ase import Atoms
from ase.optimize import BFGS
from ase.constraints import FixAtoms
from ase.io import read, write, Trajectory
from ase.calculators.espresso import Espresso
from wrapper_almace import wrapperALMACE
import sys
import os


def opt(estructura, host):
    basename = os.path.splitext(estructura)[0]
    trajname = basename + 'BFGS.traj'
    finalxyz = basename + 'end.xyz'

    atoms = read(estructura)


    pseudo = {'C': 'C.pbe-n-kjpaw_psl.1.0.0.UPF',
                'O': 'O.pbe-n-kjpaw_psl.1.0.0.UPF',
                'Cu': 'Cu.pbe-spn-kjpaw_psl.1.0.0.UPF',
                'H': 'H.pbe-kjpaw_psl.1.0.0.UPF',
                'N': 'N.pbe-n-kjpaw_psl.1.0.0.UPF'}


    conf_qe = {'kpts': [3,3,1], 'ecutwfc': 40, 'tprnfor': True, 'disk_io' : 'none',
                    'pseudo_dir' : '/lus/eagle/projects/catalysis_aesp/raymundohe/espresso/pseudo',
                    'occupations':'smearing', 'smearing':'mv', 'input_dft':'BEEF-vdW',
                    'degauss':0.01, 'nosym':True, 'mixing_mode':'local-TF',
                    'pseudopotentials':pseudo, 'conv_thr': 1e-6,
                    'command': 'mpiexec --hosts localhost -n 4 --ppn 4 --depth=8 --cpu-bind depth --env OMP_NUM_THREADS=8 --env CUDA_VISIBLE_DEVICES=0,1,2,3 /soft/applications/quantum_espresso/7.3.1-nvhpc23.1-libxc610/bin/pw.x  -nk 4 -in PREFIX.pwi > PREFIX.pwo'

              }

    kwargs = {
              'sub_software':'Espresso',
              'storage':'/lus/eagle/projects/catalysis_aesp/raymundohe/testPyntaMultiNode/storage',
              'opt_method':'BFGS',
              'debug': False,
              'sub_software_kwargs': conf_qe,
              'host' : host,
              'conect': True,

              }

    constraint = FixAtoms(indices=list(range(18)))
    atoms.set_constraint(constraint)

    atoms.calc = wrapperALMACE(**kwargs)

    opt = BFGS(atoms, trajectory=trajname)
    opt.run(fmax=0.05)

    atoms.write(finalxyz)


if __name__ == '__main__':
    st   = sys.argv[1]
    host = sys.argv[2]

    print(f" Optimization for: {st}")
    opt(st, host)
