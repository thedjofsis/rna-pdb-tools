#!/usr/bin/python
# -*- coding: utf-8 -*-

"""RNA refinement with QRNAS

Right now, there is 20k steps of refinement.

Installation of QRNAS
-----------------------------------------
Install (http://genesilico.pl/qrnas). Download the QRNAS package from http://genesilico.pl/qrnas/,
 unzip the archive, and compile it with the following command::

    ./qrnamake sequential

This should create an executable version of QRNAS.

Be default the script searches QRNAS in (rna-pdb-tools)/opt/qrnas/ .

Usage of QRNA::

    QRNA - Quick Refinement of Nucleic Acids (0.2 alpha)
         by Juliusz Stasiewicz (jstasiewicz@genesilico.pl)

    To use type:
      QRNA -i <input PDBfile> [-o <output PDBfile>] [-c <configfile>] [-p] [-m <restraintsfile>]
    OR specify <input PDBfile>, <output PDBfile> and <restraintsfile> in <configfile> and type just:
      QRNA -c <configfile>

Installation of this utils
-----------------------------------------

Set up in your bashrc::

   export QRNAS_PATH=<your path to qrnas> # e.g. /home/magnus/src/rna-pdb-tools/opt/qrnas

but default rna-pdb-tools searches for qrnas in <rna-pdb-tools>/opt/qrnas.

DONE:

- [x] onfiguration should not be hardcoded
"""

from __future__ import print_function
import argparse
import re
import os
import subprocess
import random
import string

from shutil import copyfile

PATH = os.environ['RNA_PDB_TOOLS']
QRNAS_PATH = os.getenv('QRNAS_PATH', PATH + '/opt/qrnas/')

class QRNAS:
    """QRNAS"""
    def run(self, inputfile, outputfile, steps = 10):
        """
        :param inputfile: 
        :param outputfile: 
        :param steps: 
        """
        cwd = os.getcwd()
        # get config
        conftxt = open(QRNAS_PATH + os.sep + 'configfile.txt').read()
        conftxt_tmp = re.sub('\#?\s?NSTEPS.+\d+', 'NSTEPS   ' + str(steps), conftxt)
        JOB_ID = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
        JOB_PATH = QRNAS_PATH + os.sep + 'jobs/' + JOB_ID
        os.makedirs(JOB_PATH)

        # get temp config
        with open(JOB_PATH + os.sep + 'configfile.txt','w') as f:
            f.write(conftxt_tmp)

        # copy input to qrnas folder
        qrnas_inputfile = QRNAS_PATH + os.sep + 'jobs/' + JOB_ID + os.sep + os.path.basename(inputfile)
        copyfile(inputfile, qrnas_inputfile)

        os.chdir(QRNAS_PATH)
        cmd = './QRNAS -i jobs/' + JOB_ID + os.sep + os.path.basename(inputfile) + \
          ' -c jobs/' + JOB_ID + os.sep + 'configfile.txt ' + \
          ' -o jobs/' + JOB_ID + os.sep + os.path.basename(inputfile).replace('.pdb', '.refi.pdb')
        print(cmd)
        subprocess.call(cmd, shell=True)

        os.chdir(cwd)
        copyfile(QRNAS_PATH + '/jobs/' + JOB_ID + os.sep + os.path.basename(inputfile).replace('.pdb', '.refi.pdb'), outputfile)

def get_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-s', '--steps', help="# of steps, default: 20k ", default=20000)         
    parser.add_argument('fn', help="input pdb file")     
    #parser.add_argument('outputfile', help="output pdb file")
    return parser
#main
if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    q = QRNAS()
    q.run(args.fn, args.fn.replace('.pdb', '._refi.pdb'), steps = args.steps)