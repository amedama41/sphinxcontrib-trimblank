#######################
sphinxcontrib-trimblank
#######################

A Sphinx extension, which trims redundant blanks generated from
line breaks or inline-markups in source reStructuredText.

.. note::

   This extension is inspired by `japansesupport.py`_.
   sphinxcontrib-trimblank is more friendly for ascii characters appearing
   in your document.

.. _`japansesupport.py`: https://bitbucket.org/sphinxjp/goodies/raw/86cd22393f6d707fa7fe394b47cd0db4e1968e2f/exts/japanesesupport/japanesesupport.py

*******
Install
*******

Install by setup.py:

.. code:: sh

   python setup.py install

*****
Usage
*****

Only add 'sphinxcontrib.trimblank' to ``extensions`` configuration of **conf.py**:

.. code:: python

   extensions += ['sphinxcontrib.trimblank']

If you want to change the extension behaviour, change the configuration variable's value in **conf.py**.
All configuration variables are listed in `Configuration`_.

Configuration
=============

.. list-table::
   :header-rows: 1

   * - variable
     - meaning
     - default
   * - trimblank_keep_blank_for_alnum
     - If this value is ``True``, the only blanks between non-ascii characters are trimmed.
     - ``False``
   * - trimblank_enabled
     - If this value is ``False``, no blanks are trimmed.
     - ``True``
   * - trimblank_debug
     - If this value is ``True``, the trimmed texts are output as building messages.
     - ``False``

*******
Licence
*******

MIT Licence

