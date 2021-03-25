import streamlit as st
import numpy as np
import pandas as pd
#import quantecon as qe

import plotly.graph_objects as go
import matplotlib.pyplot as plt

from st_aggrid import AgGrid


def show_tz():
    st.markdown("""
        Есть система S с количеством состояний от 1 до 10 (N). Необходимо задать количество состояний, тут же появляется матрица в которой мы должны указать на пересечении Si с Sj (S-итого с S-житым) интенсивность перехода из состояния в состояние, если она (интенсивность) есть. Строки S1, S2, ..., Sn. И столбец точно также пронумерован. Мы можем переходить из S1 в S1, переход такой возможен.
        
        Необходимо найти предельные вероятности нахождения системы в том или ином состоянии, т.е. при t стремящемся к бесконечности, и время. Если с вероятностями всё просто, то время - это не вероятность. И это даже совсем не пропорционально вероятности. Нужно найти время, когда эта система попадает в установившееся состояние.
        
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
        p = np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        p = np.zeros(n)

    for i in range(n):
        pr = round(p[i], 2)
        perc = round(pr * 100, 2)
        st.write(f"Вероятность p_{i} = {pr}.")
        st.write(f"В предельном режиме система в среднем {perc}% времени будет находиться в состоянии S_{i}")
        st.write("---")

    # # α = β = 0.1
    # # n = 10000
    # # p = β / (α + β)
    # #
    # # P = ((1 - α, α),  # Careful: P and p are distinct
    # #      (β, 1 - β))
    # # P = np.array(P)
    # # mc = MarkovChain(P)
    # mc = qe.MarkovChain(matrix)
    # fig, ax = plt.subplots(figsize=(9, 6))
    # ax.set_ylim(-0.25, 0.25)
    # ax.grid()
    # ax.hlines(0, 0, n, lw=2, alpha=0.6)  # Horizonal line at zero
    #
    # for x0, col in ((0, 'blue'), (1, 'green')):
    #     # Generate time series for worker that starts at x0
    #     X = mc.simulate(n, init=x0)
    #     # Compute fraction of time spent unemployed, for each n
    #     X_bar = (X == 0).cumsum() / (1 + np.arange(n, dtype=float))
    #     # Plot
    #     ax.fill_between(range(n), np.zeros(n), X_bar - p, color=col, alpha=0.1)
    #     ax.plot(X_bar - p, color=col, label=f'$X_0 = \, {x0} $')
    #     # Overlay in black--make lines clearer
    #     ax.plot(X_bar - p, 'k-', alpha=0.6)
    #
    # ax.legend(loc='upper right')
    # st.pyplot(fig)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=a,
        # x=np.arange(n),
        # x=matrix,
        y=p,
        mode='lines',
    ))
    fig.update_layout(
        title_text="? Какой-то полезный график",
        xaxis_title='Состояния (а нужно Время !!)',
        yaxis_title='Вероятность',
        showlegend=False
    )
    st.write(fig)


@st.cache()
def get_data(n, vals):
    arr_0 = np.zeros((n, n)).reshape(-1, n)
    arr_1 = np.ones((n, n)).reshape(-1, n)
    cols = [f"S_{i}" for i in range(0, n)]
    if vals == 0:
        df = pd.DataFrame(arr_0, columns=cols)
    elif vals == 1:
        df = pd.DataFrame(arr_1, columns=cols)
    else:
        df = pd.DataFrame(np.random.randint(0, 10, size=n*n).reshape(-1, n), columns=cols)
    return df


def main():
    st.header("Моделирование. Лабораторная работа №3")
    st.write("Предельные вероятности состояний. Уравнения Колмогорова")

    if st.checkbox("Показать ТЗ"):
        show_tz()

    c1, c2 = st.beta_columns(2)
    N = c1.slider("Задайте количество состояний системы (N):", min_value=1, max_value=10, value=5)
    values = c2.selectbox("Заполнить? (единицами, случайно):", (0, 1, "случайными значениями"))

    df = get_data(N, values)
    st.subheader("Введите значения интенсивности переходов (λ):")
    grid_return = AgGrid(df, editable=True, reload_data=False)

    arr = grid_return["data"].to_numpy()
    find_time(arr, N)


if __name__ == "__main__":
    main()
