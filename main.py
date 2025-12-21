import json
import sys

version = 0.0004
print(f'To-Do List alpha version {version}')

class Task:
    """Класс представления задачи"""
    def __init__(self, title: str, task_id: int) -> None:
        from datetime import datetime
        self.task_id = task_id
        self.title = title
        self.completed = False
        self.time_created = datetime.now().strftime('%d.%m.%Y %H:%M')

    def toggle(self):
        self.completed = not self.completed

    def to_dict(self) -> dict:
        """вернуть словарь"""
        return {
            "id": self.task_id,
            "title": self.title,
            "completed": self.completed,
            "time_created": self.time_created
        }
    
    def from_dict(self, data: dict) -> None:
        """Загрузить данные из словаря"""
        self.task_id = data["task_id"]
        self.title = data["title"]
        self.completed = data["completed"]
        self.time_created = data["time_created"]

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

    def load(self):
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

    def save(self):
        """Сохранить в файл"""
        tasks_data = []
        for task in self.tasks:
            tasks_data.append({
                "id": task.task_id,
                "title": task.title,
                "completed": task.completed,
                "time_created": task.time_created
            })
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)

    def add(self, title: str) -> Task:
        """Создать и добавить объект Task  в список"""
        new_task = Task(title, self.next_id)
        self.tasks.append(new_task)
        self.next_id += 1
        self.save()
        print(f"Добавлена задача {new_task}")
        return new_task
    
    def show_all(self):
        """Вывести все объекты Task"""
        if not self.tasks:
            print("Нет задач")
            return
        print('====Tasks=====')
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


# def delete_task(number):
#     try:
#         with open('tasks.txt', 'r', encoding='utf-8') as file:
#             tasks = file.readlines()
        
#         if not tasks:
#             print('Список задач пуст!')
#             return
        
#         index = int(number) - 1

#         if 0 <= index < len(tasks):
#             removed_task = tasks[index].strip()

#             del tasks[index]

#             with open('tasks.txt', 'w', encoding='utf-8') as file:
#                 file.writelines(tasks)
#             print(f'Задача {number}. "{removed_task}" удалена!')
#         else:
#             print('неверный номер задачи!')
        
#     except ValueError:
#         print('Пожалуйста введите число')
#     except Exception as e:
#         print(f'Ошибка при удалении: {e}')

# def delete_all_tasks():
#     with open('tasks.txt', 'w', encoding='utf-8') as file:
#         pass
#     print('Все задачи удалены!')

# def edit_task():
#      try:
#         with open('tasks.txt', 'r', encoding='utf-8') as file:
#             tasks = file.readlines()
#         read_tasks()
#         print('Выберите задачу для редактирования')
#         index = int(input()) - 1
#         if 0 <= index < len(tasks):
#             old_task = tasks[index].strip()
#             print(f'Редактировать задачу "{old_task}"')
#             print('Введите новый текст задачи')
#             new_task = input()
#             tasks[index] = new_task + '\n'

#             with open('tasks.txt', 'w', encoding='utf-8') as file:
#                 file.writelines(tasks)
            
#             print(f'Задача изменена с "{old_task}" на "{new_task}"')
#         else:
#             print('Неверный номер задачи!')

#      except ValueError:
#          print('Пожалуйста, введите число!')
def menu():
     print('')
     print('1. П0смотреть задачи')
     print('2. Д0бавить задачу')
     print('3. Удалить задачу')
     print('4. Редактировать задачу')
     print('5. Удалить все задачи')
     print('6. Выйти\n')


def main():
    # task1 = Task('Sex1', 1)
    # print(task1)
    manager = TaskManager()

    while True:

        menu()

        choice = input('')
        print()

        if choice == '6':
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
                print('Пожалуйста, введите число')

        # elif choice == '4':
        #     edit_task()

        # elif choice == '5':
        #     accept = input('Вы действительно хотите удалить все задачи?(да/нет)\n')
        #     if accept == 'да':
        #         delete_all_tasks()


if __name__ == "__main__":
    main()