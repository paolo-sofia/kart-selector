import logging
import random
import re
from copy import deepcopy

import streamlit as st

logger = logging.getLogger(__name__)

TIPO_EVENTO_MAP: dict[str, int] = {
    "GARA": 1,
    "Q1-G1": 2,
    "Q1-G1-G2": 3,
    "Q1-Q2-G1": 3,
    "Q1-Q2-G1-G2": 4,
}


def formatted_text(to_print: str, max_value: int, bold: bool = True) -> str:
    to_add: int = max_value - len(to_print)
    st.write(f"{to_print} - to add: {to_add}")
    if bold:
        return f"**{to_print}**{to_add * ' '}"
    else:
        return f"{to_print}{to_add * ' '}"


def parse_regex(piloti_regex: str) -> list[str]:
    regex = r"\d+\-\d+"
    piloti: list[int] = []

    split_regex: list = piloti_regex.split(",")
    print(f"split_regex: {split_regex}")
    for split in split_regex:
        result: re.Match | None = re.match(regex, split)
        print(split, result)
        if not result:
            return None

        start, end = result.group().split("-")
        piloti.extend(list(range(int(start), int(end) + 1)))

    return [str(x) for x in piloti]


def sorteggio(
    piloti: list[str], prev_sorteggio: dict[str, int] | None = None, extra_kart: int = 0
):
    piloti_shuffle: list[str] = deepcopy(piloti)
    random.shuffle(piloti_shuffle)

    nuovo_sorteggio: dict[str, int] = {}
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


def define_gui() -> tuple[bool | None, list[str] | None, str | None, int | None]:
    st.set_page_config(page_title="Sorteggio sessione", page_icon="🎲")
    st.title("Sorteggio Sessione")
    st.header("Istruzioni")
    st.text("""Inserire la tipologia di evento, poi inserire i nomi dei piloti, il numero di kart extra e poi clicca su sorteggia.
Il programma effettua il sorteggio considerando i risultati del sorteggio della sessione precedente.
Ad esempio, se il Pilota 1 in Qualifica ha sorteggiato il kart 5, per il sorteggio della gara il kart 5 viene escluso dal sorteggio del kart per il pilota 1, e viene assegnato ad un altro pilota.

Il numero di extra kart è il numero di kart extra che si vogliono sorteggiare. Ad esempio se la gara è composta da 10 piloti ma si hanno a disposizione 12 kart, inserendo 2 come kart extra, il programma potrà sorteggiare anche i kart 11 e 12.
    """)
    form = st.form("sorteggio")

    tipo_evento: str | None = form.selectbox(
        label="Inserisci la tipologia di evento",
        key="tipo_evento",
        options=TIPO_EVENTO_MAP.keys(),
        index=None,
    )

    piloti_string: str | None = form.text_area(
        label="Inserisci i piloti come intervalli numerici. Se vuoi inserire più intervalli, usa la virgola per separare gli intervalli. (es 1-4,6-8,10-12 genera i piloti 1,2,3,4,6,7,8,10,11,12) ",
        key="pilota",
        value=None,
    )
    piloti_list: list[str] = piloti_string.split("\n") if piloti_string else []

    piloti: list[str] = []
    for pilota_row in piloti_list:
        parsed_row = parse_regex(pilota_row)
        if parsed_row:
            piloti.extend(parsed_row)
        else:
            piloti.append(pilota_row)

    extra_kart: int | None = form.number_input(
        min_value=0,
        max_value=20,
        step=1,
        key="extra_kart",
        label="Seleziona il numero di kart extra che possono essere sorteggiati",
    )

    submit: bool = form.form_submit_button("Sorteggia")

    return submit, piloti, tipo_evento, extra_kart


def main() -> None:
    submit, piloti, tipo_evento, extra_kart = define_gui()

    if not submit:
        return

    sorteggio_sessione_precedente: dict[str, int] = None
    for i in range(TIPO_EVENTO_MAP[tipo_evento]):
        sessione: str = tipo_evento.split("-")[i]
        st.header(f"Sorteggio {sessione}")

        sorteggio_sessione: dict[str, int] = sorteggio(
            piloti, sorteggio_sessione_precedente, extra_kart=extra_kart
        )
        sorteggio_sessione_precedente = deepcopy(sorteggio_sessione)

        sorteggio_sessione = dict(sorted(sorteggio_sessione.items()))
        data = {
            "Pilota": sorteggio_sessione.keys(),
            "Kart": sorteggio_sessione.values(),
        }
        st.dataframe(data, hide_index=True)


main()
