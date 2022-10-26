from django.shortcuts import reverse, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.generic.base import ContextMixin

from django_tables2 import RequestConfig

from .models import Tags, Note
from .forms import NoteForm, TagForm
from .tables import TagsTable


#@method_decorator(staff_member_required, name='dispatch')
class NoteHomepageView(ListView):
    template_name = 'notes/homepage.html'
    model = Note
    
    def get_queryset(self):
        qs = Note.objects.all()
        qs = Note.filters_data(self.request, qs)
        return qs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = NoteForm()
        context['pinned_qs'] = self.object_list.filter(pinned=True)
        context['qs'] = self.object_list.filter(pinned=False)[:30]
        return context


#@staff_member_required
def validate_new_note_view(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Новая заметка создана')
    return redirect(reverse('notes:home'))


class NoteUpdateView(UpdateView):
    form_class = NoteForm
    success_url = reverse_lazy('notes:home')
    template_name = 'notes/form.html'
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = f'Название {self.object.title}'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'Успешно!')
        return super().form_valid(form)



def pinned_view(request, pk):
    instance = get_object_or_404(Note, id=pk)
    instance.pinned = False if instance.pinned else True
    instance.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), reverse('notes:home'))


def delete_note_view(request, pk):
    instance = get_object_or_404(Note, id=pk)
    instance.delete()
    messages.warning(request, 'Вы удалили заметку')
    return redirect(reverse('notes:home'))

class NameContextMixin(ContextMixin):

    def get_context_data(self, *args, **kwargs):
        """
        Отвечает за передачу параметров в контекст
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'Теги'
        return context

class TagListView(ListView, NameContextMixin):
    model = Tags
    template_name = 'notes/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        """
        Получение данных
        :return:
        """
        return Tags.objects.all()


# детальная информация
class TagDetailView(DetailView, NameContextMixin):
    model = Tags
    template_name = 'notes/tag_detail.html'

    def get(self, request, *args, **kwargs):
        """
        Метод обработки get запроса
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.tag_id = kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Получение этого объекта
        :param queryset:
        :return:
        """
        return get_object_or_404(Tags, pk=self.tag_id)

class TagCreateView(CreateView, NameContextMixin):
    # form_class =
    fields = '__all__'
    model = Tags
    success_url = reverse_lazy('blog:tag_list')
    template_name = 'notes/tag_create.html'

    def post(self, request, *args, **kwargs):
        """
        Пришел пост запрос
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Метод срабатывает после того как форма валидна
        :param form:
        :return:
        """
        return super().form_valid(form)


class TagUpdataView(UpdateView):
    fields = '__all__'
    model = Tags
    success_url = reverse_lazy('blog:tag_list')
    template_name = 'notes/tag_create.html'


class TagDeleteView(DeleteView):
    template_name = 'notes/tag_delete_confirm.html'
    model = Tags
    success_url = reverse_lazy('blog:tag_list')




