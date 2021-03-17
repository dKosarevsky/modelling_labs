import streamlit as st
from lab_001 import pseudo_random_nums
from lab_002 import random_variables

st.set_page_config(initial_sidebar_state="collapsed")
st.sidebar.image('logo.png', width=300)


def header():
    author = """
        ---
        made by [Kosarevsky Dmitry](https://github.com/dKosarevsky) 
        for Modelling [labs](https://github.com/dKosarevsky/modelling_labs)
        in [BMSTU](https://bmstu.ru)
    """
    st.title("МГТУ им. Баумана. Кафедра ИУ7")

    st.write("Преподаватель: Рудаков И.В.")
    st.write("Студент: Косаревский Д.П.")
    st.write("")
    st.write("---")
    st.sidebar.markdown(author)


def main():
    header()
    lab = st.radio(
        "Выберите Лабораторную работу", (
            "1. Исследование последовательности псевдослучайных чисел",
            "2. Исследование случайных величин",
            "3. :construction_worker:",
        ),
        index=1
    )

    if lab[:1] == "1":
        pseudo_random_nums.main()

    elif lab[:1] == "2":
        random_variables.main()

    elif lab[:1] == "3":
        st.write(":construction: Проектирование... :construction:")


if __name__ == "__main__":
    main()
