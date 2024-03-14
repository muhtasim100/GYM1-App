from django.test import TestCase
from gymapp.models import ToDoList, Item

# Create your tests here.

class ModelsTest(TestCase):
    def test_list(self):
        todolist = ToDoList(name="Test_List")
        todolist.save()
        item = Item(todolist=todolist, text="Item1", complete=False)
        item.save()
        print(ToDoList.objects.all())



        
