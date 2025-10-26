import random

from copy import deepcopy
from typing import Any


def sorteggio(
    piloti: list[Any], prev_sorteggio: dict[Any, int] | None = None, extra_kart: int = 0
) -> dict[Any, int]:
    piloti_shuffle: list[Any] = deepcopy(piloti)
    random.shuffle(x=piloti_shuffle)

    nuovo_sorteggio: dict[Any, int] = {}
    kart_sorteggiati: list[int] = []
    for pilota in piloti_shuffle:
        pilota_kart_da_sorteggiare: list[int] = list(
            range(1, len(piloti) + extra_kart + 1, 1)
        )

        pilota_kart_da_sorteggiare = list(
            set(pilota_kart_da_sorteggiare) - set(kart_sorteggiati)
        )

        if (
            prev_sorteggio
            and len(pilota_kart_da_sorteggiare) > 1
            and prev_sorteggio[pilota] in pilota_kart_da_sorteggiare
        ):
            index: int = pilota_kart_da_sorteggiare.index(prev_sorteggio[pilota])
            pilota_kart_da_sorteggiare.pop(index)

        kart: int = random.choice(pilota_kart_da_sorteggiare)
        nuovo_sorteggio[pilota] = kart
        kart_sorteggiati.append(kart)

    return nuovo_sorteggio
