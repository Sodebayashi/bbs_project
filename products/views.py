from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Products
from .forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class IndexView(generic.ListView):
    model = Products
    template_name = 'products/index.html'

class DetailView(generic.DetailView):
    model = Products
    template_name = 'products/detail.html'

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Products
    template_name = 'products/create.html'
    fields = ['title', 'content', 'price', 'image']
    success_url = reverse_lazy('products:index')

    def form_valid(self, form):
        form.instance.author = self.request.user

        try:
            return super().form_valid(form)
        except Exception:
            import traceback
            traceback.print_exc()
            raise
        
    def post(self, request, *args, **kwargs):
        print("FILES:", request.FILES)
        return super().post(request, *args, **kwargs)
    

class UpdateView(LoginRequiredMixin,generic.edit.UpdateView):
    model = Products
    template_name = 'products/create.html'
    fields = ['content']
    success_url = reverse_lazy('products:index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)
    
    # カスタム403のビュー(アクセス権限が無い場合)
def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {'error_message': str(exception)}, status=403)

class DeleteView(LoginRequiredMixin,generic.edit.DeleteView):
    model = Products
    template_name= 'products/delete.html'
    success_url = reverse_lazy('bbs:index') #フォームが正常に送信のリダイレクト先

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('削除権限がありません')
        return super(DeleteView, self).dispatch(request, *args, **kwargs)


def search(request):
    productss = None
    searchform = SearchForm(request.GET)

    if searchform.is_valid():
        query = searchform.cleaned_data['words']
        productss = Products.objects.filter(title__icontains=query)

    return render(request, 'products/results.html', {'productss':productss,'searchform':searchform})