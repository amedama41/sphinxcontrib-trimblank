#######################
sphinxcontrib-trimblank
#######################

.. image:: https://travis-ci.org/amedama41/sphinxcontrib-trimblank.svg?branch=master
   :target: https://travis-ci.org/amedama41/sphinxcontrib-trimblank

A Sphinx extension, which trims redundant blanks generated due to line breaks or inline-markups from generated documents.

.. note::

   This extension is inspired by `japansesupport.py`_.
   sphinxcontrib-trimblank is more friendly for ascii characters appearing
   in your document.

.. _`japansesupport.py`: https://bitbucket.org/sphinxjp/goodies/raw/86cd22393f6d707fa7fe394b47cd0db4e1968e2f/exts/japanesesupport/japanesesupport.py

*******
Install
*******

Use pip:

.. code:: sh

   pip install sphinxcontrib-trimblank

*****
Usage
*****

Only add 'sphinxcontrib.trimblank' to ``extensions`` option in **conf.py**:

.. code:: python

   extensions += ['sphinxcontrib.trimblank']

If you want to change the extension behaviour, configure options in **conf.py**:

.. code:: python

   # Keep blanks to adjacent to ascii characters in html documents
   trimblank_keep_alnum_blank = ['html', 'singlehtml']

All options are listed in `Configuration`_.

Configuration
=============

.. list-table::
   :header-rows: 1

   * - option name
     - meaning
     - default
   * - trimblank_enabled
     - A list of builder names ('html', 'singlehtml', 'latex', and so on).
       Only when the builder in the list is used, sphinxcontrib-trimblank will
       trim blanks.
       The value may also be a boolean. Then the extension will do, or not do
       for any builder.
     - ``True``
   * - trimblank_keep_alnum_blank
     - A list of builder names ('html', 'singlehtml', 'latex', and so on).
       Only when the builder in the list is used, sphinxcontrib-trimblank will
       keep blanks adjacent to an ascii character.
       The value may also be a boolean. Then the extension will do, or not do
       for any builder.
     - ``False``
   * - trimblank_keep_blank_before
     - A regular expression pattern string to specified characters, which
       sphinxcontrib-trimblank will keep blanks just before.
     - ``'[\s(]'``
   * - trimblank_keep_blank_after
     - A regular expression pattern string to specified characters, which
       sphinxcontrib-trimblank will keep blanks just after.
     - ``'[\s),.:?]'``
   * - trimblank_debug
     - If this value is ``True``, the trimmed texts are output as building messages.
     - ``False``

*******
Licence
*******

MIT Licence

