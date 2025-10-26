import streamlit as st
import random
from copy import deepcopy

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
    form = st.form("sorteggio")

    tipo_evento: str | None = form.selectbox(
        label="Inserisci la tipologia di evento",
        key="tipo_evento",
        options=TIPO_EVENTO_MAP.keys(),
        index=None,
    )

    piloti: str | None = form.text_area(
        label="Inserisci i nomi dei piloti. I piloti devono essere separati da una nuova riga",
        key="pilota",
        value=None,
    )
    piloti: list[str] | None = piloti.split("\n") if piloti else None

    extra_kart: int | None = form.number_input(
        min_value=0,
        max_value=10,
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

        # lunghezza_nome_max: int = max([len(x) for x in piloti])
        for pilota, kart in dict(sorted(sorteggio_sessione.items())).items():
            st.write(f"Pilota: **{pilota}** - Kart: **{kart}**")


main()
