from app import *

db.create_all()

def declare_chal(data):
    chal = Challenges.query.filter_by(level=data["level"]).first()
    if chal is not None:
        for n in data:
            if n == "name": continue
            setattr(chal, n, data[n])
    else:
        data["solves"] = "0"
        db.session.add(Challenges(**data))
    db.session.commit()

declare_chal({
    "level": 0,
    "info": """
    test challenge 0<br>
    flag = works
""",
    "flag": 'works'
})

declare_chal({
    "level": 1,
    "info": """
    test challenge 1<br>
    flag = works1
""",
    "flag": 'works1'
})
