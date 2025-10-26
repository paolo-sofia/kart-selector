import logging
import random
from copy import deepcopy
from sys import stdout

import streamlit as st

# Logging setup
logger = logging.getLogger("sorteggio corsia")
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.info("Logger setup")


DEFAULT_NUMBER_KART = 15


def define_gui_and_return_form() -> int | None:
    st.set_page_config(page_title="Sorteggio corsia", page_icon="🎲")
    st.title("Sorteggio Corsia Kart")
    form = st.form("form")

    num_corsie: int | None = form.number_input(
        "Seleziona il numero di corsie kart da sorteggiare:",
        min_value=1,
        max_value=100,
        value=DEFAULT_NUMBER_KART,
        step=1,
    )

    submit: bool = form.form_submit_button("Sorteggia")

    return num_corsie if submit else None


def sorteggio(corsie: list[str]) -> dict[int, str]:
    corsie_da_sorteggiare: list[str] = deepcopy(corsie)
    kart_da_sorteggiare: list[int] = list(range(1, len(corsie) + 1))

    sorteggio: dict[int, str] = {}

    for kart in kart_da_sorteggiare:
        index: int = random.randint(a=0, b=len(corsie_da_sorteggiare) - 1)
        sorteggio[kart] = corsie_da_sorteggiare.pop(index)

    return sorteggio


def main() -> None:
    num_corsie_da_sorteggiare: int | None = define_gui_and_return_form()

    if not num_corsie_da_sorteggiare:
        return

    corsie: list[str] = ["Rossa"] * (num_corsie_da_sorteggiare // 2) + ["Bianca"] * (
        num_corsie_da_sorteggiare // 2
    )

    if num_corsie_da_sorteggiare % 2 != 0:
        corsie.append(random.choice(["Rossa", "Bianca"]))

    corsie_sorteggiate: dict[str, int] = sorteggio(corsie)

    data: dict[str, list[str, int]] = {
        "kart": list(corsie_sorteggiate.keys()),
        "corsia": list(corsie_sorteggiate.values()),
    }

    st.dataframe(data, hide_index=True)


main()
