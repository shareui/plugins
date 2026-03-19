# exteraGram Plugin API Changelog

---

> Может содержать неточности. May contain inaccuracies.

## `ui.settings`

### `Text` / `Текст`

• Added `subtext` to `text` / Добавлен `subtext` к `text`
```python
Text(text="Open settings", subtext="Tap to configure")
```

• Added `create_sub_fragment` callback returning a list of settings to open as a sub-page / Добавлен `create_sub_fragment` callback, возвращающий список настроек для открытия как вложенной страницы
```python
Text(
    text="Advanced",
    create_sub_fragment=lambda: [
        Switch(key="option_a", text="Option A", default=False),
        Switch(key="option_b", text="Option B", default=True),
    ]
)
```

---

### `Switch` / `Переключатель`

• Added `subtext`, `on_long_click`, `link_alias` parameters / Добавлены параметры `subtext`, `on_long_click`, `link_alias`
```python
Switch(
    key="ghost_mode",
    text="Ghost mode",
    default=False,
    subtext="Hides typing status",
    on_long_click=lambda view: show_info(),
    link_alias="ghost-mode"
)
```

---

### `Input` / `Ввод`

• Added `subtext`, `on_long_click`, `link_alias` parameters / Добавлены параметры `subtext`, `on_long_click`, `link_alias`
```python
Input(key="city", text="City", default="Moscow", subtext="Used for weather")
```

---

### `Selector` / `Селектор`

• Added `on_long_click`, `link_alias` parameters / Добавлены параметры `on_long_click`, `link_alias`
```python
Selector(key="theme", text="Theme", default=0, items=["Light", "Dark"], link_alias="theme")
```

---

### `Custom` / `Кастомный элемент`

• Added `create_sub_fragment` opens a sub-page on click / Добавлен `create_sub_fragment` открывает вложенную страницу при нажатии
```python
Custom(
    factory=my_factory,
    create_sub_fragment=lambda: [
        Header(text="Sub settings"),
        Switch(key="x", text="X", default=False),
    ]
)
```

• Added `on_long_click`, `link_alias` parameters / Добавлены параметры `on_long_click`, `link_alias`

---

## `base_plugin`

### `MenuItemData`

• Added `subtext` field secondary text under the menu item label / Добавлено поле `subtext` дополнительный текст под названием пункта меню
```python
MenuItemData(
    menu_type=MenuItemType.MESSAGE_CONTEXT_MENU,
    text="Copy text",
    subtext="Copies plain text",
    on_click=lambda ctx: handle(ctx)
)
```

---

### `HookFilter` / Фильтры хуков

• Added `@hook_filters` decorator for `before_hooked_method` / `after_hooked_method` / Добавлен декоратор `@hook_filters` — управляет условием срабатывания хука
```python
from base_plugin import MethodHook, hook_filters, HookFilter

class MyHook(MethodHook):
    @hook_filters(HookFilter.RESULT_NOT_NULL)
    def after_hooked_method(self, param):
        self.plugin.log(f"result: {param.getResult()}")
```

• Added `HookFilter.Or(*filters)` combines filters with OR logic / Добавлен `HookFilter.Or(*filters)` объединяет фильтры по логике OR
```python
@hook_filters(HookFilter.Or(HookFilter.RESULT_IS_NULL, HookFilter.RESULT_IS_FALSE))
def after_hooked_method(self, param):
    ...
```

• Added `HookFilter.Condition(expr)` MVEL expression as filter / Добавлен `HookFilter.Condition(expr)` MVEL-выражение как фильтр
```python
@hook_filters(HookFilter.Condition("args[0] != null && args[0].length > 0"))
def before_hooked_method(self, param):
    ...
```

---

### `BaseHook`

• New class inline alternative to `MethodHook` subclassing / Новый класс inline-альтернатива наследованию от `MethodHook`
```python
from base_plugin import BaseHook, HookFilter

hook = BaseHook(
    plugin=self,
    before=lambda param: self.log("before"),
    after=lambda param: self.log("after"),
    after_filters=[HookFilter.RESULT_NOT_NULL]
)
self.hook_method(method, hook)
```

