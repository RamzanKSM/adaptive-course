# Диагностический тест по Python — MVP

## Общие правила

- Тест предназначен прежде всего для студентов, которые никогда не программировали или никогда не работали с Python.
- Все вопросы имеют 4 варианта ответа и один правильный ответ.
- Внутри каждого блока вопросы идут от самых простых к более сложным.
- Диагностика не засчитывается как практическое освоение навыка. Она только определяет, с какого места начинать обучение.
- Неправильные ответы не уменьшают уровень навыка.
- На этапе диагностики LLM-подсказки отключены.
- Коды навыков Python начинаются с `PY_`, чтобы не пересекаться с навыками Java.

---

# Блок 0. Абсолютная база: как читать простой код

### 1. Что выведет программа?

```python
print("Привет")
```

A. `print`  
B. `Привет`  
C. `"Привет"`  
D. Ничего

**Ответ:** B  
**Навык:** `PY_BASIC_CODE_READING`

### 2. Что выведет программа?

```python
x = 5
print(x)
```

A. `x`  
B. `int`  
C. `5`  
D. Ничего

**Ответ:** C  
**Навык:** `PY_VARIABLE_BASIC`

### 3. Что выведет программа?

```python
x = 5
x = 8
print(x)
```

A. `8`  
B. `5`  
C. `13`  
D. Ошибка

**Ответ:** A  
**Навык:** `PY_ASSIGNMENT`

### 4. Что выведет программа?

```python
print(2 + 3 * 4)
```

A. `20`  
B. `24`  
C. `9`  
D. `14`

**Ответ:** D  
**Навык:** `PY_ARITHMETIC_BASIC`

### 5. Что выведет программа?

```python
print("A")
print("B")
print("C")
```

A. `A B C` в одну строку  
B. `C`, затем `B`, затем `A` — каждое на новой строке  
C. `A`, затем `B`, затем `C` — каждое на новой строке  
D. Только `C`

**Ответ:** C  
**Навык:** `PY_EXECUTION_FLOW_BASIC`

### 6. Что выведет программа?

```python
name = "Аня"
print("Привет, " + name)
```

A. `Привет, name`  
B. `Привет, Аня`  
C. `"Привет, " + name`  
D. Ошибка

**Ответ:** B  
**Навык:** `PY_VARIABLE_BASIC`

### 7. Что выведет программа?

```python
count = 1
count = count + 1
print(count)
```

A. `1`  
B. `count + 1`  
C. `2`  
D. Ошибка

**Ответ:** C  
**Навык:** `PY_ASSIGNMENT`

---

# Блок 1. Типы данных и простые операции

### 8. Какой тип у значения `3.5`?

A. `int`  
B. `float`  
C. `str`  
D. `bool`

**Ответ:** B  
**Навык:** `PY_NUMBER_TYPES`

### 9. Что выведет программа?

```python
print(7 / 2)
```

A. `3`  
B. `4`  
C. `3.5`  
D. Ошибка

**Ответ:** C  
**Навык:** `PY_NUMBER_TYPES`

### 10. Что выведет программа?

```python
print("5" + "3")
```

A. `53`  
B. `8`  
C. `5 3`  
D. Ошибка

**Ответ:** A  
**Навык:** `PY_STRING_BASIC`

### 11. Что выведет программа?

```python
print(int("7") + 1)
```

A. `71`  
B. `7 + 1`  
C. Ошибка  
D. `8`

**Ответ:** D  
**Навык:** `PY_TYPE_CONVERSION`

### 12. Что произойдёт при запуске?

```python
print("Год: " + 2025)
```

A. Выведется `Год: 2025`  
B. Выведется `Год: `  
C. Возникнет ошибка `TypeError`: строку нельзя сложить с числом  
D. Выведется `2025`

**Ответ:** C  
**Навык:** `PY_TYPE_CONVERSION`

### 13. Что выведет программа?

