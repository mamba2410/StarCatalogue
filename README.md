
Star Catalog for Napier Telescopes
=============================

This is an IPython notebook for looking up star info for the Napier building telescopes.

- <code>StarCatalog.py</code>
- <code>StarCatalog.db</code>
- <code>StarCatalog.csv</code>
- A README file
- This iPython notebook


Instructions
-----------------

Import the library with <code>import StarCatalog as sc</code> then initialise it with <code>sc.sc_open()</code>

The main functions you'll want to use are:
- <code>sc.observe(_star-name_)</code>  The variable _star-name_ needs to be a string in quotes, but does not need to be an exact match. If there is more than one match, it will prompt the user to choose.
- <code>sc.info(_star-number_)</code>  The variable _star-number_ is simply the star number you want information on.

If you want to add your own stars/objects to the database, you can use the following function:
<code>sc.add_star(star_num, ra, dec, size, mag, type_and_desc, alt_name, q_tags, common_name, comments)</code>
or
<code>sc.add_star_quick(star_num, ra, dec, mag, alt_name, common_name)</code>

If a star's data is wrong (there will definitely be some errors) you can change it yourself (after letting me know at cm430@) by using an update command:
<code>sc.update_attribute(star_num, value)</code>
replacing _attribute_ with one of the following column headers:
- ra (right ascension)
- dec (declination)
- size (apparent size in sky?)
- mag (apparent magnitude)
- `type_and_desc` (type of star and description of it)
- `alt_name` (alternative name for the star, usually not the common one)
- `q_tags` (unsure what this is for, let me know if you do)
- `common_name` (common name for the star if it has one)
- comments (additional comments on the star)

If you want to quit before exiting Python, run <code>sc.sc_close()</code>



Final notes
---------------

Any bugs, questions, feature requests or changes, email me at cm430@ (or drop an issue on GitHub.
If you find a mistake, make sure to email me and I can update the master files.

I chose an iPython notebook because it's the simplest interactive Python prompt I know of with all of the dependencies and most people should have it anyway.
If you want help or a different way, again email me.

Author: Callum McGregor

