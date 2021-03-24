import streamlit as st
import numpy as np
import scipy.stats as sts

import plotly.figure_factory as ff
import plotly.graph_objects as go
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder


def show_tz():
    st.markdown("""
        Есть система S с количеством состояний от 1 до 10 (N). Необходимо задать количество состояний, тут же появляется матрица в которой мы должны указать на пересечении Si с Sj (S-итого с S-житым) интенсивность перехода из состояния в состояние, если она (интенсивность) есть. Строки S1, S2, ..., Sn. И столбец точно также пронумерован. Мы можем переходить из S1 в S1, переход такой возможен.
        
        Необходимо найти предельные вероятности нахождения системы в том или ином состоянии, т.е. при t стремящемся к бесконечности, и время. Если с вероятностями всё просто, то время - это не вероятно. И это даже совсем не пропорционально вероятности. Нужно найти время, когда эта система попадает в установившееся состояние.
        
        Лямбду задаёт пользователь (пересечение столбцов и строк матрицы, интенсивность).
        
        Правая часть уравнения нуль, производной здесь нету, установившийся режим, константа. Решаем уравнение и находим вероятность.
        
        Время не может оказаться равным вероятности!
    """)


def find_time(matrix, n):
    a = np.zeros((n, n))  # матрица для решения СЛАУ
    b = np.zeros(n)  # матрица для результатов

    for i in range(n - 1):
        for j in range(n):
            if i != j:
                a[i][j] += matrix[j][i]
            else:
                a[j][j] -= sum(matrix[j])
    a[-1] = np.ones(n)
    b[-1] = 1  # нормализация матрицы

    try:
        t = np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        t = np.zeros(n)

    for i in range(n):
        st.write(f"t_{i} = {t[i]}")


def main():
    st.header("Моделирование. Лабораторная работа №3")
    st.write("Предельные вероятности состояний. Уравнения Колмогорова")

    if st.checkbox("Показать ТЗ"):
        show_tz()

    c1, c2 = st.beta_columns(2)
    N = c1.slider("Количество состояний системы (N):", min_value=1, max_value=10, value=5)

    df = pd.DataFrame(np.zeros((N, N)))
    AgGrid(df)

    find_time(df.to_numpy(), N)


if __name__ == "__main__":
    main()
