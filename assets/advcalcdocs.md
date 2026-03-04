# Advanced Calculator — Гайд / Guide

[RU](#ru) | [EN](#en)

---

## RU

### Установка

Установи плагин через каталог плагинов exteraGram. Если установлена старая версия — удали её перед установкой новой.

---

### Команды

| Команда | Описание |
|---|---|
| `.calc [выражение]` | Вычислить математическое выражение |
| `.calcbmi [вес] [рост]` | Рассчитать индекс массы тела |

Префиксы команд можно изменить в настройках плагина.

---

### Настройки

Открыть настройки: нажми **···** в чате → **Настройки калькулятора**.

| Параметр | Описание | По умолчанию |
|---|---|---|
| Отправлять только ответ | Отправляет `4` вместо `` `2+2` = *4* `` | Выкл |
| Точность (знаков) | Количество значимых цифр в результате (1–1000) | 15 |
| Команда калькулятора | Префикс для `.calc` | `.calc` |
| Команда BMI | Префикс для `.calcbmi` | `.calcbmi` |

---

### Базовая арифметика

```
.calc 2+2
.calc 100-37
.calc 6*7
.calc 144/12
.calc 2^10
.calc 10%3
```

Поддерживаются операторы `+`, `-`, `*`, `/`, `^` (степень), `%` (остаток).  
Также работают символы `×` и `÷`.

---

### Дроби и специальные символы

Поддерживаются Unicode-дроби и надстрочные степени:

```
.calc ½ + ⅓
.calc ¾ * 8
.calc 2³
.calc 5²+3²
.calc √144
```

---

### Конвертация валют

Формат: `[сумма] [откуда] to [куда]`

```
.calc 100 usd to eur
.calc 5000 rub to usd
.calc 1 btc to usd
```

Курсы загружаются с exchangerate-api.com в реальном времени.

---

### Математические константы

Доступны все константы mpmath:

```
.calc pi
.calc e
.calc phi
.calc euler
.calc catalan
.calc inf
```

| Константа | Значение |
|---|---|
| `pi` | 3.14159... |
| `e` | 2.71828... |
| `phi` | 1.61803... (золотое сечение) |
| `euler` | 0.57721... (постоянная Эйлера) |
| `catalan` | 0.91597... |

---

### Тригонометрия

Аргументы в радианах. Для градусов используй `degrees()` / `radians()`.

```
.calc sin(pi/6)
.calc cos(0)
.calc tan(pi/4)
.calc asin(0.5)
.calc acos(1)
.calc atan(1)
.calc atan2(1, 1)
```

Доступны также: `sec`, `csc`, `cot`, `asec`, `acsc`, `acot`.

---

### Гиперболические функции

```
.calc sinh(1)
.calc cosh(1)
.calc tanh(1)
.calc asinh(1)
.calc acosh(2)
.calc atanh(0.5)
```

---

### Степени и логарифмы

```
.calc sqrt(144)
.calc cbrt(27)
.calc exp(1)
.calc log(e)
.calc log(100, 10)
.calc log10(1000)
.calc log2(1024)
.calc power(2, 10)
.calc root(8, 3)
```

---

### Факториалы и гамма-функция

```
.calc factorial(10)
.calc gamma(5)
.calc gamma(0.5)
.calc loggamma(10)
.calc rgamma(3)
.calc digamma(1)
```

> `gamma(n)` = `(n-1)!` для целых n. `gamma(0.5)` = √π.

---

### Специальные функции

```
.calc zeta(2)
.calc zeta(3)
.calc erf(1)
.calc erfc(1)
.calc besselj(0, 1)
.calc bessely(0, 1)
.calc besseli(0, 1)
.calc besselk(0, 1)
.calc airyai(1)
.calc airybi(1)
```

| Функция | Описание |
|---|---|
| `zeta(s)` | Дзета-функция Римана |
| `erf(x)` | Функция ошибок |
| `erfc(x)` | Дополнение функции ошибок |
| `besselj(n,x)` | Функция Бесселя первого рода |
| `bessely(n,x)` | Функция Бесселя второго рода |
| `airyai(x)` | Функция Эйри Ai |

---

### Комбинаторика и теория чисел

```
.calc fib(50)
.calc fib(100)
.calc binomial(10, 3)
.calc prime(10)
.calc primepi(100)
.calc bernoulli(4)
```

| Функция | Описание |
|---|---|
| `fib(n)` | n-е число Фибоначчи |
| `binomial(n, k)` | Биномиальный коэффициент C(n,k) |
| `prime(n)` | n-е простое число |
| `primepi(x)` | Количество простых ≤ x |

---

### Комплексные числа

mpmath поддерживает комплексную арифметику. Мнимая единица: `j`.

```
.calc sqrt(-1)
.calc exp(j*pi)
.calc (1+2j)*(3+4j)
.calc abs(3+4j)
.calc arg(1+1j)
```

> `exp(j*pi)` → `-1+0.0i` — формула Эйлера.

---

### Произвольная точность

В настройках плагина можно задать количество значимых цифр (1–1000).

```
# при precision=50:
.calc pi        → 3.1415926535897932384626433832795028841971693993751
.calc sqrt(2)   → 1.4142135623730950488016887242096980785696718753769
```

---

### BMI

Формат: `.calcbmi [вес_кг] [рост_см]`

```
.calcbmi 70 175
.calcbmi 90 180
```

Результат включает значение BMI, вес и рост.

| BMI | Категория |
|---|---|
| < 18.5 | Недостаток веса |
| 18.5 – 24.9 | Норма |
| 25 – 29.9 | Избыточный вес |
| ≥ 30 | Ожирение |

---

### Обработка ошибок

- Если выражение невалидно — показывается bulletin с описанием ошибки и кнопкой **RECOVER**, которая копирует выражение в буфер обмена.
- Неверный синтаксис `.calcbmi` — bulletin с подсказкой.
- Нечисловые значения веса/роста — отдельный bulletin.

---
---

## EN

### Installation

Install the plugin via the exteraGram plugin catalog. If you have an older version installed — uninstall it before installing the new one.

---

### Commands

| Command | Description |
|---|---|
| `.calc [expression]` | Evaluate a math expression |
| `.calcbmi [weight] [height]` | Calculate Body Mass Index |

Command prefixes can be changed in plugin settings.

---

### Settings

Open settings: tap **···** in chat → **Calculator Settings**.

| Option | Description | Default |
|---|---|---|
| Send only answer | Sends `4` instead of `` `2+2` = *4* `` | Off |
| Precision (digits) | Number of significant digits in result (1–1000) | 15 |
| Calculator command | Prefix for `.calc` | `.calc` |
| BMI command | Prefix for `.calcbmi` | `.calcbmi` |

---

### Basic Arithmetic

```
.calc 2+2
.calc 100-37
.calc 6*7
.calc 144/12
.calc 2^10
.calc 10%3
```

Supported operators: `+`, `-`, `*`, `/`, `^` (power), `%` (modulo).  
Symbols `×` and `÷` also work.

---

### Fractions and Special Symbols

Unicode fractions and superscript exponents are supported:

```
.calc ½ + ⅓
.calc ¾ * 8
.calc 2³
.calc 5²+3²
.calc √144
```

---

### Currency Conversion

Format: `[amount] [from] to [to]`

```
.calc 100 usd to eur
.calc 5000 rub to usd
.calc 1 btc to usd
```

Rates are fetched in real time from exchangerate-api.com.

---

### Mathematical Constants

All mpmath constants are available:

```
.calc pi
.calc e
.calc phi
.calc euler
.calc catalan
.calc inf
```

| Constant | Value |
|---|---|
| `pi` | 3.14159... |
| `e` | 2.71828... |
| `phi` | 1.61803... (golden ratio) |
| `euler` | 0.57721... (Euler–Mascheroni) |
| `catalan` | 0.91597... |

---

### Trigonometry

Arguments in radians. Use `degrees()` / `radians()` for conversion.

```
.calc sin(pi/6)
.calc cos(0)
.calc tan(pi/4)
.calc asin(0.5)
.calc acos(1)
.calc atan(1)
.calc atan2(1, 1)
```

Also available: `sec`, `csc`, `cot`, `asec`, `acsc`, `acot`.

---

### Hyperbolic Functions

```
.calc sinh(1)
.calc cosh(1)
.calc tanh(1)
.calc asinh(1)
.calc acosh(2)
.calc atanh(0.5)
```

---

### Powers and Logarithms

```
.calc sqrt(144)
.calc cbrt(27)
.calc exp(1)
.calc log(e)
.calc log(100, 10)
.calc log10(1000)
.calc log2(1024)
.calc power(2, 10)
.calc root(8, 3)
```

---

### Factorials and Gamma Function

```
.calc factorial(10)
.calc gamma(5)
.calc gamma(0.5)
.calc loggamma(10)
.calc rgamma(3)
.calc digamma(1)
```

> `gamma(n)` = `(n-1)!` for integer n. `gamma(0.5)` = √π.

---

### Special Functions

```
.calc zeta(2)
.calc zeta(3)
.calc erf(1)
.calc erfc(1)
.calc besselj(0, 1)
.calc bessely(0, 1)
.calc besseli(0, 1)
.calc besselk(0, 1)
.calc airyai(1)
.calc airybi(1)
```

| Function | Description |
|---|---|
| `zeta(s)` | Riemann zeta function |
| `erf(x)` | Error function |
| `erfc(x)` | Complementary error function |
| `besselj(n,x)` | Bessel function of the first kind |
| `bessely(n,x)` | Bessel function of the second kind |
| `airyai(x)` | Airy function Ai |

---

### Combinatorics and Number Theory

```
.calc fib(50)
.calc fib(100)
.calc binomial(10, 3)
.calc prime(10)
.calc primepi(100)
.calc bernoulli(4)
```

| Function | Description |
|---|---|
| `fib(n)` | n-th Fibonacci number |
| `binomial(n, k)` | Binomial coefficient C(n,k) |
| `prime(n)` | n-th prime number |
| `primepi(x)` | Count of primes ≤ x |

---

### Complex Numbers

mpmath supports complex arithmetic. Imaginary unit: `j`.

```
.calc sqrt(-1)
.calc exp(j*pi)
.calc (1+2j)*(3+4j)
.calc abs(3+4j)
.calc arg(1+1j)
```

> `exp(j*pi)` → `-1+0.0i` — Euler's formula.

---

### Arbitrary Precision

Set the number of significant digits (1–1000) in plugin settings.

```
# with precision=50:
.calc pi        → 3.1415926535897932384626433832795028841971693993751
.calc sqrt(2)   → 1.4142135623730950488016887242096980785696718753769
```

---

### BMI

Format: `.calcbmi [weight_kg] [height_cm]`

```
.calcbmi 70 175
.calcbmi 90 180
```

Result includes BMI value, weight, and height.

| BMI | Category |
|---|---|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25 – 29.9 | Overweight |
| ≥ 30 | Obese |

---

### Error Handling

- Invalid expression — bulletin with error description and a **RECOVER** button that copies the expression to clipboard.
- Wrong `.calcbmi` syntax — bulletin with usage hint.
- Non-integer weight/height values — separate bulletin.
