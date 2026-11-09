
import streamlit as st


def render_lesson(
    text: dict,
    language: str,
    topic: str,
) -> None:

    st.markdown(f"### 📚 {text['current_lesson']}")

    if topic == "Linear Equations":
        render_linear_equations(text, language)
    elif topic == "Binary Search":
        render_binary_search(text, language)
    elif topic == "Linear Search":
        render_linear_search(text, language)
    elif topic == "Big-O Notation":
      render_big_o(text, language)
    elif topic == "Sorting":
       render_sorting(text, language)
    elif topic == "Functions":
      render_functions(text, language)
    elif topic == "Algebra":
      render_algebra(text, language)
    elif topic == "Arrays":
      render_arrays(text, language)
    elif topic == "Stack":
      render_stack(text, language)
    elif topic == "Queue":
      render_queue(text, language)
       
       
       
    else:
        if language == "English":
            st.info(
                f"The lesson for {topic} is being prepared."
            )
        else:
            st.info(
                f"يجري إعداد الدرس الخاص بموضوع {topic}."
            )


def render_binary_search(text, language):

    st.markdown("## Binary Search" if language == "English"
                else "## البحث الثنائي")

    if language == "English":

        st.markdown("""
### 1. Introduction

Binary Search is an efficient searching algorithm
used to find a target value in a **sorted array**.

Instead of checking every element one by one,
it repeatedly divides the search interval into two halves.

The algorithm eliminates half of the remaining elements
after each comparison.

### 2. Learning Objectives

After completing this lesson, you should be able to:

- Explain how Binary Search works.
- Identify why sorted data is required.
- Apply Binary Search step by step.
- Understand its time complexity.
- Distinguish Binary Search from Linear Search.

### 3. Prerequisites

Before studying Binary Search, you should understand:

- Arrays and indexing.
- Comparison operators.
- The concept of sorted data.
- Basic algorithm steps.

### 4. How Does Binary Search Work?

Binary Search uses three important positions:

- `low`: the first index in the search interval.
- `high`: the last index in the search interval.
- `mid`: the middle index.

The algorithm compares the target with the middle element.

There are three possible cases:

1. If target equals the middle element, the search succeeds.
2. If target is smaller, continue searching the left half.
3. If target is greater, continue searching the right half.

### 5. Worked Example

Consider this sorted array:

`[2, 5, 8, 12, 16, 23, 38]`

Our target is `16`.

**Step 1**

- low = 0
- high = 6
- mid = (0 + 6) // 2 = 3
- array[3] = 12

Since 16 is greater than 12, search the right half.

**Step 2**

- low = 4
- high = 6
- mid = (4 + 6) // 2 = 5
- array[5] = 23

Since 16 is smaller than 23, search the left half.

**Step 3**

- low = 4
- high = 4
- mid = 4
- array[4] = 16

The target is found at index 4.

### 6. Pseudocode

```text
BinarySearch(array, target):

    low = 0
    high = length(array) - 1

    while low <= high:

        mid = (low + high) // 2

        if array[mid] == target:
            return mid

        else if target < array[mid]:
            high = mid - 1

        else:
            low = mid + 1

    return -1
```

### 7. Time Complexity

| Case | Complexity |
|---|---|
| Best Case | O(1) |
| Average Case | O(log n) |
| Worst Case | O(log n) |

Binary Search is efficient because it removes
approximately half of the remaining search space
after each iteration.

### 8. Common Mistakes

- Applying Binary Search to unsorted data.
- Forgetting to update `low` or `high`.
- Using `low < high` instead of `low <= high`
  when the final single element must also be checked.
- Calculating the middle index incorrectly.

### 9. Practice Exercise

Given the sorted array:

`[3, 7, 11, 15, 19, 23, 27, 31]`

Find the target value `23`.

Answer these questions:

1. What are the initial values of low and high?
2. What is the first middle index?
3. Which half will be searched next?
4. At which index is the target found?

### 10. Lesson Summary

Binary Search finds an element by repeatedly
dividing a sorted search interval in half.

Its worst-case time complexity is O(log n).

**Remember:** Binary Search requires sorted data.
""")

    else:

        st.markdown("""
### 1. مقدمة

البحث الثنائي (Binary Search) خوارزمية فعّالة
تُستخدم للعثور على عنصر داخل مصفوفة مرتبة.

بدلاً من فحص العناصر واحداً تلو الآخر،
تقوم الخوارزمية بتقسيم نطاق البحث إلى نصفين
في كل خطوة.

وبذلك تستبعد نصف العناصر المتبقية تقريباً
بعد كل مقارنة.

### 2. أهداف التعلم

بعد دراسة هذا الدرس، ستكون قادراً على:

- شرح آلية عمل البحث الثنائي.
- معرفة سبب ضرورة ترتيب البيانات.
- تطبيق الخوارزمية خطوة بخطوة.
- فهم التعقيد الزمني.
- التمييز بين البحث الثنائي والبحث الخطي.

### 3. المتطلبات السابقة

قبل دراسة البحث الثنائي، ينبغي فهم:

- المصفوفات والفهرسة (Arrays and Indexing).
- معاملات المقارنة.
- مفهوم البيانات المرتبة.
- الخطوات الأساسية للخوارزميات.

### 4. كيف يعمل البحث الثنائي؟

تعتمد الخوارزمية على ثلاثة مؤشرات:

- `low`: أول فهرس في نطاق البحث.
- `high`: آخر فهرس في نطاق البحث.
- `mid`: الفهرس الأوسط.

نقارن العنصر الأوسط بالقيمة المطلوبة.

هناك ثلاث حالات:

1. إذا كانت القيمة المطلوبة مساوية للعنصر الأوسط، فقد وجدنا العنصر.
2. إذا كانت أصغر منه، نبحث في النصف الأيسر.
3. إذا كانت أكبر منه، نبحث في النصف الأيمن.

### 5. مثال محلول خطوة بخطوة

لدينا المصفوفة المرتبة:

`[2, 5, 8, 12, 16, 23, 38]`

نريد البحث عن العدد `16`.

**الخطوة الأولى**

- low = 0
- high = 6
- mid = (0 + 6) // 2 = 3
- array[3] = 12

بما أن 16 أكبر من 12، ننتقل إلى النصف الأيمن.

**الخطوة الثانية**

- low = 4
- high = 6
- mid = (4 + 6) // 2 = 5
- array[5] = 23

بما أن 16 أصغر من 23، ننتقل إلى النصف الأيسر.

**الخطوة الثالثة**

- low = 4
- high = 4
- mid = 4
- array[4] = 16

تم العثور على العنصر عند الفهرس 4.

### 6. الخوارزمية شبه البرمجية

```text
BinarySearch(array, target):

    low = 0
    high = length(array) - 1

    while low <= high:

        mid = (low + high) // 2

        if array[mid] == target:
            return mid

        else if target < array[mid]:
            high = mid - 1

        else:
            low = mid + 1

    return -1
```

### 7. التعقيد الزمني

| الحالة | التعقيد |
|---|---|
| أفضل حالة | O(1) |
| متوسط الحالة | O(log n) |
| أسوأ حالة | O(log n) |

تتميز الخوارزمية بالكفاءة لأنها تستبعد
نصف نطاق البحث تقريباً بعد كل خطوة.

### 8. الأخطاء الشائعة

- تطبيق البحث الثنائي على بيانات غير مرتبة.
- نسيان تحديث `low` أو `high`.
- استخدام `low < high` بدلاً من `low <= high`
  عندما نحتاج إلى فحص العنصر الأخير.
- حساب الفهرس الأوسط بطريقة خاطئة.

### 9. تمرين تطبيقي

لديك المصفوفة المرتبة:

`[3, 7, 11, 15, 19, 23, 27, 31]`

ابحث عن العدد `23`.

أجب عن الأسئلة التالية:

1. ما القيم الابتدائية لـ low وhigh؟
2. ما الفهرس الأوسط في الخطوة الأولى؟
3. أي نصف سنبحث فيه بعد المقارنة؟
4. عند أي فهرس نجد العدد المطلوب؟

### 10. ملخص الدرس

البحث الثنائي خوارزمية تبحث عن عنصر عن طريق
تقسيم نطاق البحث المرتب إلى نصفين بشكل متكرر.

التعقيد الزمني في أسوأ حالة هو O(log n).

**تذكر:** يجب أن تكون البيانات مرتبة قبل استخدام
البحث الثنائي.
""")


