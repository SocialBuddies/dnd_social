from core.models import Alignment


def add_alignments():
    ALIGNMENTS = [
        "Lawful Good",
        "Neutral Good",
        "Chaotic Good",
        "Lawful Neutral",
        "Neutral Neutral",
        "Chaotic Neutral",
        "Lawful Evil",
        "Neutral Evil",
    ]

    for tmp in ALIGNMENTS:
        obedience, alignment = tmp.split(" ")
        Alignment.objects.get_or_create(obedience=obedience, alignment=alignment)


add_alignments()
