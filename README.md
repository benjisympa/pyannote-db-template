# pyannote.database plugin for IberSpeech Challenge 2018 Albayzin

http://iberspeech2018.talp.cat/index.php/albayzin-evaluation-challenges/

This repository provides a template for creating your own [`pyannote.database`](http://github.com/pyannote/pyannote-database) plugin.

1. Fork this repository.
2. Edit `MyDatabase/__init__.py`
3. Edit `setup.py`, `setup.cfg` and `.gitattributes`
4. Edit lines 45 to 48 in `MyDatabase/_version.py`
5. Rename `MyDatabase` directory to the name of your database (e.g. to [`Etape`](http://github.com/pyannote/pyannote-db-etape) or [`REPERE`](http://github.com/pyannote/pyannote-db-repere))
6. Commit and tag your changes using [`semantic versioning`](http://semver.org)
7. Run `pip install -e .` and enjoy!
8. Edit and copy the db.yml file in your home pyannote folder : ~/.pyannote/db.yml

In case your database is public and you want to share, I'd be happy to integrate your plugin in `pyannote`: a [pull request](https://help.github.com/articles/about-pull-requests/) to this repository should help us get started...
