import streamlit as st
import numpy.random as nr


class UniformGenerator:
    def __init__(self, a, b):
        if not 0 <= a <= b:
            raise ValueError('Параметры должны удовлетворять условию 0 <= a <= b')
        self._a = a
        self._b = b

    def generate(self):
        return nr.uniform(self._a, self._b)


class NormalGenerator:
    def __init__(self, m, d):
        self._m = m
        self._d = d

    def generate(self):
        return nr.normal(self._m, self._d)


class Model:
    def __init__(self, dt, req_count, reenter_prob):
        self.dt = dt
        self.req_count = req_count
        self.reenter_prob = reenter_prob

        self.queue = 0
        self.queue_len_max = 0
        self.reenter = 0

    def check_len_max(self):
        if self.queue > self.queue_len_max:
            self.queue_len_max = self.queue

    def add_to_queue(self):
        self.queue += 1
        self.check_len_max()

    def rem_from_queue(self, is_reenter=True):
        if self.queue == 0:
            return 0

        self.queue -= 1

        if is_reenter and nr.sample() < self.reenter_prob:
            self.reenter += 1
            self.add_to_queue()

        return 1

    def event_based_modelling(self, a, b, m, d):
        req_generator = UniformGenerator(a, b)
        req_proccessor = NormalGenerator(m, d)

        req_done_count = 0
        t_generation = req_generator.generate()
        t_proccessor = t_generation + req_proccessor.generate()

        while req_done_count < self.req_count:
            if t_generation <= t_proccessor:
                self.add_to_queue()
                t_generation += req_generator.generate()
                continue
            if t_generation >= t_proccessor:
                req_done_count += self.rem_from_queue(True)
                t_proccessor += req_proccessor.generate()

        return self.queue_len_max, self.req_count, self.reenter

    def time_based_modelling(self, a, b, m, d):

        req_generator = UniformGenerator(a, b)
        req_proccessor = NormalGenerator(m, d)

        req_done_count = 0
        t_generation = req_generator.generate()
        t_proccessor = t_generation + req_proccessor.generate()

        t_curr = 0
        while req_done_count < self.req_count:
            if t_generation <= t_curr:
                self.add_to_queue()
                t_generation += req_generator.generate()
            if t_curr >= t_proccessor:
                if self.queue > 0:
                    req_done_count += self.rem_from_queue(True)
                    t_proccessor += req_proccessor.generate()
                else:
                    t_proccessor = t_generation + req_proccessor.generate()

            t_curr += self.dt

        return self.queue_len_max, self.req_count, self.reenter


def show_tz():
    st.markdown("""
        У нас есть генератор (или источник сообщений), есть память, и есть обслуживающий аппарат (ОА). 
        Генератор выдаёт сообщения по равномерному закону распределённого в интервале a+-b (от a до b). 
        ОА выбирает сообщения из памяти, и вот здесь преподаватель пишет наш закон, тот который мы писали во 2-й ЛР 
        (по вариантам, нормальный, экспоненциальный, пуассоновский и т.д.). Все эти законы параметрически настраиваются.

        1. Необходимо определить минимальную длину очереди (или объём памяти), при котором сообщения не теряются 
        (т.е. не возникает такая ситуация, когда сообщение идёт в ОА, а он занят). 
        Реализовывать это нужно двумя способами (принципами): дельта t  и событийно. Посмотреть есть ли разница.
        
        2. А дальше наступает ужас-ужас. Преподаватель умудряется передать выданные сообщения из ОА в процентном 
        соотношении снова на вход очереди. Он задаёт, например, что половина сообщение снова поступает на ОА, 
        или 0,7 или 0,1 и снова смотрит, что произойдёт с очередью.
        
        Определить оптимальную длину очереди, т.е. ту длину, при которой ни одно сообщение необработанным не исчезает. 
        Т.е. нет отказа.
        
        Т.е. нужно сделать прогу, которая сначала выдаст минимальное t, потом подаём % и она снова выдаёт минимальное t.
        И хорошо если ещё и статистики сюда прикрутим и можно будет посмотреть по каждому устройству как оно нагружено, 
        т.е. вроде своего мини-GPSS создадим.
        """)


def main():
    st.header("Моделирование. Лабораторная работа №4")
    st.write("Программная имитация i-го прибора")

    if st.checkbox("Показать ТЗ"):
        show_tz()
    st.markdown("---")

    distribution = st.radio(
        "Выберите тип распределения ОА", (
            "1. Нормальное",
            "2. Пуассоновское",
            "3. Эрланговское",
        )
    )

    st.write("Параметры генератора. Равномерное распределение")
    c1, c2 = st.beta_columns(2)
    a = c1.number_input("Задайте начало интервала (a):", min_value=1., max_value=10000., value=1.)
    b = c2.number_input("Задайте начало интервала (b):", min_value=1., max_value=10000., value=10.)

    if distribution[:1] == "1":
        st.write(f"Параметры обслуживающего аппарата. {distribution[3:]} распределение")  # TODO fix not only naming
        c2, c3 = st.beta_columns(2)
        m = c2.number_input("Задайте значение (μ):", min_value=1., max_value=10000., value=5.)
        d = c3.number_input("Задайте значение (D):", min_value=1., max_value=10000., value=5.)

    st.write("Дополнительные параметры")
    c4, c5, c6 = st.beta_columns(3)
    requests_count = c4.number_input("Количество заявок:", min_value=1, max_value=10000, value=1000)
    reenter_probability = c5.number_input("Вер-сть повторной обработки:", min_value=0., max_value=1., value=.5)
    delta_t = c6.number_input("Задайте значение (Δt):", min_value=0., max_value=1., value=.1)
    st.markdown("---")

    modelT = Model(delta_t, requests_count, reenter_probability)
    results1 = modelT.time_based_modelling(a, b, m, d)

    modelEvent = Model(delta_t, requests_count, reenter_probability)
    results2 = modelEvent.event_based_modelling(a, b, m, d)

    queue_len_max1, req_done_count1, reenter1 = results1
    st.write("Метод Δt")
    st.write(f"Количество повторно обработанных заявок: {reenter1}")
    st.write(f"Максимальная длина очереди: {queue_len_max1}")
    st.markdown("---")

    queue_len_max2, req_done_count2, reenter2 = results2
    st.write("Событийный метод")
    st.write(f"Количество повторно обработанных заявок: {reenter2}")
    st.write(f"Максимальная длина очереди: {queue_len_max2}")
    st.markdown("---")


if __name__ == "__main__":
    main()
