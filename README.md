# Incrypt-[X]

Forked from [andreafioraldi/motherfucking-ctf](https://github.com/andreafioraldi/motherfucking-ctf).
Thanks [supersam9899](https://github.com/supersam9899) for the new design!

Define a description of the CTF in `templates/index.html`.

Install requirements `pip install -r requirements.txt`

Define the set of challenges in `chals.py`.

Run `python chals.py` to setup the database.

Run `python run.py` and you are up.

## TODO
- [ ] Update `requirements.txt`
- [ ] Rewrite README properly.
- [ ] Refactor and properly recomment `app.py`.
- [ ] Replace `chals.py` with a config file.
- [ ] Deal with timezone problems.
  - [ ] Fix `get_hms` to deal with multi-day contests.
  - [ ] Fix the 23 minute offset.
