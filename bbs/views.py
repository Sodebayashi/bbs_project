from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Article
from .forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class IndexView(generic.ListView):
    model = Article
    template_name = 'bbs/index.html'

class DetailView(generic.DetailView):
    model = Article
    template_name = 'bbs/detail.html'

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    template_name = 'bbs/create.html'
    fields = ['content']

    def form_valid(self, form): # バリテーション通過時に呼び出し
        form.instance.author = self.request.user # authorにログインユーザーを渡す
        return super(CreateView, self).form_valid(form) # クラスのメソッド呼び出し
    

class UpdateView(LoginRequiredMixin,generic.edit.UpdateView):
    model = Article
    template_name = 'bbs/create.html'
    fields = ['content']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)
    
    # カスタム403のビュー(アクセス権限が無い場合)
def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {'error_message': str(exception)}, status=403)

class DeleteView(LoginRequiredMixin,generic.edit.DeleteView):
    model = Article
    template_name= 'bbs/delete.html'
    success_url = reverse_lazy('bbs:index') #フォームが正常に送信のリダイレクト先

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('削除権限がありません')
        return super(DeleteView, self).dispatch(request, *args, **kwargs)


def search(request):
    articles = None
    searchform = SearchForm(request.GET)

    if searchform.is_valid():
        query = searchform.cleaned_data['words']
        articles = Article.objects.filter(content__icontains=query)

    return render(request, 'bbs/results.html', {'articles':articles,'searchform':searchform})