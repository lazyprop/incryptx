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
    The Trickster<br>
    https://files.catbox.moe/6zsyvd.zip
""",
    "flag": 'awakening'
})

declare_chal({
    "level": 1,
    "info": """
    <img src="https://cdn.discordapp.com/attachments/767286724601839627/774273383469678622/lvl2.jpg"
    width=50% height=50%>
""",
    "flag": 'amongus'
})

declare_chal({
    "level": 2,
    "info": """
    https://www.youtube.com/watch?v=LuTJQQU160w<br>
    https://files.catbox.moe/fqbiws.zip
""",
    "flag": 'cve202012352'
})

declare_chal({
    "level": 3,
    "info": """
    <img src="https://t6.rbxcdn.com/d5020e9b94187c1e37d0eeb1ac715354"
    width=50% height=50%>
""",
    "flag": 'cocoapress'
})

declare_chal({
    "level": 4,
    "info": """
    https://bit.ly/32jnzea
""",
    "flag": 'generation um...'
})

declare_chal({
    "level": 5,
    "info": """
     When in times of turmoil and breakup, do not cut or shave your head, because it will<br>
     never end well.<br>
     https://files.catbox.moe/6zsyvd.zip
""",
    "flag": 'petehawley'
})

declare_chal({
    "level": 6,
    "info": """
    <img src="https://i.imgur.com/96KW6O9.png"
    width=50% height=50%>
""",
    "flag": 'u/moonlight296'
})


declare_chal({
    "level": 7,
    "info": """
    bit.ly/sg14fhjf<br>
    bit.ly/3l5mSfV<br>
    https://files.catbox.moe/xnek48.zip
""",
    "flag": 'sleight'
})


declare_chal({
    "level": 8,
    "info": """
    <a href="https://bit.ly/32hRD9X">courage and heroism</a><br>
    the image contains a hidden message
""",
    "flag": 'goldstar'
})


declare_chal({
    "level": 9,
    "info": """
    The Nine Muses-Urania, Erato, Terpsichore, and the rest-met to sing<br>
    and dance on the slopes of Mount Olympus, surrounded by the honey bees<br>
    which attended them. One day a goat-heard named Comatas glimpsed<br>
    them dancing, and caught up in a wave of awe, sacrificed one of his goats<br>
    in their honor. When his master discovered what he had done, he ordered<br>
    that the boy be sealed into a chest to die.The Muses took pity on Comatas,<br>
    and sent their bees to carry honey to him through a crack in the chest.<br>
    When the chest was finally opened, he emerged in perfect health
""",
    "flag": 'halo2'
})

declare_chal({
    "level": 10,
    "info": """
    bit.ly/yehloyaar
    https://rb.gy/yn7tfu
    """,
    "flag": 'trinity'
})

declare_chal({
    "level": 11,
    "info": """
    Take  a look at your past before you solve this question<br>
    https://files.catbox.moe/4tzwk8.zip
""",
    "flag": 'emiew3'
})
