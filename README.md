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
> - git clone https://github.com/stripathi08/smpost.git
> - python setup.py install

Usage
-------------------
```
from SMPOST.main import SMPOST
<code blocks>
sample_text = [''] # Please fill the sample text
pre_class = smpost(lang = 'BN')
pre_class.predict(sample_text)
```
- Language argument (lang) can take three values, **'BN'**, **'HI'**, **'TE'**

Reporting Doubts and Errors
-------------------
- For any queries, please contact at **stripathi1770@gmail.com**.

- Please refer to the publication for detailed results.

Next Versions
-------------------
- To include Coarser tag set.
- Improved feature set as used in the [work](https://github.com/stripathi08/pos_cmism).
