import json, sys, os

version = 0.08
os.system('cls' if os.name == 'nt' else 'clear')
print(f'To-Do List alpha version {version}')

class Task:
    """Класс представления задачи"""
    def __init__(self, title: str, task_id: int) -> None:
        from datetime import datetime
        self.task_id = task_id
        self.title = title
        self.completed = False
        self.time_created = datetime.now().strftime('%d.%m.%Y %H:%M')

    def toggle(self) -> None:
        """Изменяем статус выполнения задачи на противоположный"""
        self.completed = not self.completed

    def to_dict(self) -> dict:
        """вернуть словарь"""
        return {
            "id": self.task_id,
            "title": self.title,
            "completed": self.completed,
            "time_created": self.time_created
        }

    def __str__(self) -> str:
        """вывод задачи str"""
        if self.completed:
            checkbox = '[.]'
        else:
            checkbox = '[ ]'
        return f'{checkbox} {self.task_id} {self.time_created} {self.title}'

class TaskManager:
    """Менеджер задач"""
    def __init__(self) -> None:
        self.file_name = "tasks.json"
        self.tasks = []
        self.next_id = 1
        self.load()

    def load(self) -> None:
        """Загрузить задачи из файла"""
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                max_id = 0
                for task_data in data:
                    task = Task(task_data["title"], task_data["id"])
                    task.completed = task_data["completed"]
                    task.time_created = task_data["time_created"]
                    self.tasks.append(task)
                    if task.task_id > max_id:
                        max_id = task.task_id
                self.next_id = max_id + 1
        except FileNotFoundError:
            self.tasks = []
            self.next_id = 1

    def save(self) -> None:
        """Сохранить в файл"""
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=2)

    def add(self, title: str) -> Task | None:
        """Создать и добавить объект Task  в список"""
        title = title.strip()
        if not title:
            print("Название не может быть пустым.")
            return None
        new_task = Task(title, self.next_id)
        self.tasks.append(new_task)
        self.next_id += 1
        self.save()
        return new_task
    
    def show_all(self) -> None:
        """Вывести все объекты Task"""
        if not self.tasks:
            print("Нет задач")
            return
        print('================Tasks==================')
        for task in self.tasks:
            print(task)

    def delete_by_id(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                removed = self.tasks.pop(i)
                self.save()
                print(f'Задача "{removed.title}" удалена.')
                return True
        print('Задача не найдена')
        return False
    
    def delete_all_tasks(self) -> None:
        """Удалить все задачи и начать новый id"""
        self.tasks = []
        self.next_id = 1
        self.save()
        print('Все задачи удалены.')

    def edit_task_by_id(self, task_id: int, new_title: str) -> bool:
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                task.title = new_title
                self.save()
                print(f'Задача "{task}" изменена.')
                return True
        print('Задача не найдена')
        return False
    
    def toggle_task(self, task_id) -> None:
        for task in self.tasks:
            if task.task_id == task_id:
                task.toggle()
                self.save()
                print(f'Задача "{task}" отмечена')



def menu() -> None:
    print('=======================================')
    print('1. Посмотреть задачи                  |')
    print('2. Добавить задачу                    |')
    print('3. Удалить задачу                     |')
    print('4. Редактировать задачу               |')
    print('5. Изменить статус выполнения задачи  |')
    print('6. Удалить все задачи                 |')
    print('0. Выйти                              |')
    print('=======================================')

def main():

    manager = TaskManager()

    while True:
        menu()
        choice = input('')
        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == '0':
            sys.exit()

        elif choice == '1':
            manager.show_all()

        elif choice == '2':
            print('Введите новую задачу:')
            new_task_title = input()
            manager.add(new_task_title)
            print(f'Задача "{new_task_title}" добавлена!')

        elif choice == '3':
            manager.show_all()
            try:
                print('Выберите id задачи для удаления:')
                number = int(input())
                manager.delete_by_id(number)
            except ValueError:
                print('Пожалуйста, введите число.')

        elif choice == '4':
            manager.show_all()
            try:
                task_id = int(input('Введите id задачи, которую желаете изменить: '))
                new_title = input('Введите новое название задачи\n')
                manager.edit_task_by_id(task_id, new_title)
            except ValueError:
                print('Пожалуйста, введите число.')

        elif choice == '5':
            manager.show_all()
            try:
                print('Выберите id задачи для отметки:')
                number = int(input())
                manager.toggle_task(number)
            except ValueError:
                print('Пожалуйста, введите число.')

        elif choice == '6':
            accept = input('Вы действительно хотите удалить все задачи?(да/нет)\n')
            if accept == 'да':
                manager.delete_all_tasks()


if __name__ == "__main__":
    main()