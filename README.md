# Modelling labs

[Course](https://github.com/dKosarevsky/iu7/blob/master/6sem/modeling.md) | [all labs on web page](https://share.streamlit.io/dkosarevsky/modelling_labs/main.py)


## lab 001
[code](https://github.com/dKosarevsky/modelling_labs/tree/master/lab_001)

На экране табличка.

Две большие колонки.
Табличный и алгоритмический способ получения последовательности псевдослучайных чисел.

Табличные(т.е. берëм готовые из таблиц проверенные математиками последовательности псевдослучайных чисел): Одноразрядные, двухразрядные и трëхразрядные.

Алгоритмическим способом генерируем(любым, который выберем): Одноразрядные, двухразрядные и трëхразрядные.

На экран выводим порядка 10-ти чисел из тысячи, которую сгенерируем.

Внизу под каждым столбцом выводим число, которое оценивает случайность данной последовательности.

**Необходимо придумать критерий случайности.**

Если фантазии нет придумать свой собственный критерий - открываем 2-й том Кнута.

Предусмотреть форму, где пользователь может сам задать последовательность чисел - после чего выводится итоговое число с оценкой случайности.

+Отчëт: 
3 страницы.
1. Титул, фио студента и препода, ЛР #1 "Исследование последовательности псевдослучайных чисел" по курсу Моделирование.
2. Задание.
3. Результат.

+текст программы (код) на носителе.

## lab 002
[code](https://github.com/dKosarevsky/modelling_labs/tree/master/lab_002)

Случайные процессы.

* Функция распределения
* Функция плотности

Необходимо построить обе эти функции для:

0. Равномерного распределения (для всех + одно из трёх по списку группы, т.е. каждый должен исследовать обе функции для каждого из двух распределений) и внутри группы делим следующим образом:
2. Пуассоновское распределение (все величины закона, что входит, как он влияет) [необходимо реализовать изменение параметров в диалоге, не в командной строке, например параметр лямбда, мат. ожидание, дисперсия и т.д. (у кого-то сигма), параметрическая настройка закона] + график
3. Нормальное распределение (про величины график и вот это всё аналогично)
4. Эрланговское распределение (про величины график и вот это всё аналогично)

## lab 003
[code](https://github.com/dKosarevsky/modelling_labs/tree/master/lab_003)

Есть система S с количеством состояний от 1 до 10 (N). 
Необходимо задать количество состояний, тут же появляется матрица в которой мы должны указать на пересечении Si с Sj (S-итого с S-житым) интенсивность перехода из состояния в состояние, если она (интенсивность) есть. 
Строки S1, S2, ..., Sn. И столбец точно также пронумерован.
Мы можем переходить из S1 в S1, переход такой возможен.

Необходимо найти предельные вероятности нахождения системы в том или ином состоянии, т.е. при t стремящемся к бесконечности, и время. Если с вероятностями всё просто, то время - это не вероятно. И это даже совсем не пропорционально вероятности. 
Нужно найти время, когда эта система попадает в установившееся состояние.

Лямбду задаёт пользователь (пересечение столбцов и строк матрицы, интенсивность).

Правая часть уравнения нуль, производной здесь нету, установившийся режим, константа.
Решаем уравнение и находим вероятность.

Время не может оказаться равным вероятности!

## lab 004