def render_linear_equations(text, language):

    st.markdown(
        f"## {topic_title(language, 'Linear Equations')}"
    )

    if language == "English":

        st.markdown("""
### 1. Introduction

A linear equation is an equation in which
the highest power of the variable is one.

The goal is to isolate the unknown variable
while maintaining equality on both sides.

### 2. Learning Objectives

- Understand linear equations.
- Identify the two sides of an equation.
- Apply inverse operations.
- Solve equations step by step.

### 3. Worked Example

Solve:

`2x + 3 = 11`

Step 1: Subtract 3 from both sides.

`2x = 11 - 3`

`2x = 8`

Step 2: Divide both sides by 2.

`x = 8 / 2`

`x = 4`

### 4. Check Your Answer

Substitute x = 4 into the original equation:

`2(4) + 3 = 11`

`8 + 3 = 11`

`11 = 11`

Therefore, x = 4 is correct.

### 5. Practice

Solve:

`3x + 5 = 20`

### 6. Common Mistakes

- Performing an operation on only one side.
- Making sign errors.
- Forgetting to check the answer.
""")

    else:

        st.markdown("""
### 1. مقدمة

المعادلة الخطية هي معادلة يكون فيها أعلى أس
للمتغير مساوياً للواحد.

الهدف هو عزل المتغير المجهول مع الحفاظ
على تساوي طرفي المعادلة.

### 2. أهداف التعلم

- فهم المعادلات الخطية.
- تحديد طرفي المعادلة.
- استخدام العمليات العكسية.
- حل المعادلات خطوة بخطوة.

### 3. مثال محلول

حل المعادلة:

`2x + 3 = 11`

الخطوة الأولى: نطرح 3 من الطرفين.

`2x = 11 - 3`

`2x = 8`

الخطوة الثانية: نقسم الطرفين على 2.

`x = 8 / 2`

`x = 4`

### 4. التحقق من الإجابة

نعوّض عن x بالقيمة 4 في المعادلة الأصلية:

`2(4) + 3 = 11`

`8 + 3 = 11`

`11 = 11`

إذن الإجابة x = 4 صحيحة.

### 5. تمرين تطبيقي

حل المعادلة:

`3x + 5 = 20`

### 6. أخطاء شائعة

- إجراء العملية على طرف واحد فقط.
- الوقوع في أخطاء الإشارات.
- نسيان التحقق من الإجابة.
""")


def topic_title(language, topic):

    if language == "Arabic" and topic == "Linear Equations":
        return "المعادلات الخطية"

    return topic