```python
print(7 // 2)
```

A. `3.5`  
B. `3`  
C. `4`  
D. `1`

**Ответ:** B  
**Навык:** `PY_INTEGER_DIVISION`

### 14. Что выведет программа?

```python
print(7 % 3)
```

A. `2`  
B. `0`  
C. `2.33`  
D. `1`

**Ответ:** D  
**Навык:** `PY_INTEGER_DIVISION`

### 15. Что выведет программа?

```python
x = 10
x += 5
print(x)
```

A. `10`  
B. `15`  
C. `5`  
D. `105`

**Ответ:** B  
**Навык:** `PY_ASSIGNMENT_OPERATORS`

### 16. Что выведет программа?

```python
name = "Оля"
age = 20
print(f"{name}: {age}")
```

A. `{name}: {age}`  
B. `f"Оля: 20"`  
C. `Оля: 20`  
D. Ошибка

**Ответ:** C  
**Навык:** `PY_FSTRINGS`

---

# Блок 2. Условия

### 17. Что выведет программа?

```python
x = 7
if x > 5:
    print("больше")
else:
    print("не больше")
```

A. `больше`  
B. `не больше`  
C. `больше` и `не больше`  
D. Ничего

**Ответ:** A  
**Навык:** `PY_IF_ELSE_BASIC`

### 18. Что выведет программа?

```python
x = 3
if x > 5:
    print("A")
print("B")
```

A. `A`  
B. `A`, затем `B`  
C. Ничего  
D. `B`

**Ответ:** D  
**Навык:** `PY_IF_ELSE_BASIC`

### 19. Что выведет программа?

```python
x = 4
print(x == 4)
```

A. `4`  
B. `True`  
C. `x == 4`  
D. Ошибка

**Ответ:** B  
**Навык:** `PY_COMPARISON_OPERATORS`

### 20. Что не так в этой строке?

```python
if x = 5:
    print("пять")
```

A. Всё правильно  
B. Нужны круглые скобки вокруг условия  
C. Нужно `===` вместо `=`  
D. Для сравнения нужно `==`, а `=` — это присваивание, поэтому будет `SyntaxError`

**Ответ:** D  
**Навык:** `PY_COMPARISON_OPERATORS`

### 21. Что выведет программа?

```python
age = 20
has_ticket = False
print(age >= 18 and has_ticket)
```

A. `True`  
B. `False`  
C. `20`  
D. Ошибка

**Ответ:** B  
**Навык:** `PY_LOGICAL_AND`

### 22. Что выведет программа?

```python
is_weekend = False
is_holiday = True
if is_weekend or is_holiday:
    print("отдыхаем")
else:
    print("работаем")
```

A. `работаем`  
B. `отдыхаем` и `работаем`  
C. `отдыхаем`  
D. Ничего

**Ответ:** C  
**Навык:** `PY_LOGICAL_OR`

### 23. Что выведет программа?

```python
score = 75
if score >= 90:
    print("отлично")
elif score >= 70:
    print("хорошо")
else:
    print("плохо")
```

A. `отлично`  
B. `хорошо`  
C. `плохо`  
D. `хорошо` и `плохо`

**Ответ:** B  
**Навык:** `PY_ELIF`

### 24. Что выведет программа?

```python
items = []
if items:
    print("есть")
else:
    print("пусто")
```

A. `пусто`  
B. `есть`  
C. `[]`  
D. Ошибка

**Ответ:** A  
**Навык:** `PY_TRUTHINESS`

---

# Блок 3. Циклы

### 25. Что выведет программа?

```python
for i in range(3):
    print(i)
```

A. `1`, `2`, `3` — каждое на новой строке  
B. `0`, `1`, `2`, `3` — каждое на новой строке  
C. `0`, `1`, `2` — каждое на новой строке  
D. `3`

**Ответ:** C  
**Навык:** `PY_FOR_RANGE`

### 26. Какие числа выведет программа?

