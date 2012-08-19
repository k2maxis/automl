automl
======

Toolbox for aggregating automotive data and the hundred of attributes for each vehicle

Inputs are lists, such as [Manufacturer] or [Manufacturer Model]  and outputs are same list with logic around
mis-spellings, inconsistencies etc due to manual entry.  Undetermined entries are returned as NULL, rather than 
with the original garbage.

The goal is too catch the bulk of errors 90%, and just set the other errors to NULL.

spellchecker.py
======

This file is run using command line, for help run `python spellchecker.py -h`.
You can supply a word for it to spellcheck (if there are spaces, use surrounding double-quotes), or you can also use other arguments to see the whole list of manufacturers or add new ones.