def render_linear_search(text, language):

    st.markdown(
        "## Linear Search"
        if language == "English"
        else "## البحث الخطي"
    )

    if language == "English":

        st.markdown("""
### 1. Introduction

Linear Search is a simple searching algorithm
that checks elements one by one until the target
is found or the end of the collection is reached.

Unlike Binary Search, Linear Search does not
require the data to be sorted.

### 2. Learning Objectives

After completing this lesson, you should be able to:

- Explain how Linear Search works.
- Apply Linear Search step by step.
- Write its pseudocode.
- Analyze its time complexity.
- Compare Linear Search with Binary Search.

### 3. How Does Linear Search Work?

The algorithm starts from the first element.

It compares each element with the target:

1. If the element matches the target, return its index.
2. Otherwise, move to the next element.
3. If the target is not found, return -1.

### 4. Worked Example

Consider this array:

`[10, 25, 7, 40, 15, 30]`

We want to find the target value `15`.

| Step | Element | Comparison |
|---|---:|---|
| 1 | 10 | Not equal |
| 2 | 25 | Not equal |
| 3 | 7 | Not equal |
| 4 | 40 | Not equal |
| 5 | 15 | Found! |

The target is found at index `4`.

Notice that indexing starts from zero.

### 5. Pseudocode

```text
LinearSearch(array, target):

    for i = 0 to length(array) - 1:

        if array[i] == target:
            return i

    return -1
```

### 6. Time Complexity

| Case | Complexity |
|---|---|
| Best Case | O(1) |
| Average Case | O(n) |
| Worst Case | O(n) |

Best case occurs when the target is the first element.

Worst case occurs when the target is the last element
or does not exist in the array.

### 7. Common Mistakes

- Forgetting that array indexing starts at zero.
- Stopping before checking the last element.
- Returning the element value instead of its index.
- Assuming the array must be sorted.

### 8. Practice Exercise

Given this array:

`[4, 9, 2, 18, 7, 13]`

Search for the value `7`.

Answer these questions:

1. Which element is checked first?
2. How many comparisons are required?
3. At which index is the target found?
4. What does the algorithm return if the target is absent?

### 9. Lesson Summary

Linear Search checks elements sequentially.

It works with both sorted and unsorted data.

Its worst-case time complexity is O(n).
""")

    else:

        st.markdown("""
### 1. مقدمة

البحث الخطي (Linear Search) هو خوارزمية بحث بسيطة
تقوم بفحص العناصر واحداً تلو الآخر حتى تجد العنصر
المطلوب أو تصل إلى نهاية مجموعة البيانات.

على عكس البحث الثنائي، لا يشترط البحث الخطي
أن تكون البيانات مرتبة.

### 2. أهداف التعلم

بعد دراسة هذا الدرس، ستكون قادراً على:

- شرح آلية عمل البحث الخطي.
- تطبيق البحث الخطي خطوة بخطوة.
- كتابة الخوارزمية شبه البرمجية.
- تحليل التعقيد الزمني.
- المقارنة بين البحث الخطي والبحث الثنائي.

### 3. كيف يعمل البحث الخطي؟

تبدأ الخوارزمية من العنصر الأول.

ثم تقارن كل عنصر بالقيمة المطلوبة:

1. إذا كان العنصر يساوي القيمة المطلوبة، تُرجع فهرسه.
2. إذا لم يكن كذلك، تنتقل إلى العنصر التالي.
3. إذا لم تجد العنصر، تُرجع -1.

### 4. مثال محلول

لدينا المصفوفة:

`[10, 25, 7, 40, 15, 30]`

نريد البحث عن العدد `15`.

| الخطوة | العنصر | نتيجة المقارنة |
|---|---:|---|
| 1 | 10 | غير متساوٍ |
| 2 | 25 | غير متساوٍ |
| 3 | 7 | غير متساوٍ |
| 4 | 40 | غير متساوٍ |
| 5 | 15 | تم العثور عليه! |

تم العثور على العنصر عند الفهرس `4`.

لاحظ أن الفهرسة تبدأ من الصفر.

### 5. الخوارزمية شبه البرمجية

```text
LinearSearch(array, target):

    for i = 0 to length(array) - 1:

        if array[i] == target:
            return i

    return -1
```

### 6. التعقيد الزمني

| الحالة | التعقيد |
|---|---|
| أفضل حالة | O(1) |
| متوسط الحالة | O(n) |
| أسوأ حالة | O(n) |

تحدث أفضل حالة عندما يكون العنصر المطلوب
هو العنصر الأول.

أما أسوأ حالة فتحدث عندما يكون العنصر المطلوب
في النهاية أو عندما لا يكون موجوداً في المصفوفة.

### 7. الأخطاء الشائعة

- نسيان أن فهرسة المصفوفة تبدأ من الصفر.
- التوقف قبل فحص العنصر الأخير.
- إرجاع قيمة العنصر بدلاً من فهرسه.
- الاعتقاد بأن المصفوفة يجب أن تكون مرتبة.

### 8. تمرين تطبيقي

لديك المصفوفة:

`[4, 9, 2, 18, 7, 13]`

ابحث عن العدد `7`.

أجب عن الأسئلة التالية:

1. ما أول عنصر يتم فحصه؟
2. كم عدد المقارنات المطلوبة؟
3. عند أي فهرس يوجد العنصر المطلوب؟
4. ماذا تُرجع الخوارزمية إذا لم يكن العنصر موجوداً؟

### 9. ملخص الدرس

البحث الخطي يفحص العناصر بالتتابع.

يمكن استخدامه مع البيانات المرتبة وغير المرتبة.

التعقيد الزمني في أسوأ حالة هو O(n).
""")