```python
for i in range(1, 6, 2):
    print(i)
```

A. `1, 2, 3, 4, 5`  
B. `1, 3, 5`  
C. `2, 4, 6`  
D. `1, 3, 5, 7`

**Ответ:** B  
**Навык:** `PY_FOR_RANGE`

### 27. Что выведет программа?

```python
total = 0
for n in range(1, 4):
    total += n
print(total)
```

A. `3`  
B. `10`  
C. `0`  
D. `6`

**Ответ:** D  
**Навык:** `PY_ACCUMULATOR_PATTERN`

### 28. Что выведет программа?

```python
n = 1
while n < 10:
    n = n * 2
print(n)
```

A. `8`  
B. `16`  
C. `10`  
D. `1`

**Ответ:** B  
**Навык:** `PY_WHILE_LOOP_BASIC`

### 29. Какие числа выведет программа?

```python
for i in range(10):
    if i == 3:
        break
    print(i)
```

A. `0, 1, 2`  
B. `0, 1, 2, 3`  
C. `3`  
D. Все числа от `0` до `9`

**Ответ:** A  
**Навык:** `PY_LOOP_CONTROL`

### 30. Какие числа выведет программа?

```python
for i in range(5):
    if i % 2 == 0:
        continue
    print(i)
```

A. `0, 2, 4`  
B. `1, 3, 5`  
C. Ничего  
D. `1, 3`

**Ответ:** D  
**Навык:** `PY_LOOP_CONTROL`

### 31. Что произойдёт при запуске?

```python
i = 1
while i < 5:
    print(i)
```

A. Программа выведет `1 2 3 4`  
B. Программа выведет `1` один раз  
C. Цикл будет выполняться бесконечно  
D. Возникнет ошибка

**Ответ:** C  
**Навык:** `PY_LOOP_TERMINATION`

---

# Блок 4. Списки, строки и функции

### 32. Что выведет программа?

```python
nums = [10, 20, 30]
print(nums[0])
```

A. `10`  
B. `20`  
C. `30`  
D. Ошибка

**Ответ:** A  
**Навык:** `PY_LIST_INDEXING`

### 33. Что выведет программа?

```python
nums = [10, 20, 30]
print(nums[-1])
```

A. `10`  
B. Ошибка  
C. `30`  
D. `20`

**Ответ:** C  
**Навык:** `PY_LIST_INDEXING`

### 34. Что выведет программа?

```python
nums = [10, 20, 30]
print(len(nums))
```

A. `2`  
B. `3`  
C. `30`  
D. `60`

**Ответ:** B  
**Навык:** `PY_LIST_BASIC`

### 35. Что выведет программа?

```python
nums = [2, 4, 6]
total = 0
for n in nums:
    total += n
print(total)
```

A. `6`  
B. `10`  
C. `246`  
D. `12`

**Ответ:** D  
**Навык:** `PY_LIST_ITERATION`

### 36. Что выведет программа?

```python
word = "Python"
print(word[1:4])
```

A. `Pyt`  
B. `yth`  
C. `ytho`  
D. `Pyth`

**Ответ:** B  
**Навык:** `PY_STRING_SLICING`

### 37. Что выведет программа?

```python
text = "  да  "
print(text.strip() + "!")
```

A. `  да  !`  
B. `да  !`  
C. `да!`  
D. Ошибка

**Ответ:** C  
**Навык:** `PY_STRING_METHODS`

### 38. Что выведет программа?

```python
def add(a, b):
    return a + b

print(add(2, 3))
```

A. `5`  
B. `23`  
C. `2`  
D. Ничего

**Ответ:** A  
**Навык:** `PY_FUNCTION_BASIC`

### 39. Что выведет программа?

```python
def greet(name):
    print("Привет, " + name)

result = greet("Оля")
print(result)
```

A. `Привет, Оля` два раза  
B. Только `None`  
C. Ошибка  
D. `Привет, Оля`, затем `None`

