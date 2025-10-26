import logging
import random
from sys import stdout

import streamlit as st
from src.common import init_corsie

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
    st.set_page_config(page_title="Sorteggio Piazzola e Corsia", page_icon="🎲")
    st.title("Sorteggio Corsia")
    st.header("Istruzioni")
    st.write("""Questo programma effettua il sorteggio della corsia per ogni kart. Inserisci il numero di kart da sorteggiare e ad ogni kart verrà sorteggiata una corsia
""")

    form = st.form("form")

    num_kart: int | None = form.number_input(
        "Seleziona il numero di kart da sorteggiare:",
        min_value=1,
        max_value=100,
        value=DEFAULT_NUMBER_KART,
        step=1,
    )

    submit: bool = form.form_submit_button("Sorteggia")

    return num_kart if submit else None


def sorteggio(num_corsie: int) -> dict[int, str]:
    corsie_da_sorteggiare: list[str] = init_corsie(num_corsie)
    kart_da_sorteggiare: list[int] = list(range(1, len(corsie_da_sorteggiare) + 1))
    random.shuffle(kart_da_sorteggiare)

    sorteggio: dict[int, str] = {}

    for kart in kart_da_sorteggiare:
        index: int = random.randint(a=0, b=len(corsie_da_sorteggiare) - 1)
        sorteggio[kart] = corsie_da_sorteggiare.pop(index)

    return sorteggio


def main() -> None:
    num_corsie_da_sorteggiare: int | None = define_gui_and_return_form()

    if not num_corsie_da_sorteggiare:
        return

    corsie_sorteggiate: dict[str, int] = sorteggio(num_corsie_da_sorteggiare)

    corsie_sorteggiate = dict(sorted(corsie_sorteggiate.items()))

    data: dict[str, list[str, int]] = {
        "pilota": list(corsie_sorteggiate.keys()),
        "corsia": list(corsie_sorteggiate.values()),
    }

    st.dataframe(data, hide_index=True)


main()