def render_big_o(text, language):

    st.markdown(
        "## Big-O Notation"
        if language == "English"
        else "## ترميز Big-O"
    )

    if language == "English":

        st.markdown("""
### 1. Introduction

Big-O Notation is a mathematical way to describe
how an algorithm's running time or memory usage
grows as the input size increases.

It helps us compare algorithms independently
of computer speed or programming language.

### 2. Learning Objectives

After completing this lesson, you should be able to:

- Explain Big-O Notation.
- Distinguish time complexity from space complexity.
- Recognize common complexity classes.
- Analyze simple loops.
- Compare algorithm efficiency.

### 3. Time Complexity and Space Complexity

**Time Complexity**

Describes how the number of operations grows
as the input size increases.

**Space Complexity**

Describes how the additional memory required
by an algorithm grows with input size.

### 4. Common Big-O Classes

| Complexity | Name | Example |
|---|---|---|
| O(1) | Constant | Accessing an array element |
| O(log n) | Logarithmic | Binary Search |
| O(n) | Linear | Linear Search |
| O(n log n) | Linearithmic | Merge Sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Some recursive algorithms |

### 5. Understanding Each Complexity

**O(1) – Constant Time**

```python
def get_first(arr):
    return arr[0]
```

The operation takes a constant amount of time,
regardless of the array size.

**O(log n) – Logarithmic Time**

Binary Search divides the search interval
into two halves after each comparison.

**O(n) – Linear Time**

```python
def print_items(arr):
    for item in arr:
        print(item)
```

If the array contains n elements,
the loop executes n times.

**O(n²) – Quadratic Time**

```python
def print_pairs(arr):
    for i in arr:
        for j in arr:
            print(i, j)
```

For n elements, the nested loops execute n × n times.

### 6. Comparing Growth Rates

Consider an input size of n = 100.

| Complexity | Approximate Operations |
|---|---:|
| O(1) | 1 |
| O(log₂ n) | 7 |
| O(n) | 100 |
| O(n log₂ n) | 664 |
| O(n²) | 10,000 |

These are simplified operation counts,
not exact execution times.

### 7. Rules for Analyzing Big-O

**Rule 1: Ignore constant factors**

O(2n) becomes O(n).

**Rule 2: Keep the dominant term**

O(n² + n + 5) becomes O(n²).

**Rule 3: Sequential operations**

O(n) + O(n) = O(n).

**Rule 4: Nested loops**

O(n) × O(n) = O(n²).

### 8. Common Mistakes

- Thinking Big-O gives exact execution time.
- Confusing O(n) with O(log n).
- Keeping unnecessary constant factors.
- Ignoring nested loops.
- Assuming every algorithm has O(n) complexity.

### 9. Practice Exercise

Determine the time complexity:

```python
for i in range(n):
    print(i)
```

Then analyze:

```python
for i in range(n):
    for j in range(n):
        print(i, j)
```

Questions:

1. What is the complexity of the first code?
2. What is the complexity of the second code?
3. Why does the second code grow faster?

### 10. Lesson Summary

Big-O describes how algorithm resource usage
grows as input size increases.

Common classes include:

O(1), O(log n), O(n), O(n log n), O(n²).

The dominant term determines the simplified
asymptotic complexity.
""")

    else:

        st.markdown("""
### 1. مقدمة

ترميز Big-O هو أسلوب رياضي يُستخدم لوصف
كيفية نمو زمن تنفيذ الخوارزمية أو استهلاكها للذاكرة
عندما يزداد حجم المدخلات.

يساعدنا على مقارنة كفاءة الخوارزميات
بغض النظر عن سرعة الحاسوب أو لغة البرمجة.

### 2. أهداف التعلم

بعد دراسة هذا الدرس، ستكون قادراً على:

- شرح مفهوم Big-O.
- التمييز بين التعقيد الزمني وتعقيد المساحة.
- التعرف على أشهر فئات التعقيد.
- تحليل الحلقات البرمجية البسيطة.
- مقارنة كفاءة الخوارزميات.

### 3. التعقيد الزمني وتعقيد المساحة

**Time Complexity – التعقيد الزمني**

يصف كيفية نمو عدد العمليات التي تنفذها الخوارزمية
عندما يزداد حجم المدخلات.

**Space Complexity – تعقيد المساحة**

يصف كيفية نمو الذاكرة الإضافية التي تحتاجها الخوارزمية
عندما يزداد حجم المدخلات.

### 4. أشهر فئات Big-O

| التعقيد | الاسم | المثال |
|---|---|---|
| O(1) | ثابت | الوصول إلى عنصر في مصفوفة |
| O(log n) | لوغاريتمي | Binary Search |
| O(n) | خطي | Linear Search |
| O(n log n) | خطي لوغاريتمي | Merge Sort |
| O(n²) | تربيعي | الحلقات المتداخلة |
| O(2ⁿ) | أسي | بعض الخوارزميات العودية |

### 5. فهم أنواع التعقيد

**O(1) – زمن ثابت**

```python
def get_first(arr):
    return arr[0]
```

تستغرق العملية زمناً ثابتاً،
بغض النظر عن حجم المصفوفة.

**O(log n) – زمن لوغاريتمي**

البحث الثنائي يقسم نطاق البحث إلى نصفين
بعد كل مقارنة.

**O(n) – زمن خطي**

```python
def print_items(arr):
    for item in arr:
        print(item)
```

إذا كانت المصفوفة تحتوي على n من العناصر،
فإن الحلقة تتكرر n مرة.

**O(n²) – زمن تربيعي**

```python
def print_pairs(arr):
    for i in arr:
        for j in arr:
            print(i, j)
```

إذا كان لدينا n من العناصر،
فإن الحلقتين المتداخلتين تنفذان n × n مرة.

### 6. مقارنة معدلات النمو

لنفترض أن حجم المدخلات n = 100.

| التعقيد | عدد العمليات التقريبي |
|---|---:|
| O(1) | 1 |
| O(log₂ n) | 7 |
| O(n) | 100 |
| O(n log₂ n) | 664 |
| O(n²) | 10,000 |

هذه أعداد تقريبية ومبسطة للعمليات،
وليست أزمنة تنفيذ فعلية.

### 7. قواعد تحليل Big-O

**القاعدة الأولى: تجاهل الثوابت**

O(2n) تصبح O(n).

**القاعدة الثانية: الاحتفاظ بالحد المسيطر**

O(n² + n + 5) تصبح O(n²).

**القاعدة الثالثة: العمليات المتتابعة**

O(n) + O(n) = O(n).

**القاعدة الرابعة: الحلقات المتداخلة**

O(n) × O(n) = O(n²).

### 8. الأخطاء الشائعة

- الاعتقاد بأن Big-O يعطي زمن التنفيذ الفعلي.
- الخلط بين O(n) و O(log n).
- عدم تجاهل الثوابت غير الضرورية.
- تجاهل تأثير الحلقات المتداخلة.
- افتراض أن جميع الخوارزميات تعقيدها O(n).

### 9. تمرين تطبيقي

حدد التعقيد الزمني للكود التالي:

```python
for i in range(n):
    print(i)
```

ثم حلل الكود التالي:

```python
for i in range(n):
    for j in range(n):
        print(i, j)
```

أجب عن الأسئلة:

1. ما تعقيد الكود الأول؟
2. ما تعقيد الكود الثاني؟
3. لماذا ينمو الكود الثاني بسرعة أكبر؟

### 10. ملخص الدرس

يصف Big-O كيفية نمو الموارد التي تستهلكها الخوارزمية
عندما يزداد حجم المدخلات.

من أشهر فئات التعقيد:

O(1)، O(log n)، O(n)، O(n log n)، O(n²).

الحد المسيطر هو الذي يحدد التعقيد التقريبي النهائي.
""")
        
        
        
      
def render_sorting(text: dict, language: str) -> None:

    st.markdown("## Sorting Algorithms")

    if language == "English":

        st.markdown("""
        ### 1. Introduction

        Sorting is the process of arranging data in a specific order,
        usually ascending or descending.

        Example:

        Unsorted: ` [5, 2, 8, 1, 3] `

        Sorted: ` [1, 2, 3, 5, 8] `

        ### 2. Learning Objectives

        By the end of this lesson, you should be able to:

        - Explain the purpose of sorting.
        - Understand Bubble Sort.
        - Understand Selection Sort.
        - Understand Insertion Sort.
        - Compare their time and space complexities.

        ### 3. Bubble Sort

        Bubble Sort repeatedly compares adjacent elements and swaps
        them if they are in the wrong order.

        **Worked Example**

        Initial array: `[5, 3, 8, 2]`

        Pass 1:
        - Compare 5 and 3 → swap: `[3, 5, 8, 2]`
        - Compare 5 and 8 → no swap.
        - Compare 8 and 2 → swap: `[3, 5, 2, 8]`

        Pass 2:
        - Compare 3 and 5 → no swap.
        - Compare 5 and 2 → swap: `[3, 2, 5, 8]`

        Pass 3:
        - Compare 3 and 2 → swap: `[2, 3, 5, 8]`

        **Pseudocode**
        """)

        st.code("""
        for i = 0 to n - 2:
            for j = 0 to n - i - 2:
                if A[j] > A[j + 1]:
                    swap(A[j], A[j + 1])
        """, language="text")

        st.markdown("""
        ### 4. Selection Sort

        Selection Sort repeatedly finds the smallest element in the
        unsorted portion and places it at the beginning.

        **Worked Example**

        Initial array: `[5, 3, 8, 2]`

        - Pass 1: smallest is 2 → `[2, 3, 8, 5]`
        - Pass 2: smallest is 3 → `[2, 3, 8, 5]`
        - Pass 3: smallest is 5 → `[2, 3, 5, 8]`

        **Pseudocode**
        """)

        st.code("""
        for i = 0 to n - 2:
            min_index = i

            for j = i + 1 to n - 1:
                if A[j] < A[min_index]:
                    min_index = j

            swap(A[i], A[min_index])
        """, language="text")

        st.markdown("""
        ### 5. Insertion Sort

        Insertion Sort builds a sorted portion one element at a time.
        Each new element is inserted into its correct position.

        **Worked Example**

        Initial array: `[5, 3, 8, 2]`

        - Insert 3: `[3, 5, 8, 2]`
        - Insert 8: `[3, 5, 8, 2]`
        - Insert 2: `[2, 3, 5, 8]`

        **Pseudocode**
        """)

        st.code("""
        for i = 1 to n - 1:
            key = A[i]
            j = i - 1

            while j >= 0 and A[j] > key:
                A[j + 1] = A[j]
                j = j - 1

            A[j + 1] = key
        """, language="text")

        st.markdown("""
        ### 6. Complexity Comparison

        | Algorithm | Best Case | Average Case | Worst Case | Space |
        |---|---|---|---|---|
        | Bubble Sort (optimized) | O(n) | O(n²) | O(n²) | O(1) |
        | Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
        | Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |

        ### 7. Common Mistakes

        - Confusing comparisons with swaps.
        - Forgetting that array indexes start at zero.
        - Using the wrong loop boundaries.
        - Assuming all sorting algorithms have the same complexity.

        ### 8. Practice Exercise

        Sort the following array in ascending order using
        **Bubble Sort**. Show every pass:

        `[7, 4, 9, 2]`

        ### 9. Summary

        - Bubble Sort swaps adjacent elements.
        - Selection Sort selects the minimum element.
        - Insertion Sort inserts elements into a sorted portion.
        - All three algorithms use O(1) auxiliary space.
        """)

    else:

        st.markdown("""
        ### 1. المقدمة

        الترتيب (Sorting) هو عملية تنظيم البيانات وفق ترتيب محدد،
        عادةً تصاعديًا أو تنازليًا.

        مثال:

        قبل الترتيب: `[5, 2, 8, 1, 3]`

        بعد الترتيب: `[1, 2, 3, 5, 8]`

        ### 2. أهداف التعلم

        بعد دراسة هذا الدرس، ستكون قادرًا على:

        - فهم الهدف من ترتيب البيانات.
        - شرح Bubble Sort.
        - شرح Selection Sort.
        - شرح Insertion Sort.
        - مقارنة التعقيد الزمني والمكاني للخوارزميات.

        ### 3. الترتيب بالفقاعات (Bubble Sort)

        تقارن الخوارزمية كل عنصر بالعنصر المجاور له،
        وتبدّل بينهما إذا كانا في ترتيب خاطئ.

        **مثال محلول**

        المصفوفة الأولية: `[5, 3, 8, 2]`

        المرور الأول:
        - مقارنة 5 و3 ← تبديل: `[3, 5, 8, 2]`
        - مقارنة 5 و8 ← لا تبديل.
        - مقارنة 8 و2 ← تبديل: `[3, 5, 2, 8]`

        المرور الثاني:
        - مقارنة 3 و5 ← لا تبديل.
        - مقارنة 5 و2 ← تبديل: `[3, 2, 5, 8]`

        المرور الثالث:
        - مقارنة 3 و2 ← تبديل: `[2, 3, 5, 8]`

        **الخوارزمية الوصفية (Pseudocode)**
        """)

        st.code("""
        for i = 0 to n - 2:
            for j = 0 to n - i - 2:
                if A[j] > A[j + 1]:
                    swap(A[j], A[j + 1])
        """, language="text")

        st.markdown("""
        ### 4. الترتيب بالاختيار (Selection Sort)

        تبحث الخوارزمية عن أصغر عنصر في الجزء غير المرتب،
        ثم تضعه في بداية ذلك الجزء.

        **مثال محلول**

        المصفوفة الأولية: `[5, 3, 8, 2]`

        - المرور الأول: الأصغر هو 2 ← `[2, 3, 8, 5]`
        - المرور الثاني: الأصغر هو 3 ← `[2, 3, 8, 5]`
        - المرور الثالث: الأصغر هو 5 ← `[2, 3, 5, 8]`

        **الخوارزمية الوصفية**
        """)

        st.code("""
        for i = 0 to n - 2:
            min_index = i

            for j = i + 1 to n - 1:
                if A[j] < A[min_index]:
                    min_index = j

            swap(A[i], A[min_index])
        """, language="text")

        st.markdown("""
        ### 5. الترتيب بالإدراج (Insertion Sort)

        تبني الخوارزمية جزءًا مرتبًا تدريجيًا،
        وتُدخل كل عنصر جديد في موقعه الصحيح.

        **مثال محلول**

        المصفوفة الأولية: `[5, 3, 8, 2]`

        - إدراج 3: `[3, 5, 8, 2]`
        - إدراج 8: `[3, 5, 8, 2]`
        - إدراج 2: `[2, 3, 5, 8]`

        **الخوارزمية الوصفية**
        """)

        st.code("""
        for i = 1 to n - 1:
            key = A[i]
            j = i - 1

            while j >= 0 and A[j] > key:
                A[j + 1] = A[j]
                j = j - 1

            A[j + 1] = key
        """, language="text")

        st.markdown("""
        ### 6. مقارنة التعقيد

        | الخوارزمية | أفضل حالة | متوسط الحالة | أسوأ حالة | المساحة |
        |---|---|---|---|---|
        | Bubble Sort (محسّنة) | O(n) | O(n²) | O(n²) | O(1) |
        | Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
        | Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |

        ### 7. الأخطاء الشائعة

        - الخلط بين عدد المقارنات وعدد عمليات التبديل.
        - نسيان أن فهرسة المصفوفة تبدأ من الصفر.
        - استخدام حدود حلقات غير صحيحة.
        - الاعتقاد بأن جميع خوارزميات الترتيب لها التعقيد نفسه.

        ### 8. تمرين تطبيقي

        رتّب المصفوفة التالية تصاعديًا باستخدام
        **Bubble Sort**، مع توضيح كل مرور:

        `[7, 4, 9, 2]`

        ### 9. الخلاصة

        - Bubble Sort تبدّل العناصر المتجاورة.
        - Selection Sort تختار أصغر عنصر.
        - Insertion Sort تُدرج العناصر في الجزء المرتب.
        - تستخدم الخوارزميات الثلاث مساحة إضافية O(1).
        """)
  
  
