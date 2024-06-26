$(document).ready(function () {
    $('#table_id').DataTable({
        language: {
            "processing": "Подождите...",
            "search": "Поиск:",
            "lengthMenu": "Показать _MENU_ записей",
            "info": "Записи с _START_ до _END_ из _TOTAL_ записей",
            "infoEmpty": "Записи с 0 до 0 из 0 записей",
            "infoFiltered": "(отфильтровано из _MAX_ записей)",
            "loadingRecords": "Загрузка записей...",
            "zeroRecords": "Записи отсутствуют.",
            "emptyTable": "В таблице отсутствуют данные",
            "paginate": {
                "first": "Первая",
                "previous": "Предыдущая",
                "next": "Следующая",
                "last": "Последняя"
            },
            "aria": {
                "sortAscending": ": активировать для сортировки столбца по возрастанию",
                "sortDescending": ": активировать для сортировки столбца по убыванию"
            },
            "select": {
                "rows": {
                    "_": "Выбрано записей: %d",
                    "1": "Выбрана одна запись"
                },
                "cells": {
                    "_": "Выбрано %d ячеек",
                    "1": "Выбрана 1 ячейка "
                },
                "columns": {
                    "1": "Выбран 1 столбец ",
                    "_": "Выбрано %d столбцов "
                }
            },
            "searchBuilder": {
                "conditions": {
                    "string": {
                        "startsWith": "Начинается с",
                        "contains": "Содержит",
                        "empty": "Пусто",
                        "endsWith": "Заканчивается на",
                        "equals": "Равно",
                        "not": "Не",
                        "notEmpty": "Не пусто",
                        "notContains": "Не содержит",
                        "notStartsWith": "Не начинается на",
                        "notEndsWith": "Не заканчивается на"
                    },
                    "date": {
                        "after": "После",
                        "before": "До",
                        "between": "Между",
                        "empty": "Пусто",
                        "equals": "Равно",
                        "not": "Не",
                        "notBetween": "Не между",
                        "notEmpty": "Не пусто"
                    },
                    "number": {
                        "empty": "Пусто",
                        "equals": "Равно",
                        "gt": "Больше чем",
                        "gte": "Больше, чем равно",
                        "lt": "Меньше чем",
                        "lte": "Меньше, чем равно",
                        "not": "Не",
                        "notEmpty": "Не пусто",
                        "between": "Между",
                        "notBetween": "Не между ними"
                    },
                    "array": {
                        "equals": "Равно",
                        "empty": "Пусто",
                        "contains": "Содержит",
                        "not": "Не равно",
                        "notEmpty": "Не пусто",
                        "without": "Без"
                    }
                },
                "data": "Данные",
                "deleteTitle": "Удалить условие фильтрации",
                "logicAnd": "И",
                "logicOr": "Или",
                "title": {
                    "0": "Конструктор поиска",
                    "_": "Конструктор поиска (%d)"
                },
                "value": "Значение",
                "add": "Добавить условие",
                "button": {
                    "0": "Конструктор поиска",
                    "_": "Конструктор поиска (%d)"
                },
                "clearAll": "Очистить всё",
                "condition": "Условие",
                "leftTitle": "Превосходные критерии",
                "rightTitle": "Критерии отступа"
            },
            "searchPanes": {
                "clearMessage": "Очистить всё",
                "collapse": {
                    "0": "Панели поиска",
                    "_": "Панели поиска (%d)"
                },
                "count": "{total}",
                "countFiltered": "{shown} ({total})",
                "emptyPanes": "Нет панелей поиска",
                "loadMessage": "Загрузка панелей поиска",
                "title": "Фильтры активны - %d",
                "showMessage": "Показать все",
                "collapseMessage": "Скрыть все"
            },
            "buttons": {
                "pdf": "PDF",
                "print": "Печать",
                "collection": "Коллекция <span class=\"ui-button-icon-primary ui-icon ui-icon-triangle-1-s\"><\/span>",
                "colvis": "Видимость столбцов",
                "colvisRestore": "Восстановить видимость",
                "copy": "Копировать",
                "copyKeys": "Нажмите ctrl or u2318 + C, чтобы скопировать данные таблицы в буфер обмена.  Для отмены, щелкните по сообщению или нажмите escape.",
                "copyTitle": "Скопировать в буфер обмена",
                "csv": "CSV",
                "excel": "Excel",
                "pageLength": {
                    "-1": "Показать все строки",
                    "_": "Показать %d строк",
                    "1": "Показать 1 строку"
                },
                "removeState": "Удалить",
                "renameState": "Переименовать",
                "copySuccess": {
                    "1": "Строка скопирована в буфер обмена",
                    "_": "Скопировано %d строк в буфер обмена"
                },
                "createState": "Создать состояние",
                "removeAllStates": "Удалить все состояния",
                "savedStates": "Сохраненные состояния",
                "stateRestore": "Состояние %d",
                "updateState": "Обновить"
            },
            "decimal": ".",
            "infoThousands": ",",
            "autoFill": {
                "cancel": "Отменить",
                "fill": "Заполнить все ячейки <i>%d<i><\/i><\/i>",
                "fillHorizontal": "Заполнить ячейки по горизонтали",
                "fillVertical": "Заполнить ячейки по вертикали",
                "info": "Информация"
            },
            "datetime": {
                "previous": "Предыдущий",
                "next": "Следующий",
                "hours": "Часы",
                "minutes": "Минуты",
                "seconds": "Секунды",
                "unknown": "Неизвестный",
                "amPm": [
                    "AM",
                    "PM"
                ],
                "months": {
                    "0": "Январь",
                    "1": "Февраль",
                    "10": "Ноябрь",
                    "11": "Декабрь",
                    "2": "Март",
                    "3": "Апрель",
                    "4": "Май",
                    "5": "Июнь",
                    "6": "Июль",
                    "7": "Август",
                    "8": "Сентябрь",
                    "9": "Октябрь"
                },
                "weekdays": [
                    "Вс",
                    "Пн",
                    "Вт",
                    "Ср",
                    "Чт",
                    "Пт",
                    "Сб"
                ]
            },
            "editor": {
                "close": "Закрыть",
                "create": {
                    "button": "Новый",
                    "title": "Создать новую запись",
                    "submit": "Создать"
                },
                "edit": {
                    "button": "Изменить",
                    "title": "Изменить запись",
                    "submit": "Изменить"
                },
                "remove": {
                    "button": "Удалить",
                    "title": "Удалить",
                    "submit": "Удалить",
                    "confirm": {
                        "_": "Вы точно хотите удалить %d строк?",
                        "1": "Вы точно хотите удалить 1 строку?"
                    }
                },
                "multi": {
                    "restore": "Отменить изменения",
                    "title": "Несколько значений",
                    "noMulti": "Это поле должно редактироваться отдельно, а не как часть группы",
                    "info": "Выбранные элементы содержат разные значения для этого входа.  Чтобы отредактировать и установить для всех элементов этого ввода одинаковое значение, нажмите или коснитесь здесь, в противном случае они сохранят свои индивидуальные значения."
                },
                "error": {
                    "system": "Возникла системная ошибка (<a target=\"\\\" rel=\"nofollow\" href=\"\\\">Подробнее<\/a>)."
                }
            },
            "searchPlaceholder": "Что ищете?",
            "stateRestore": {
                "creationModal": {
                    "button": "Создать",
                    "search": "Поиск",
                    "columns": {
                        "search": "Поиск по столбцам",
                        "visible": "Видимость столбцов"
                    },
                    "name": "Имя:",
                    "order": "Сортировка",
                    "paging": "Страницы",
                    "scroller": "Позиция прокрутки",
                    "searchBuilder": "Редактор поиска",
                    "select": "Выделение",
                    "title": "Создать новое состояние",
                    "toggleLabel": "Включает:"
                },
                "removeJoiner": "и",
                "removeSubmit": "Удалить",
                "renameButton": "Переименовать",
                "duplicateError": "Состояние с таким именем уже существует.",
                "emptyError": "Имя не может быть пустым.",
                "emptyStates": "Нет сохраненных состояний",
                "removeConfirm": "Вы уверены, что хотите удалить %s?",
                "removeError": "Не удалось удалить состояние.",
                "removeTitle": "Удалить состояние",
                "renameLabel": "Новое имя для %s:",
                "renameTitle": "Переименовать состояние"
            },
            "thousands": " "
        }
    });
});

