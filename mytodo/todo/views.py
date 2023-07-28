# from django.urls import reverse_lazy
# from django.contrib.auth import login
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .models import ToDoList,ToDoItem
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView


# Create your views here.

# class based
class CustomLoginView(LoginView):
    template_name = 'login1.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return  super(RegisterView,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return  redirect('list')
        return super(RegisterView, self).get(*args,**kwargs)


class ListListView(LoginRequiredMixin,ListView):
    model = ToDoList
    # context_object_name = 'task'
    template_name = 'index.html'

class ItemListView(LoginRequiredMixin,ListView):
    model = ToDoItem
    # context_object_name = 'task'
    template_name = 'todo_list.html'

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context['todo_list']=context['ToDoList'].filter(user=self.request.user)
#
#
class ListCreate(LoginRequiredMixin,CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context

class ItemCreate(LoginRequiredMixin,CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
        "completed",
        ]
    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ListDelete(DeleteView):
    model = ToDoList
    # You have to use reverse_lazy() instead of reverse(),
    # as the urls are not loaded when the file is imported.
    success_url = reverse_lazy("index")

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context


# class TaskCreate(LoginRequiredMixin,CreateView):
#     model=Task
#     fields = ['title','completed']
#     success_url=reverse_lazy('task_create') #redirect to task)create html
#     template_name = 'taskcreate.html'
#
#     def form_valid(self,form):
#         form.instance.user=self.request.user
#         return super(TaskCreate,self).form_valid(form)
#
# class TaskUpdate(LoginRequiredMixin,UpdateView):
#     model = Task
#     fields = ['title','description','completed']
#     success_url = reverse_lazy('task_list')
#     template_name = 'taskcreate.html'
#
# class TaskDelete(LoginRequiredMixin,DeleteView):
#     model = Task
#     context_object_name = 'task'
#     success_url = reverse_lazy('task_list')
#     template_name = 'taskdelete.html'
#
# class TaskDetailView(LoginRequiredMixin,DetailView):
#     model = Task
#     template_name = 'taskdetail.html'