def render_functions(text: dict, language: str) -> None:

    st.markdown("## Functions")

    if language == "English":
        st.markdown("""
### 1. Introduction

A function is a reusable block of code that performs a specific task.
It can receive inputs called parameters and return an output.

### 2. Learning Objectives

- Understand functions and their purpose.
- Identify parameters and return values.
- Distinguish between function definition and function call.
- Understand local variables.

### 3. Function Structure

A Python function uses the `def` keyword.

""")
        st.code("""
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8
""", language="python")

        st.markdown("""
### 4. Important Concepts

- **Parameters:** Variables listed in the function definition.
- **Arguments:** Actual values passed to the function.
- **Return:** Sends a result back to the caller.
- **Local Variables:** Variables created inside a function.

### 5. Worked Example

Consider:

`multiply(4, 3)`

1. The function receives 4 and 3.
2. It multiplies both values.
3. It returns 12.

### 6. Function Without Return

""")
        st.code("""
def greet(name):
    print("Hello", name)

greet("Sara")
""", language="python")

        st.markdown("""
### 7. Common Mistakes

- Forgetting parentheses when calling a function.
- Confusing parameters with arguments.
- Forgetting to return a value.
- Using local variables outside their function.

### 8. Practice

Write a function that receives a number and returns its square.

### 9. Summary

Functions improve code reuse, organization, readability, and testing.
""")

    else:
        st.markdown("""
### 1. المقدمة

الدالة (Function) هي كتلة برمجية قابلة لإعادة الاستخدام،
تنفذ مهمة محددة، ويمكنها استقبال مدخلات وإرجاع نتيجة.

### 2. أهداف التعلم

- فهم مفهوم الدوال وأهميتها.
- معرفة المعاملات والقيم المعادة.
- التمييز بين تعريف الدالة واستدعائها.
- فهم المتغيرات المحلية.

### 3. تركيب الدالة

نستخدم الكلمة `def` لتعريف دالة في Python.
""")
        st.code("""
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8
""", language="python")

        st.markdown("""
### 4. المفاهيم الأساسية

- **Parameters:** المعاملات المكتوبة في تعريف الدالة.
- **Arguments:** القيم الفعلية التي نمررها للدالة.
- **Return:** إرجاع النتيجة إلى الجزء الذي استدعى الدالة.
- **Local Variables:** متغيرات تُنشأ داخل الدالة.

### 5. مثال محلول

عند استدعاء:

`multiply(4, 3)`

1. تستقبل الدالة العددين 4 و3.
2. تضرب العددين.
3. تعيد النتيجة 12.

### 6. دالة لا تعيد قيمة
""")
        st.code("""
def greet(name):
    print("Hello", name)

greet("Sara")
""", language="python")

        st.markdown("""
### 7. الأخطاء الشائعة

- نسيان الأقواس عند استدعاء الدالة.
- الخلط بين Parameters وArguments.
- نسيان إرجاع النتيجة.
- استخدام متغير محلي خارج الدالة.

### 8. تمرين

اكتب دالة تستقبل عددًا وتعيد مربعه.

### 9. الخلاصة

تساعد الدوال على إعادة استخدام الكود وتنظيمه
وتحسين قراءته واختباره.
""")


