# Ngenix test task

Написать программу на Python, которая делает следующие действия:

1.Создает 50 zip-архивов, в каждом 100 xml файлов со случайными данными следующей структуры:

```xml
<root>
    <var name='id' value='<случайное уникальное строковое значение>'/>
    <var name='level' value='<случайное число от 1 до 100>'/>
    <objects>
        <object name='<случайное строковое значение>'/>
        <object name='<случайное строковое значение>'/>
    </objects>
</root>
```

В тэге objects случайное число (от 1 до 10) вложенных тэгов object.

2.Обрабатывает директорию с полученными zip архивами, разбирает вложенные xml файлы и формирует 2 csv файла:

- Первый: id, level - по одной строке на каждый xml файл
- Второй: id, object_name - по отдельной строке для каждого тэга object (получится от 1 до 10 строк на каждый xml файл)

Очень желательно сделать так, чтобы задание 2 эффективно использовало ресурсы многоядерного процессора. 

Также желательно чтобы программа работала быстро.

Формулировка задания имеет неоднозначность в строке
```xml
    <var name='id' value='<случайное уникальное строковое значение>'/>
```
Строка может быть случайной, но тогда не обязательно будет уникальной.
Либо строка может быть уникальной, но тогда не будет случайной, т.к. формируется по правилам, обеспечивающим ее уникальность.

Для реализации выбрано правило уникальной строки, т.к. больше подходит по контексту (формируется значение для атрибута с именем 'id').

[Другая реализация](https://github.com/droppoint/ngenix-demo-task) этого задания.
