from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import FileForm, SimpleSearchForm, FileNotStatusForm
from webapp.models import File, FILE_STATUS, Private



class IndexView(ListView):
    model = File
    template_name = 'index.html'
    context_object_name = 'files'
    ordering = '-created_at'
    paginate_by = 2
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        # context['files'] = self.get_common_files()
        return context

    # def get_common_files(self):
    #     queryset = super().get_queryset().filter(file_status='common')
    #     return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = File.objects.filter(file_status='common')
        queryset = File.objects.filter()
        if self.search_value:
            query = Q(name__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class FileDetailView(DetailView):
    model = File
    template_name = 'detail.html'
    context_object_name = 'file'


class FileCreateView(CreateView):
    model = File
    template_name = 'create.html'

    def form_valid(self, form):
        File.objects.create(
            file=form.cleaned_data['file'],
            name=form.cleaned_data['name'],
            author=self.request.user,
            file_status=form.cleaned_data['file_status']
        )
        return redirect('webapp:index')

    def get_form_class(self):
        if self.request.user.id != None:
            return FileForm
        else:
            return FileNotStatusForm

    def get_success_url(self):
        return reverse('webapp:index')


class FileUpdateView(PermissionRequiredMixin, UpdateView):
    model = File
    template_name = 'update.html'
    form_class = FileForm
    context_object_name = 'file'

    def test_func(self):
        file = File.objects.get(id=self.kwargs['pk'])
        if (file.created_by == self.request.user) or (self.request.user.has_perm('webapp.delete_file')):
            return self.request.user

    def get_success_url(self):
        return reverse('webapp:file_detail_view', kwargs={'pk': self.object.pk})


class FileDeleteView(PermissionRequiredMixin, DeleteView):
    model = File
    pk_kwargs_url = 'pk'
    template_name = 'delete.html'
    context_object_name = 'file'

    def test_func(self):
        file = File.objects.get(id=self.kwargs['pk'])
        if (file.created_by == self.request.user) or (self.request.user.has_perm('webapp.delete_file')):
            return self.request.user

    def get_success_url(self):
        return reverse('webapp:index')


class AddUserToPrivateView(View):
    def post(self, request, *args, **kwargs):
        file_id = request.POST.get('file_id')
        user = request.POST.get('user_name')
        try:
            user_id = User.objects.get(username=user)
            private = Private.objects.get_or_create(file_id=file_id, user=user_id)
            print(file_id, user_id, private)
            if private[1] == False:
                return JsonResponse({'status': 'User already private'})
            else:
                return JsonResponse({'status': 'User Added to Private',
                                     'user': user_id.username, 'user_id': user_id.pk,
                                     })
        except User.DoesNotExist:
            return JsonResponse({'status': 'User does not exist'})


class DeleteFromPrivateView(View):
    def post(self, request):
        user_id = request.POST.get('user_id')
        user_in_private = Private.objects.get(user_id=user_id)
        user_id = user_in_private.user_id
        user_in_private.delete()
        return JsonResponse({'status': 'ok', 'user_id': user_id})