def render_algebra(text: dict, language: str) -> None:

    st.markdown("## Algebra")

    if language == "English":
        st.markdown("""
### 1. Introduction

Algebra is a branch of mathematics that uses symbols and variables
to represent unknown or changing quantities.

### 2. Learning Objectives

- Understand variables and constants.
- Simplify algebraic expressions.
- Evaluate expressions.
- Solve basic equations.

### 3. Variables and Constants

In `3x + 5`:

- x is a variable.
- 3 is its coefficient.
- 5 is a constant.
- 3x is a term.

### 4. Simplifying Expressions

Like terms can be combined.

Example:

`3x + 2x + 4 = 5x + 4`

### 5. Evaluating Expressions

If `x = 2`, evaluate `3x + 5`:

1. Substitute x with 2.
2. Calculate `3(2) + 5`.
3. Result: `11`.

### 6. Solving Equations

Example:

`2x + 4 = 12`

1. Subtract 4 from both sides: `2x = 8`.
2. Divide both sides by 2: `x = 4`.
3. Check: `2(4) + 4 = 12`.

""")
        st.code("""
# Evaluate an algebraic expression
x = 2
result = 3 * x + 5
print(result)  # 11
""", language="python")

        st.markdown("""
### 7. Common Mistakes

- Combining unlike terms.
- Forgetting negative signs.
- Performing different operations on equation sides.
- Incorrectly substituting variable values.

### 8. Practice

1. Simplify: `4x + 3x - 2`.
2. Evaluate `5x + 1` when `x = 3`.
3. Solve: `3x + 6 = 18`.

### 9. Summary

Algebra uses variables, expressions, and equations
to represent and solve mathematical problems.
""")

    else:
        st.markdown("""
### 1. المقدمة

الجبر فرع من الرياضيات يستخدم الرموز والمتغيرات
لتمثيل الكميات المجهولة أو المتغيرة.

### 2. أهداف التعلم

- فهم المتغيرات والثوابت.
- تبسيط العبارات الجبرية.
- حساب قيمة العبارات.
- حل المعادلات الأساسية.

### 3. المتغيرات والثوابت

في العبارة `3x + 5`:

- x متغير.
- 3 معامل المتغير.
- 5 ثابت.
- 3x حد جبري.

### 4. تبسيط العبارات الجبرية

يمكن جمع الحدود المتشابهة.

مثال:

`3x + 2x + 4 = 5x + 4`

### 5. حساب قيمة عبارة جبرية

إذا كان `x = 2`، احسب `3x + 5`:

1. نعوض x بالعدد 2.
2. نحسب `3(2) + 5`.
3. النتيجة: `11`.

### 6. حل المعادلات

مثال:

`2x + 4 = 12`

1. نطرح 4 من الطرفين: `2x = 8`.
2. نقسم الطرفين على 2: `x = 4`.
3. التحقق: `2(4) + 4 = 12`.

""")
        st.code("""
x = 2
result = 3 * x + 5
print(result)  # 11
""", language="python")

        st.markdown("""
### 7. الأخطاء الشائعة

- جمع حدود غير متشابهة.
- نسيان الإشارات السالبة.
- إجراء عمليات مختلفة على طرفي المعادلة.
- التعويض الخاطئ بقيم المتغيرات.

### 8. تمارين تطبيقية

1. بسّط: `4x + 3x - 2`.
2. احسب `5x + 1` عندما `x = 3`.
3. حل: `3x + 6 = 18`.

### 9. الخلاصة

يستخدم الجبر المتغيرات والعبارات والمعادلات
لتمثيل المسائل الرياضية وحلها.
""")


