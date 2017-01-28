SMPOST: Social Media POS Tagger
===================

The tagger was build as a part of the [shared task](http://ltrc.iiit.ac.in/icon2016/) at ICON, 2016.

For understanding how SMPOST works, please visit [here](https://github.com/stripathi08/pos_cmism) and see our publication for the same.

----------


Installation
-------------
- Pre-requisites : [CRF++](https://taku910.github.io/crfpp/), [Pickle](https://docs.python.org/3/library/pickle.html)
- Clone the repository.
- Move in the directory and run the **setup.py** file.

```
git clone https://github.com/stripathi08/smpost.git
python setup.py install
```
Usage
-------------------
```
from SMPOST.main import smpost

sample_text = ['input sentence here']
pre_class = smpost(lang = 'BN')
pre_class.predict(sample_text)
```
- Language argument (lang) can take three values, **'BN'**, **'HI'**, **'TE'**

Reporting Doubts and Errors
-------------------
- For any queries, please contact at **stripathi1770@gmail.com**.
- Please refer to the publication for detailed results.

Citing the paper
-------------------
- If you are using the code for research purposes, please cite the paper. **SMPOST: Parts of Speech Tagger for Code-Mixed Indic Social Media Text**

Next Versions
-------------------
- To include Coarser tag set and both the constrained runs.
- BLSTM framework for the same.
- Improved feature set as used in the [work](https://github.com/stripathi08/pos_cmism).