**Ответ:** D  
**Навык:** `PY_FUNCTION_RETURN`

### 40. Что такое `a` и `b` в этом объявлении?

```python
def add(a, b):
    return a + b
```

A. Названия функций  
B. Параметры функции  
C. Типы данных  
D. Переменные цикла

**Ответ:** B  
**Навык:** `PY_FUNCTION_PARAMETERS`

---

# Блок 5. Классы и объекты

### 41. Что описывает этот код?

```python
class Student:
    def __init__(self, name):
        self.name = name
```

A. Функцию, которая сразу печатает имя  
B. Класс — шаблон, по которому создаются объекты-студенты  
C. Список студентов  
D. Модуль Python

**Ответ:** B  
**Навык:** `PY_CLASS_BASIC`

### 42. Что выведет программа?

```python
class Student:
    def __init__(self, name):
        self.name = name

s = Student("Аня")
print(s.name)
```

A. `Student`  
B. `name`  
C. `Аня`  
D. Ошибка

**Ответ:** C  
**Навык:** `PY_OBJECT_CREATION`

### 43. Когда вызывается метод `__init__`?

A. При импорте файла  
B. При каждом вызове `print`  
C. Только если вызвать его вручную  
D. Автоматически при создании нового объекта класса

**Ответ:** D  
**Навык:** `PY_INIT_METHOD`

### 44. Что выведет программа?

```python
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

c = Counter()
c.increment()
c.increment()
print(c.value)
```

A. `0`  
B. `1`  
C. `2`  
D. Ошибка

**Ответ:** C  
**Навык:** `PY_SELF_BASIC`

### 45. Что по соглашению означает подчёркивание в имени атрибута `self._balance`?

A. Атрибут нельзя прочитать вообще  
B. Это внутренняя деталь класса, снаружи её не трогают напрямую  
C. Это константа  
D. Атрибут общий для всех объектов

**Ответ:** B  
**Навык:** `PY_ENCAPSULATION_BASIC`

### 46. Что выведет программа?

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

t = Temperature(100)
print(t.fahrenheit)
```

A. `100`  
B. `212.0`  
C. Ошибка: метод нужно вызывать со скобками  
D. `fahrenheit`

**Ответ:** B  
**Навык:** `PY_PROPERTY_BASIC`

### 47. Что выведет программа?

```python
class Dog:
    legs = 4

a = Dog()
b = Dog()
print(a.legs + b.legs)
```

A. `8`  
B. `4`  
C. `44`  
D. Ошибка

**Ответ:** A  
**Навык:** `PY_CLASS_ATTRIBUTES`

---

# Блок 6. Наследование и полиморфизм

### 48. Что выведет программа?

```python
class Animal:
    def sound(self):
        return "..."

class Cat(Animal):
    pass

print(Cat().sound())
```

A. Ошибка: у `Cat` нет метода `sound`  
B. `None`  
C. `...`  
D. `Cat`

**Ответ:** C  
**Навык:** `PY_INHERITANCE_BASIC`

### 49. Что выведет программа?

```python
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):
        return "Гав"

print(Dog().sound())
```

A. `...`  
B. `Гав`  
C. `...Гав`  
D. Ошибка

**Ответ:** B  
**Навык:** `PY_METHOD_OVERRIDE`

### 50. Что выведет программа?

```python
class Animal:
    def sound(self):
        return "..."

class Dog(Animal):
    def sound(self):
        return "Гав"

class Cat(Animal):
    def sound(self):
        return "Мяу"

for animal in [Dog(), Cat()]:
    print(animal.sound())
```

A. `...` два раза  
B. `Гав`, затем `Мяу`  
C. `Гав` два раза  
D. Ошибка

**Ответ:** B  
**Навык:** `PY_POLYMORPHISM_BASIC`

### 51. Что выведет программа?

```python
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, group):
        super().__init__(name)
        self.group = group