def render_arrays(text: dict, language: str) -> None:

    st.markdown("## Arrays")

    if language == "English":
        st.markdown("""
### 1. Introduction

An array is a data structure that stores multiple elements
under one variable name. Elements are accessed using indexes.

### 2. Learning Objectives

- Understand arrays and indexing.
- Traverse an array.
- Search for an element.
- Understand insertion and deletion.
- Analyze array operation complexity.

### 3. Array Indexing

Consider:

`A = [10, 20, 30, 40, 50]`

| Index | Value |
|---|---|
| 0 | 10 |
| 1 | 20 |
| 2 | 30 |
| 3 | 40 |
| 4 | 50 |

The first index is usually zero.

### 4. Traversal

Traversal means visiting each element.

""")
        st.code("""
A = [10, 20, 30, 40, 50]

for i in range(len(A)):
    print(A[i])
""", language="python")

        st.markdown("""
### 5. Searching

To find 30, inspect elements until the target is found.

- Index 0: 10
- Index 1: 20
- Index 2: 30 → Found!

Linear search takes O(n) time in the worst case.

### 6. Insertion and Deletion

Inserting or deleting an element in the middle of an array
may require shifting other elements.

""")
        st.code("""
A = [10, 20, 30]

# Insert 15 at index 1
A.insert(1, 15)

# Delete the element at index 2
del A[2]

print(A)
""", language="python")

        st.markdown("""
### 7. Complexity

| Operation | Typical Complexity |
|---|---|
| Access by index | O(1) |
| Search (unsorted) | O(n) |
| Traversal | O(n) |
| Insert at beginning | O(n) |
| Delete at beginning | O(n) |
| Append (dynamic array) | O(1) amortized |

### 8. Common Mistakes

- Accessing an invalid index.
- Confusing index with element value.
- Forgetting that indexes start at zero.
- Modifying an array while iterating without care.

### 9. Practice

Given `A = [4, 8, 2, 9, 5]`:

1. What is the element at index 2?
2. Find the index of 9.
3. Insert 7 at index 1.
4. Delete the element at index 3.

### 10. Summary

Arrays organize elements in indexed positions
and support efficient direct access.
""")

    else:
        st.markdown("""
### 1. المقدمة

المصفوفة (Array) هي بنية بيانات تخزن عدة عناصر
تحت اسم متغير واحد، ويمكن الوصول إلى العناصر باستخدام الفهارس.

### 2. أهداف التعلم

- فهم المصفوفات والفهرسة.
- المرور على عناصر المصفوفة.
- البحث عن عنصر.
- فهم الإدراج والحذف.
- تحليل تعقيد عمليات المصفوفة.

### 3. فهرسة المصفوفة

لدينا:

`A = [10, 20, 30, 40, 50]`

| الفهرس | القيمة |
|---|---|
| 0 | 10 |
| 1 | 20 |
| 2 | 30 |
| 3 | 40 |
| 4 | 50 |

يبدأ الفهرس عادةً من الصفر.

### 4. المرور على العناصر (Traversal)

يعني زيارة كل عنصر في المصفوفة.
""")
        st.code("""
A = [10, 20, 30, 40, 50]

for i in range(len(A)):
    print(A[i])
""", language="python")

        st.markdown("""
### 5. البحث (Searching)

للبحث عن 30 نفحص العناصر بالتتابع:

- الفهرس 0: القيمة 10.
- الفهرس 1: القيمة 20.
- الفهرس 2: القيمة 30 ← تم العثور عليها!

البحث الخطي يحتاج في أسوأ حالة إلى O(n).

### 6. الإدراج والحذف

إضافة عنصر أو حذفه من وسط المصفوفة
قد يتطلب تحريك العناصر الأخرى.
""")
        st.code("""
A = [10, 20, 30]

A.insert(1, 15)
del A[2]

print(A)
""", language="python")

        st.markdown("""
### 7. التعقيد

| العملية | التعقيد المعتاد |
|---|---|
| الوصول باستخدام الفهرس | O(1) |
| البحث في مصفوفة غير مرتبة | O(n) |
| المرور على العناصر | O(n) |
| الإدراج في البداية | O(n) |
| الحذف من البداية | O(n) |
| الإضافة في النهاية للمصفوفة الديناميكية | O(1) بالمعدل |

### 8. الأخطاء الشائعة

- الوصول إلى فهرس غير موجود.
- الخلط بين الفهرس وقيمة العنصر.
- نسيان أن الفهرسة تبدأ من الصفر.
- تعديل المصفوفة أثناء المرور عليها دون الانتباه.

### 9. تمرين

لدينا `A = [4, 8, 2, 9, 5]`:

1. ما العنصر عند الفهرس 2؟
2. ما فهرس العنصر 9؟
3. أدرج 7 عند الفهرس 1.
4. احذف العنصر عند الفهرس 3.

### 10. الخلاصة

تنظم المصفوفات العناصر في مواقع مفهرسة
وتسمح بالوصول المباشر والفعال إليها.
""")


def render_stack(text: dict, language: str) -> None:

    st.markdown("## Stack")

    if language == "English":
        st.markdown("""
### 1. Introduction

A Stack is a linear data structure that follows
LIFO: Last In, First Out.

The last element added is the first one removed.

### 2. Learning Objectives

- Understand the LIFO principle.
- Explain Push and Pop.
- Understand Peek and IsEmpty.
- Identify stack applications.
- Analyze stack operation complexity.

### 3. Main Operations

- **Push:** Add an element to the top.
- **Pop:** Remove the top element.
- **Peek:** View the top element without removing it.
- **IsEmpty:** Check whether the stack contains elements.

### 4. Worked Example

Start with an empty stack:

1. Push 10 → `[10]`
2. Push 20 → `[10, 20]`
3. Push 30 → `[10, 20, 30]`
4. Pop → removes 30.
5. The new top is 20.

### 5. Python Implementation
""")
        st.code("""
stack = []

stack.append(10)  # Push
stack.append(20)
stack.append(30)

top = stack[-1]   # Peek
removed = stack.pop()

print(top)
print(removed)
""", language="python")

        st.markdown("""
### 6. Applications

- Function calls and recursion.
- Undo operations.
- Browser history.
- Expression evaluation.
- Parentheses matching.

### 7. Complexity

| Operation | Complexity |
|---|---|
| Push | O(1) amortized |
| Pop | O(1) |
| Peek | O(1) |
| IsEmpty | O(1) |
| Search | O(n) |

### 8. Common Mistakes

- Popping from an empty stack.
- Confusing LIFO with FIFO.
- Removing an element from the wrong end.

### 9. Practice

Perform these operations:

Push 5, Push 10, Push 15, Pop, Push 20.

What is the final stack and its top element?

### 10. Summary

A Stack uses LIFO and supports efficient insertion
and removal at the top.
""")

    else:
        st.markdown("""
### 1. المقدمة

المكدس (Stack) هو بنية بيانات خطية تتبع مبدأ:

LIFO: Last In, First Out

أي أن آخر عنصر يدخل هو أول عنصر يخرج.

### 2. أهداف التعلم

- فهم مبدأ LIFO.
- شرح عمليتي Push وPop.
- فهم Peek وIsEmpty.
- معرفة استخدامات المكدس.
- تحليل تعقيد عملياته.

### 3. العمليات الأساسية

- **Push:** إضافة عنصر إلى أعلى المكدس.
- **Pop:** إزالة العنصر الموجود في الأعلى.
- **Peek:** عرض العنصر العلوي دون إزالته.
- **IsEmpty:** التحقق مما إذا كان المكدس فارغًا.

### 4. مثال محلول

نبدأ بمكدس فارغ:

1. Push 10 ← `[10]`
2. Push 20 ← `[10, 20]`
3. Push 30 ← `[10, 20, 30]`
4. Pop ← إزالة 30.
5. يصبح العنصر العلوي 20.

### 5. تطبيق باستخدام Python
""")
        st.code("""
stack = []

stack.append(10)
stack.append(20)
stack.append(30)

top = stack[-1]
removed = stack.pop()

print(top)
print(removed)
""", language="python")

        st.markdown("""
### 6. استخدامات المكدس

- استدعاء الدوال والاستدعاء الذاتي.
- التراجع عن العمليات (Undo).
- سجل التصفح.
- تقييم التعبيرات الرياضية.
- التحقق من الأقواس.

### 7. التعقيد

| العملية | التعقيد |
|---|---|
| Push | O(1) بالمعدل |
| Pop | O(1) |
| Peek | O(1) |
| IsEmpty | O(1) |
| البحث | O(n) |

### 8. الأخطاء الشائعة

- إزالة عنصر من مكدس فارغ.
- الخلط بين LIFO وFIFO.
- إزالة عنصر من الطرف الخطأ.

### 9. تمرين

نفّذ العمليات التالية:

Push 5, Push 10, Push 15, Pop, Push 20.

ما شكل المكدس النهائي؟ وما العنصر الموجود في الأعلى؟

### 10. الخلاصة

يعتمد Stack على مبدأ LIFO،
ويسمح بإضافة العناصر وإزالتها بكفاءة من الأعلى.
""")


