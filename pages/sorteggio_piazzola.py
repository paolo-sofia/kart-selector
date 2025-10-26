import logging
from sys import stdout

import streamlit as st

from src.common import sorteggio

# Logging setup
logger = logging.getLogger("sorteggio piazzola")
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.info("Logger setup")


DEFAULT_NUMBER_KART: int = 15


def define_gui_and_return_form() -> int | None:
    st.set_page_config(page_title="Sorteggio kart", page_icon="🎲")
    st.title("Sorteggio Piazzole Kart")

    form = st.form("form")
    num_kart: int | None = form.number_input(
        "Seleziona il numero di piazzole kart da sorteggiare:",
        min_value=1,
        max_value=100,
        value=DEFAULT_NUMBER_KART,
        step=1,
    )

    submit: bool = form.form_submit_button("Sorteggia")

    return num_kart if submit else None


def main() -> None:
    num_kart_da_sorteggiare: int = define_gui_and_return_form()

    if not num_kart_da_sorteggiare:
        return

    risultato_sorteggio: dict[int, int] = sorteggio(
        piloti=list(range(1, num_kart_da_sorteggiare + 1))
    )

    risultato_sorteggio = dict(sorted(risultato_sorteggio.items()))
    data: dict[str, list[int]] = {
        "pilota": list(risultato_sorteggio.keys()),
        "piazzola": list(risultato_sorteggio.values()),
    }

    st.dataframe(data, hide_index=True)


main()
