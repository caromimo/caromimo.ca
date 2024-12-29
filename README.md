# Yummy things I like making and eating :)

This is a personal project to store my favorite recipes on a website so I no longer wonder where did I get this recipe from. Recipes on this site can be from a friend, family member, an Instagram post, a book, or from me. I will list the source if applicable. 

I am using a postgres database to store my recipes as a good excuse to use postgres. Probably total overkill but that is what I am doing. I am also using [pdm scripts](https://pdm-project.org/latest/usage/scripts/) instead of a Makefile.

## Steps (all defined in pyproject.toml file):
* Create a local instance of the database with Docker: `pdm create`
* Run migration to create all tables in the database with `pdm migrateup`
* Connect to the database with `pdm connect`

The basic flow is [here](https://play.d2lang.com/?script=SirKLy9OLeIqTi0qSy3iSkksSUxKLE7lggoo6NopwMSsFIIDfeAqQDIQNVZgFVxQk5DFM0pKCpAMgqoAiefmcAECAAD__w%3D%3D&).