---

### `hook_method` / `hook_all_methods` / `hook_all_constructors`

• Now accept `before` / `after` callbacks directly, without subclassing `MethodHook` / Теперь принимают `before` / `after` callback-и напрямую, без создания подкласса `MethodHook`
• Added `before_filters` / `after_filters` params / Добавлены параметры `before_filters` / `after_filters`
```python
def on_plugin_load(self):
    method = ...  # java.lang.reflect.Method
    self.hook_method(
        method,
        before=lambda param: self.log(f"called with: {param.args[0]}"),
        before_filters=[HookFilter.ArgumentNotNull(0)]
    )
```

---

## `client_utils`

• Added `send_text` shortcut for sending a plain text message / Добавлен `send_text` удобная отправка текстового сообщения
```python
from client_utils import send_text
send_text(peer=dialog_id, text="Hello!")
```

• Added `send_photo`, `send_document`, `send_video`, `send_audio` / Добавлены функции отправки медиа
```python
from client_utils import send_photo, send_video, send_audio, send_document
send_photo(peer=dialog_id, file_path="/sdcard/pic.jpg", caption="Look at this")
send_video(peer=dialog_id, file_path="/sdcard/clip.mp4")
```

• Added `edit_message` edit text or media of an existing message / Добавлен `edit_message` редактирование текста или медиа существующего сообщения
```python
from client_utils import edit_message
edit_message(message_obj, text="Updated text", parse_mode="markdown")
```

• `send_message` / `send_text` now support `parse_mode="html"` / `"markdown"` / Добавлена поддержка `parse_mode` в `send_message` и `send_text`
```python
send_text(peer=dialog_id, text="**bold** _italic_", parse_mode="markdown")
send_text(peer=dialog_id, text="<b>bold</b> <i>italic</i>", parse_mode="html")
```

• Added `run_on_queue(fn, queue_name, delay)` run code on a specific dispatch queue / Добавлен `run_on_queue` — запуск кода в конкретной очереди
```python
from client_utils import run_on_queue, PLUGINS_QUEUE
run_on_queue(lambda: self.log("on plugins queue"), PLUGINS_QUEUE)
```

• Added `NotificationCenterDelegate` proxy class / Добавлен прокси-класс `NotificationCenterDelegate`
```python
from client_utils import NotificationCenterDelegate
from java import Override, jvoid, jint, jarray
from java.lang import Object

class MyDelegate(NotificationCenterDelegate):
    @Override(jvoid, [jint, jint, jarray(Object)])
    def didReceivedNotification(self, id, account, args):
        self.plugin.log(f"notification id: {id}")
```

---

## `hook_utils` (new module / новый модуль)

• `find_class(class_name)` safe class lookup by name / Безопасный поиск класса по имени
```python
from hook_utils import find_class
clazz = find_class("org.telegram.ui.ChatActivity")
```

• `get_private_field(obj, field_name)` / `set_private_field(obj, field_name, value)` — read/write private instance fields / Чтение и запись приватных полей объекта
```python
from hook_utils import get_private_field, set_private_field
value = get_private_field(some_obj, "mField")
set_private_field(some_obj, "mField", new_value)
```

• `get_static_private_field(clazz, field_name)` / `set_static_private_field(clazz, field_name, value)` — same for static fields / То же для статических полей
```python
from hook_utils import get_static_private_field
val = get_static_private_field(clazz, "INSTANCE")
```

---

## `android_utils`

• Added `copy_to_clipboard(text)` copies text and shows a bulletin / Добавлен `copy_to_clipboard(text)` — копирует текст и показывает уведомление
```python
from android_utils import copy_to_clipboard
copy_to_clipboard("some text")
```
It could have been done earlier, but it was more difficult. / Это можно было сделать раньше, но это было бы сложнее.