def render_queue(text: dict, language: str) -> None:

    st.markdown("## Queue")

    if language == "English":
        st.markdown("""
### 1. Introduction

A Queue is a linear data structure that follows
FIFO: First In, First Out.

The first element added is the first one removed.

### 2. Learning Objectives

- Understand FIFO.
- Explain Enqueue and Dequeue.
- Understand Front and Rear.
- Identify queue applications.
- Analyze queue operation complexity.

### 3. Main Operations

- **Enqueue:** Add an element to the rear.
- **Dequeue:** Remove an element from the front.
- **Front:** View the first element.
- **Rear:** View the last element.
- **IsEmpty:** Check whether the queue is empty.

### 4. Worked Example

Start with an empty queue:

1. Enqueue 10 → `[10]`
2. Enqueue 20 → `[10, 20]`
3. Enqueue 30 → `[10, 20, 30]`
4. Dequeue → removes 10.
5. The queue becomes `[20, 30]`.

### 5. Python Implementation
""")
        st.code("""
from collections import deque

queue = deque()

queue.append(10)     # Enqueue
queue.append(20)
queue.append(30)

removed = queue.popleft()  # Dequeue

print(removed)
print(queue)
""", language="python")

        st.markdown("""
### 6. Applications

- Printer job scheduling.
- CPU task scheduling.
- Customer service systems.
- Breadth-First Search (BFS).
- Network packet processing.

### 7. Complexity

For a deque implementation:

| Operation | Complexity |
|---|---|
| Enqueue | O(1) |
| Dequeue | O(1) |
| Front | O(1) |
| Rear | O(1) |
| Search | O(n) |

### 8. Common Mistakes

- Confusing FIFO with LIFO.
- Removing an element from the rear.
- Dequeue from an empty queue.
- Using a list with pop(0) for a large queue.

### 9. Practice

Perform:

Enqueue 5, Enqueue 10, Enqueue 15, Dequeue, Enqueue 20.

What is the final queue? Which element is at the front?

### 10. Summary

A Queue follows FIFO and is useful when tasks
must be processed in arrival order.
""")

    else:
        st.markdown("""
### 1. المقدمة

الطابور (Queue) هو بنية بيانات خطية تتبع مبدأ:

FIFO: First In, First Out

أي أن أول عنصر يدخل هو أول عنصر يخرج.

### 2. أهداف التعلم

- فهم مبدأ FIFO.
- شرح عمليتي Enqueue وDequeue.
- فهم Front وRear.
- معرفة استخدامات الطابور.
- تحليل تعقيد عمليات الطابور.

### 3. العمليات الأساسية

- **Enqueue:** إضافة عنصر إلى نهاية الطابور.
- **Dequeue:** إزالة العنصر من مقدمة الطابور.
- **Front:** عرض أول عنصر.
- **Rear:** عرض آخر عنصر.
- **IsEmpty:** التحقق من أن الطابور فارغ.

### 4. مثال محلول

نبدأ بطابور فارغ:

1. Enqueue 10 ← `[10]`
2. Enqueue 20 ← `[10, 20]`
3. Enqueue 30 ← `[10, 20, 30]`
4. Dequeue ← إزالة 10.
5. يصبح الطابور `[20, 30]`.

### 5. تطبيق باستخدام Python
""")
        st.code("""
from collections import deque

queue = deque()

queue.append(10)
queue.append(20)
queue.append(30)

removed = queue.popleft()

print(removed)
print(queue)
""", language="python")

        st.markdown("""
### 6. استخدامات الطابور

- تنظيم مهام الطابعة.
- جدولة مهام المعالج.
- أنظمة خدمة العملاء.
- خوارزمية البحث بالعرض (BFS).
- معالجة حزم الشبكات.

### 7. التعقيد

عند استخدام deque:

| العملية | التعقيد |
|---|---|
| Enqueue | O(1) |
| Dequeue | O(1) |
| Front | O(1) |
| Rear | O(1) |
| البحث | O(n) |

### 8. الأخطاء الشائعة

- الخلط بين FIFO وLIFO.
- إزالة العنصر من نهاية الطابور بدلًا من بدايته.
- تنفيذ Dequeue على طابور فارغ.
- استخدام pop(0) مع قائمة كبيرة دون مراعاة كلفته.

### 9. تمرين

نفّذ العمليات التالية:

Enqueue 5, Enqueue 10, Enqueue 15, Dequeue, Enqueue 20.

ما شكل الطابور النهائي؟ وما العنصر الموجود في المقدمة؟

### 10. الخلاصة

يعتمد Queue على مبدأ FIFO،
ويستخدم عندما يجب معالجة المهام حسب ترتيب وصولها.
""")


