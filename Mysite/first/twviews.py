from django.views.generic.base import TemplateView,ContextMixin
from django.views.generic.list import ListView
from django.core.paginator import Paginator, InvalidPage
from django.views.generic.detail import DetailView
from first.models import Category, Good,New
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic.edit import ProcessFormView
from django.core.urlresolvers import reverse
from django import forms
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields ='__all__'
        exclude =()
    name = forms.CharField(label="Name",help_text="Must be unique")
    description = forms.CharField(widget = forms.Textarea, label="Descript")
    category = forms.ModelChoiceField(queryset=Category.objects.all(),label="category",empty_label =None)
    in_stock = forms.BooleanField(label="Have")    


class CategoryListMixin(ContextMixin):
    def get_context_data(self,**kwargs):
        context = super(CategoryListMixin,self).get_context_data(**kwargs)
        context["cats"] = Category.objects.order_by("name")
        return context

class GoodListView(ListView,CategoryListMixin):
    template_name = "index.html"
    paginate_by = 1
    cat = None
    def get (self,request,*args,**kwargs):
        if self.kwargs["cat_id"] ==None:
            self.cat = Category.objects.first()
        else:
            self.cat = Category.objects.get(pk = self.kwargs["cat_id"])
        return super(GoodListView,self).get(request,*args,**kwargs)
    def get_queryset(self):
        return Good.objects.filter(category =self.cat).order_by("name")
                    
    def get_context_data(self, **kwargs):
        context = super(GoodListView,self).get_context_data(**kwargs)
        context["category"] = self.cat
        return context
             
class GoodDetailView(DetailView,CategoryListMixin):
    model = Good
    template_name = "good.html"
    pk_url_kwarg = "good_id"
    def get_context_data(self, **kwargs):
        context = super(GoodDetailView,self).get_context_data(**kwargs)
        try:
            context["pn"] = self.request.GET["page"]
        except KeyError:
            context["pn"] = 1
        return context          
     
     
     
     
        
class GoodEditMixin(CategoryListMixin):
    def get_context_data(self, **kwargs):
        context = super(GoodEditMixin,self).get_context_data(**kwargs)
        try:
            context["pn"]= self.request.GET["page"]
        except KeyError:
            context["pn"] = "1"
        return context
        
        
class GoodEditView(ProcessFormView):
	def post(self,request,*args,**kwargs):
		try:
			pn = request.GET["page"]
		except KeyError:
			pn = "1"
		self.success_url = self.success_url + "?page="+pn
		return super(GoodEditView,self).post(request,*args,**kwargs)
		
		
class GoodCreate(SuccessMessageMixin
,CreateView,GoodEditMixin):
	model = Good
	form_class = GoodForm
	#fields='__all__'
	template_name = "good_add.html"
	def get(self,request,*args,**kwargs):
	  
		if self.kwargs["cat_id"] != None:
		  cat = Category.objects.get(pk=self.kwargs["cat_id"])
		else:    
			cat = Category.objects.first()
		try:
		  in_stock = request.session["in_stock"]
		except:
		  in_stock = True
		self.form = GoodForm(initial={"category":cat,"in_stock":in_stock})
		self.initial["category"] = Category.objects.get(pk=self.kwargs["cat_id"])    
		return super(GoodCreate,self).get(request,*args,**kwargs)
	
	def post(self,request,*args,**kwargs):
		self.success_url = reverse("index",kwargs = {"cat_id": Category.objects.get(pk = self.kwargs["cat_id"]).id})
		self.form = GoodForm(request.POST)
		if self.form.is_valid():
		  request.session["in_stock"] = self.form.cleaned_data["in_stock"]
		  self.form.save()
		  return redirect("index",cat_id=Category.objects.get(pk=self.kwargs["cat_id"]).id)
		else:
		  return super(GoodCreate,self).post(request,*args,**kwargs)
	
	
	def get_context_data(self,**kwargs):
		context=super(GoodCreate,self).get_context_data(**kwargs)
		context["category"]=Category.objects.get(pk=self.kwargs["cat_id"])
		return context
		
		
class GoodUpdate(SuccessMessageMixin,UpdateView,GoodEditMixin,GoodEditView):
	success_message="Item successfuly changed"
	model = Good
	form_class = GoodForm
	#fields='__all__'
	template_name = "good_edit.html"
	pk_url_kwarg = "good_id"
	def post(self, request,*args,**kwargs):
		self.success_url = reverse("index",kwargs = {"cat_id":Good.objects.get(pk = kwargs["good_id"]).category.id})
		return super(GoodUpdate,self).post(request,*args, **kwargs)
		
		
class GoodDelete(DeleteView,GoodEditMixin,GoodEditView):
    model =Good
    template_name = "good_delete.html"
    fields='__all__'
    pk_url_kwarg = "good_id"
    def post(self,request,*args,**kwargs):
        self.success_url = reverse("index", kwargs = {"cat_id":Good.objects.get(pk = kwargs["good_id"]).category.id})
        return super(GoodDelete,self).post(request,*args,**kwargs)
    ####why
    def get_context_data(self, **kwargs):
        context = super(GoodDelete, self).get_context_data(**kwargs)
        context["good"] = self.object
        return context     
		
		
		
		
		
		
		
		
		
		
		
		                        