$(document).ready(function () {
    url = document.location.href
    if (document.location.pathname == "/")
        $('a[href="/"]').addClass('active');
    if (url.includes('brand'))
        $('a[href="/brand/"]').addClass('active');
    if (url.includes('model'))
        $('a[href="/model/"]').addClass('active');
    if (url.includes('generation'))
        $('a[href="/generation/"]').addClass('active');
    if (url.includes('restyling'))
        $('a[href="/restyling/"]').addClass('active');
    if (url.includes('configuration'))
        $('a[href="/configuration/"]').addClass('active');
})

$('.menu_button').click(function () {
    $(this).toggleClass('active');
    $('.menu_button').not(this).removeClass('active');
})

function toggleShow(option, show) {
    $(option).toggle(show);
    if (show) {
        if ($(option).parent('span.toggleOption').length)
            $(option).unwrap();
    } else {
        if ($(option).parent('span.toggleOption').length == 0)
            $(option).wrap('<span class="toggleOption" style="display: none;" />');
    }
}

function onSelectChange(obj, chooseEmpty = true) {
    const childSelect = $(`select[name="${obj.getAttribute('data-child')}"]`)[0]
    childSelect.disabled = !Boolean(obj.value);

    let children = obj.options[obj.selectedIndex].getAttribute('data-children');
    if (children) {
        children = children.split(',').map(Number)
    } else {
        children = [];
    }
    Array.from(childSelect.querySelectorAll('option')).forEach((option) => {
        if (!Boolean(option.value) & chooseEmpty)
            option.selected = 'selected';

        toggleShow(
            option,
            Boolean(children.includes(Number(option.value)) | !Boolean(option.value))
        );
    });

    if (childSelect.getAttribute('data-child'))
        onSelectChange(childSelect, chooseEmpty);
}