s = Student("Аня", "ИТ-1")
print(s.name, s.group)
```

A. `Аня ИТ-1`  
B. `ИТ-1`  
C. Ошибка: у `Student` нет атрибута `name`  
D. `Аня`

**Ответ:** A  
**Навык:** `PY_SUPER_BASIC`

### 52. Какой объект можно передать в эту функцию?

```python
def describe(thing):
    return thing.speak()
```

A. Только объект класса `Animal`  
B. Только строку  
C. Любой объект, у которого есть метод `speak()`  
D. Только список

**Ответ:** C  
**Навык:** `PY_DUCK_TYPING`

---

# Блок 7. Коллекции

### 53. Что выведет программа?

```python
items = [1, 2]
items.append(3)
print(items)
```

A. `[1, 2]`  
B. `[3, 1, 2]`  
C. `3`  
D. `[1, 2, 3]`

**Ответ:** D  
**Навык:** `PY_LIST_OPERATIONS`

### 54. Что произойдёт при запуске?

```python
point = (2, 5)
point[0] = 10
```

A. `point` станет `(10, 5)`  
B. Возникнет `TypeError`: кортеж нельзя изменить  
C. `point` станет `(2, 5, 10)`  
D. Ничего

**Ответ:** B  
**Навык:** `PY_TUPLE_BASIC`

### 55. Что выведет программа?

```python
print(len({1, 2, 2, 3, 3, 3}))
```

A. `6`  
B. `1`  
C. `3`  
D. Ошибка

**Ответ:** C  
**Навык:** `PY_SET_BASIC`

### 56. Что выведет программа?

```python
ages = {"Аня": 20, "Боря": 22}
print(ages["Боря"])
```

A. `Боря`  
B. `22`  
C. `20`  
D. Ошибка

**Ответ:** B  
**Навык:** `PY_DICT_BASIC`

### 57. Нужно хранить уникальные логины и быстро проверять, есть ли среди них нужный. Что подходит лучше всего?

A. `set`  
B. `list`  
C. `tuple`  
D. Одна длинная строка `str`

**Ответ:** A  
**Навык:** `PY_COLLECTION_SELECTION`

### 58. Что выведет программа?

```python
print([n * n for n in range(4)])
```

A. `[1, 4, 9, 16]`  
B. `[0, 1, 2, 3]`  
C. `[0, 1, 4, 9]`  
D. `14`

**Ответ:** C  
**Навык:** `PY_COMPREHENSIONS`

---

# Блок 8. Исключения

### 59. Что выведет программа?

```python
try:
    print(10 / 0)
except ZeroDivisionError:
    print("делить на ноль нельзя")
```

A. `0`  
B. `делить на ноль нельзя`  
C. Программа завершится с ошибкой  
D. `inf`

**Ответ:** B  
**Навык:** `PY_TRY_EXCEPT_BASIC`

### 60. Что выведет программа?

```python
try:
    n = int("abc")
    print("число")
except ValueError:
    print("не число")
```

A. `число`  
B. `число`, затем `не число`  
C. `abc`  
D. `не число`

**Ответ:** D  
**Навык:** `PY_EXCEPTION_TYPES`

### 61. Что выведет программа?

```python
try:
    print("A")
finally:
    print("B")
```

A. Только `A`  
B. Только `B`  
C. `A`, затем `B`  
D. `B`, затем `A`

**Ответ:** C  
**Навык:** `PY_FINALLY_BASIC`

### 62. Что произойдёт при вызове `check_age(-1)`?

```python
def check_age(age):
    if age < 0:
        raise ValueError("возраст не может быть отрицательным")
    return age
```

A. Функция вернёт `-1`  
B. Функция вернёт `0`  
C. Возникнет `ValueError` с сообщением «возраст не может быть отрицательным»  
D. Ничего не произойдёт

**Ответ:** C  
**Навык:** `PY_RAISE_BASIC`
