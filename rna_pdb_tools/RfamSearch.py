#!/usr/bin/env python
from __future__ import print_function

import subprocess
import tempfile

from Seq import RNASequence
from rpt_config import RFAM_DB_PATH


class RfamSearchError(Exception):
    pass


class RfamSearch():
    """RfamSearch (local).

    Rfam is a collection of multiple sequence alignments and covariance models representing non-coding RNA families. Rfam is available on the web http://rfam.xfam.org/. The website allow the user to search a query sequence against a library of covariance models, and view multiple sequence alignments and family annotation. The database can also be downloaded in flatfile form and searched locally using the INFERNAL package (http://infernal.wustl.edu/). The first release of Rfam (1.0) contains 25 families, which annotate over 50 000 non-coding RNA genes in the taxonomic divisions of the EMBL nucleotide database.

    Infernal ("INFERence of RNA ALignment") is for searching DNA sequence databases for RNA structure and sequence similarities. It is an implementation of a special case of profile stochastic context-free grammars called covariance models (CMs). A CM is like a sequence profile, but it scores a combination of sequence consensus and RNA secondary structure consensus, so in many cases, it is more capable of identifying RNA homologs that conserve their secondary structure more than their primary sequence.

    Infernal `cmscan` is used to search the CM-format Rfam database.

    Setup:

    - download the database from ftp://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT (file: Rfam.cm.gz, ~30mb)
    - install http://eddylab.org/infernal/
    - set up ``RFAM_DB_PATH`` in the config file of rna-pdb-tools.

    Cite: Nawrocki and S. R. Eddy, Infernal 1.1: 100-fold faster RNA homology searches, Bioinformatics 29:2933-2935 (2013). """  # noqa

    def __init__(self):
        pass

    def cmscan(self, seq):
        """Run cmscan on the seq.

        Usage::

           >>> seq = RNASequence("GGCGCGGCACCGUCCGCGGAACAAACGG")
           >>> rs = RfamSearch()
           >>> hit = rs.cmscan(seq)
           >>> print(hit)  #doctest: +ELLIPSIS
           # cmscan :: search sequence(s) against a CM database...

        :param seq: string
        :returns: result
        :rtype: string """
        # make tmp file
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.name += '.fa'
        with open(tf.name, 'w') as f:
            f.write('>target\n')
            f.write(seq.seq + '\n')

        # make output file
        of = tempfile.NamedTemporaryFile(delete=False)

        # run cmscan
        cmd = 'cmscan -E 1 ' + RFAM_DB_PATH + ' ' + tf.name + '  > ' + of.name
        o = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # out = o.stdout.read().strip()
        err = o.stderr.read().strip()
        if err:
            raise RfamSearchError(err)
        self.output = open(of.name).read()
        # os.chdir(old_pwd)
        return self.output


# main
if __name__ == '__main__':
    seq = RNASequence("GGCGCGGCACCGUCCGCGGAACAAACGG")
    rs = RfamSearch()
    hit = rs.cmscan(seq)
    print(hit)

    import doctest
    doctest.testmod()
