FullMoon
========

This python module is a translation and implementation of the
`Astro::MoonPhase Perl module`_ via the `Ruby implementation`_. You can
use this module to determine the occurrence of the next full moon or to
determine if a given date is/was/will be a full moon.

Installation
------------

Add this line to your application’s Gemfile:

.. code:: python

   pip install fullmoon

Usage
-----

Two classes can be called. One determines the next full moon. The other
determines if a given date is a full moon or not.

.. code:: python

   from fullmoon import NextFullMoon
   from fullmoon import IsFullMoon

   ###################################
   #   Next Full Moon Examples
   ###################################

   n = NextFullMoon() 

   # Iterate through all next full moon from "now"
   print(n.next_full_moon())
   print(n.next_full_moon())

   # Restart from "now"
   print(n.reset().next_full_moon())
   print(n.next_full_moon())

   # Change the origin to 1998-07-12
   print(n.set_origin_date_string('1998-07-12').next_full_moon()) # PRINT: 1998-08-07
   print(n.next_full_moon()) # PRINT: 1998-09-06       

   # Reset the origin to 1998-07-12
   n.reset()
   print(n.next_full_moon()) # PRINT: 1998-08-07

   # Reset the origin to "now"
   print(n.set_origin_now().next_full_moon())


   ###################################
   #   Is Full Moon Examples
   ###################################

   i = IsFullMoon()

   # Check if "now" if full moon
   print(i.is_full_moon())

   # Check if "1998-07-12" is full moon
   print(i.set_date_string('12/07/1992', '%d/%m/%Y').is_full_moon()) # PRINT: False

Contributing
------------

Bug reports and pull requests are welcome on GitHub at
https://github.com/jr-k/fullmoon. This project is intended to be a safe,
welcoming space for collaboration, and contributors are expected to
adhere to the `Contributor Covenant`_ code of conduct.

License
-------

The module is available as open source under the terms of the `MIT
License`_.

.. _`Astro::MoonPhase Perl module`: http://search.cpan.org/~brett/Astro-MoonPhase-0.60/MoonPhase.pm
.. _Ruby implementation: https://raw.githubusercontent.com/psoliver92/full-moon
.. _Contributor Covenant: http://contributor-covenant.org
.. _MIT License: https://opensource.org/licenses/MIT