# Yummy things I like making and eating :)

This is a personal project to store my favorite recipes on a website so I no longer wonder where did I get this recipe from. Recipes on this site can be from a friend, family member, an Instagram post, a book, or from me. I will list the source if applicable. 

I am using a postgres database to store my recipes as a good excuse to use postgres. Probably total overkill but that is what I am doing. I am also using [pdm scripts](https://pdm-project.org/latest/usage/scripts/) instead of a Makefile.

## Steps (all defined in pyproject.toml file):
* Create a local instance of the database with Docker: `pdm create`
* Run migration to create all tables in the database with `pdm migrateup`
* Connect to the database with `pdm connect`

The basic flow of the app is [here](https://play.d2lang.com/?script=rJIxawMxDIV3_wovGXOGgyxHKXTJlNK5U1BsxTY9n11JuRBK_3txuEsz9IZAxyfhp6dPdpHQSsxDpyn6IEodKJ8ZqdNfSutoayeIFO6MqYobQSJgoZOVxuZkBG1Ytdvp3bptePRKaw5QsNMxgUf1rRQjjY_YOhxX7bZcJORhwdKBwAEYHzbNLJ6QP_ulrJZikX_NeoHU_2V4Kn0G15zjR0zoIjSZvKmqVGVsTikPbDZmA-bteIw2Qr9_f3nd7XfZ54VhE2y9fta_jOatb9hqe75Krc2nv69fY97Z3X5HkNRfl9JPaz3zIgQ3wVuY_RMAAP__&) and the ERD is [here](https://dbdiagram.io/d/recipes-677806ba5406798ef736de6e).