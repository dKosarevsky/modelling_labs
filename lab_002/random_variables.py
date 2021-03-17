import streamlit as st
import numpy as np
import scipy.stats as sts

import plotly.figure_factory as ff
import plotly.graph_objects as go

np.random.seed(42)
RNG = np.random.default_rng()


def header():
    author = """
        ---
        made by [Kosarevsky Dmitry](https://github.com/dKosarevsky) 
        for Modelling [lab#2](https://github.com/dKosarevsky/modelling_lab_002)
        in [BMSTU](https://bmstu.ru)
    """
    st.title("МГТУ им. Баумана. Кафедра ИУ7")
    st.header("Моделирование. Лабораторная работа №2")
    st.write("Исследование случайных величин")
    st.write("Преподаватель: Рудаков И.В.")
    st.write("Студент: Косаревский Д.П.")
    st.write("")
    st.write("---")
    st.sidebar.markdown(author)


def show_tz():
    st.markdown("""
        Вариант 7.

        * Функция распределения
        * Функция плотности
        
        Необходимо построить обе эти функции для:
        
        1. Равномерного распределения
        2. Пуассоновского распределения
        
        Важно учесть все величины закона, что входит, как он влияет. Необходимо реализовать изменение параметров, 
        например параметр лямбда, мат. ожидание, дисперсия и т.д., параметрическая настройка закона, графики.
    """)


def plot_distribution(random_sample, bins):
    fig = go.Figure(data=[go.Histogram(x=random_sample, nbinsx=bins)])
    fig.update_layout(title_text="Гистограмма")
    st.write(fig)

    fig = ff.create_distplot([random_sample], [""], bin_size=.2, show_hist=False)
    fig.update_layout(title_text="Плотность")
    st.write(fig)

    fig = go.Figure(go.Histogram2dContour(
        x=random_sample,
        y=random_sample
    ))
    fig.update_layout(title_text="Контуры плотности")
    st.write(fig)


def main():
    header()

    if st.checkbox("Показать ТЗ"):
        show_tz()

    distribution = st.radio(
        "Выберите тип распределения", (
            "1. Равномерное",
            "2. Пуассоновское",
            "3. Нормальное",
            "4. Эрланговское",
        )
    )
    st.markdown("---")

    if distribution[:1] == "1":
        st.write("Равномерное распределение")

        c1, c2, c3, c4 = st.beta_columns(4)
        lower_boundary = c1.number_input("Нижняя граница:", value=0.0)
        upper_boundary = c2.number_input("Верхняя граница:", min_value=0.1, value=1.0)
        size = c3.number_input("Размер выборки:", min_value=2, value=1000)
        bins = c4.number_input("Размер корзины:", min_value=2, value=50)

        uniform_rv = sts.uniform(lower_boundary, upper_boundary - lower_boundary)
        x = np.linspace(lower_boundary - 1, upper_boundary + 1, size)

        cdf = uniform_rv.cdf(x)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=cdf,
            mode='lines',
        ))
        fig.update_layout(title_text="Распределение вероятностей")
        st.write(fig)

        pdf = uniform_rv.pdf(x)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=pdf,
            mode='lines',
        ))
        fig.update_layout(title_text="Плотность вероятностей")
        st.write(fig)

        random_uniform = RNG.uniform(low=lower_boundary, high=upper_boundary, size=size)
        plot_distribution(random_uniform, bins)

        st.markdown("""
        **Равномерное распределение** описывает событие, в котором все возможные исходы равновероятны.
        Ни один исход не имеет большей или меньшей вероятности, чем любой другой возможный исход.
        **Равномерное распределение может быть дискретным или непрерывным**.
        """)

    elif distribution[:1] == "2":
        st.write("Распределение Пуассона")

        c1, c2, c3 = st.beta_columns(3)
        exp_interval = c1.number_input("Мат. ожидание (λ):", min_value=0.1, value=3.0)
        size = c2.number_input("Размер выборки:", min_value=2, value=10000)
        bins = c3.number_input("Размер корзины:", min_value=2, value=30)

        poisson_rv = sts.poisson(exp_interval)
        x = np.linspace(0, 30, 31)

        cdf = poisson_rv.cdf(x)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=cdf,
            mode='lines',
        ))
        fig.update_layout(title_text="Распределение вероятностей")
        st.write(fig)

        pmf = poisson_rv.pmf(x)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=pmf,
            mode='lines',
        ))
        fig.update_layout(title_text="Плотность вероятностей")
        st.write(fig)

        random_poisson = RNG.poisson(exp_interval, size)
        plot_distribution(random_poisson, bins)

        st.markdown("""
        **Пуассоновская** случайная величина обычно используется для моделирования того, 
        сколько раз событие произошло за интервал времени. Например, количество пользователей, посещенных веб-сайтом 
        за интервал, можно рассматривать как процесс Пуассона. Распределение Пуассона описывается скоростью (μ), 
        с которой происходят события. Событие может произойти 0, 1, 2,… раз в интервале. Среднее количество событий 
        в интервале обозначено λ (лямбда). Лямбда - это частота событий, также называемая параметром скорости. 
        Вероятность наблюдения k событий в интервале определяется уравнением:
        $P(k) = e^-λ * λ^k/k!$
        
        Отметим, что нормальное распределение является предельным случаем распределения Пуассона с параметром λ → ∞. 
        Кроме того, если время между случайными событиями следует экспоненциальному распределению со скоростью λ, 
        то общее количество событий в период времени длиной t следует распределению Пуассона с параметром λt.
        """)

    elif distribution[:1] == "3":
        st.write("Нормальное распределение")

        c1, c2, c3, c4 = st.beta_columns(4)
        mu = c1.number_input("Мат. ожидание (μ):", min_value=0.0, value=0.0)
        sigma = c2.number_input("Среднеквадратичное отклонение (σ):", min_value=0.1, value=0.1)
        size = c3.number_input("Размер выборки:", min_value=2, value=1000)
        bins = c4.number_input("Размер корзины:", min_value=2, value=30)

        random_normal = RNG.normal(mu, sigma, size)
        plot_distribution(random_normal, bins)

    elif distribution[:1] == "4":
        st.write("Эрланговское распределение")

        c1, c2, c3, c4 = st.beta_columns(4)
        shape = c1.number_input("Shape (k):", min_value=0.1, value=2.0)
        scale = c2.number_input("Scale (λ):", min_value=0.1, value=2.0)
        size = c3.number_input("Размер выборки:", min_value=2, value=1000)
        bins = c4.number_input("Размер корзины:", min_value=2, value=30)

        random_gamma = RNG.gamma(shape, scale, size)
        plot_distribution(random_gamma, bins)


if __name__ == "__main__":
    main()
