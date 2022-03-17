
Star Catalog for Napier Telescopes
=============================

This is an IPython notebook for looking up star info for the Napier building telescopes.

- `StarCatalog.py`
- `StarCatalog.db`
- `StarCatalog.csv`
- A README file
- This iPython notebook


Instructions
-----------------

Import the library with `import StarCatalog as sc` then initialise it with `sc.sc_open()`

The main functions you'll want to use are:
- `sc.observe(star_name)`  The variable `star_name` needs to be a string in quotes, but does not need to be an exact match. If there is more than one match, it will prompt the user to choose.
- `sc.info(star_number)`  The variable `star_number` is simply the star number you want information on.

If you want to add your own stars/objects to the database, you can use the following function:
`sc.add_star(star_num, ra, dec, size, mag, type_and_desc, alt_name, q_tags, common_name, comments)`
or
`sc.add_star_quick(star_num, ra, dec, mag, alt_name, common_name)`

If a star's data is wrong (there will definitely be some errors) you can change it yourself (after letting me know at cm430@, or by opening a github issue/pull request) by using an update command:
`sc.update_attribute(star_num, value)`
replacing `attribute` with one of the following column headers:
- `ra` (right ascension)
- `dec` (declination)
- `size` (apparent size in sky?)
- `mag` (apparent magnitude)
- `type_and_desc` (type of star and description of it)
- `alt_name` (alternative name for the star, usually not the common one)
- `q_tags` (unsure what this is for, let me know if you do)
- `common_name` (common name for the star if it has one)
- `comments` (additional comments on the star)

If you want to quit before exiting Python, run `sc.sc_close()`



Final notes
---------------

Any bugs, questions, feature requests or changes, email me at cm430@ (or drop an issue on GitHub).
If you find a mistake, make sure to email me and I can update the master files.

I chose an iPython notebook because it's the simplest interactive Python prompt I know of with all of the dependencies and most people should have it anyway.
If you want help or a different way, again email me.

Author: Callum McGregor

