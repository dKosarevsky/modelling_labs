import streamlit as st
from lab_001 import pseudo_random_nums
from lab_002 import random_variables
from lab_003 import kolmogorov
from lab_004 import imit
from lab_005 import smo

st.set_page_config(initial_sidebar_state="collapsed")
st.sidebar.image('logo.png', width=300)


def header():
    author = """
        made by [Kosarevsky Dmitry](https://github.com/dKosarevsky) 
        for Modelling [labs](https://github.com/dKosarevsky/modelling_labs)
        in [BMSTU](https://bmstu.ru)
    """
    st.title("МГТУ им. Баумана. Кафедра ИУ7")
    st.write("Преподаватель: Рудаков И.В.")
    st.write("Студент: Косаревский Д.П.")
    st.sidebar.markdown(author)


def main():
    header()
    lab = st.sidebar.radio(
        "Выберите Лабораторную работу", (
            "1. Исследование последовательности псевдослучайных чисел",
            "2. Исследование случайных величин",
            "3. Предельные вероятности состояний. Уравнения Колмогорова",
            "4. Программная имитация i-го прибора",
            "5. Многоканальная СМО",
        ),
        index=4
    )

    if lab[:1] == "1":
        pseudo_random_nums.main()

    elif lab[:1] == "2":
        random_variables.main()

    elif lab[:1] == "3":
        kolmogorov.main()

    elif lab[:1] == "4":
        imit.main()

    elif lab[:1] == "5":
        smo.main()


if __name__ == "__main__":
    main()