function toggleHideClass(obj, className) {
    for (let el of document.querySelectorAll(`.${className}`)) el.style.display = ((obj.checked) ? '' : 'none');
}


function onCheckParam(checkBox) {
    let parent = document.querySelector(`[data-child='${checkBox.className}'] [data-selected=true]`);
    if (!!parent) {
        let children = parent.getAttribute('data-children')
        children = ((children) ? children.split(',').map(Number) : [])

        if (checkBox.checked) children.push(checkBox.id)
        else {
            let index = children.indexOf(checkBox.id);
            children.splice(index, 1);
        }

        parent.setAttribute('data-children', children)
    }

    let selected = document.querySelector(`input.${checkBox.className}[data-selected=true]`);
    let selected_id = (!!selected) ? selected.id : null

    if (!checkBox.disabled) {
        setColumn(
            checkBox.className,
            false,
            ((!!selected && (checkBox.id === selected_id)) ? null : selected_id),
            getChecked(checkBox.className)
        );
    }
}

function getChecked(className) {
    let arr = [];
    for (let checkBox of document.querySelectorAll(`input.${className}:checked`)) {
        arr.push(checkBox.id)
    }
    return ((!!arr) ? arr.join() : null);
}

function onSelectParam(label) {
    let checkBox = document.getElementById(label.getAttribute('data-for'));
    if ((checkBox.checked && !checkBox.disabled) || label.className === 'root_params') {
        setColumn(
            label.className,
            false,
            checkBox.id,
            getChecked(label.className)
        );
    }
}

function setCheckBox(checkBox, disabled, checked) {
    checkBox.disabled = disabled;
    checkBox.checked = checked;
}

function setSelection(checkBox, selected) {
    checkBox.setAttribute('data-selected', selected);
    checkBox.parentElement.style.backgroundColor = ((selected) ? 'thistle' : 'unset');
}


function setColumn(className, disabled, selected, checked) {
    let childClassName = null;
    let checkedChildren = null;
    checked = ((checked) ? checked.split(',').map(Number) : []);
    for (let checkBox of document.querySelectorAll(`input.${className}`)) {
        setCheckBox(
            checkBox,
            disabled,
            (!disabled && checked.includes(Number(checkBox.id)))
        );

        let curCBSelected = (!disabled && (selected === checkBox.id))
        setSelection(checkBox, curCBSelected);

        childClassName = checkBox.parentElement.parentElement.getAttribute('data-child');
        checkedChildren = ((curCBSelected) ? checkBox.getAttribute('data-children') : checkedChildren);
    }

    if (childClassName) setColumn(childClassName, !selected, null, checkedChildren)
}


$(document).ready(function () {
    setColumn('root_params', false, null, null);

    onSelectChange(($('select[name="brand"]')[0]), false);
    onSelectChange(($('select[name="attributes__restrictions__rim__drilling__rec"]')[0]), false);
    onSelectChange(($('select[name="attributes__restrictions__rear_rim__drilling__rec"]')[0]), false);
    onSelectChange(($('select[name="attributes__restrictions__tire__diameter__rec"]')[0]), false);
    onSelectChange(($('select[name="attributes__restrictions__rear_tire__diameter__rec"]')[0]), false);
    toggleHideClass(($('input[name="attributes__restrictions__different_rims"]')[0]), 'rearRims');
    toggleHideClass(($('input[name="attributes__restrictions__different_tires"]')[0]), 'rearTires');
})


function submitForm(e) {
    e.preventDefault();

    let data = {}
    for (let checkBox of document.querySelectorAll('input[type=checkbox]')) {
        let children = checkBox.getAttribute('data-children')
        data[checkBox.id] = ((children) ? children.split(',').map(Number) : [])
    }

    fetch(document.URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: [
            `csrfmiddlewaretoken=${document.querySelector('input[name="csrfmiddlewaretoken"]').value}`,
            'dataJson=' + JSON.stringify(data)
        ].join("&")
    })
}