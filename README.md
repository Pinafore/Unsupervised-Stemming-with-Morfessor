# Unsupervised-morphological-segmentation-with-Morfessor

This stemmer uses Morfessor 2.0 (Virpioja,et al. 2013) and Morfessor FlatCat 1.0 (Grönroos, et al. 2014).
* Stemming_unsupervised.py is the code for unsupervised stemming.
* The sample data to be stemmed is in raw/en/ and raw/tr/.
* The output will be stored in segmented/en/ and segmented/tr/ respectively.

## Setup
Before running the code, please install Morfessor 2.0 (http://morfessor.readthedocs.io/en/latest/installation.html) and Morfessor FlatCat 1.0.5 (http://morfessor-flatcat.readthedocs.io/en/latest/installation.html#installation-instructions).

## Running Example
`$ python Stemming_unsupervised.py raw/en/ segmented/en/`

