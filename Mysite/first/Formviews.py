from django.views.generic.edit import CreativeView, UpdateView,DeleteView
from django.views.generic.edit import ProcessFormView
from django.core.urlresolvers import reverse

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
		self.success_url = self.success_url+"?page="+pn
		return super(GoodEfitView,self).post(request,*args,**kwargs)
		
		
class GoodCreate(CreateView,GoodEditMixin):
	model = Good
	template_name = "good_add.html"
	def get(self,request,*args,**kwargs):
		if self.kwargs["cat_id"] !=None:
			self.initial["actegory"] = Category.objects.get(pk = self.kwargs["cat_id"])
		return super(GoodCreate,self).get(request,*args,**kwargs)
	def post(self,request,*args,**kwargs):
		self,success_url = reverse("index",kwargs = {"cat_id": Category.objects.get(pk = self.kwargs["cat_id"]).id})
		return super(Good.Create,self).post(request,*args,**kwargs)
	def get_context_data(self,**kwargs):
		context=super(GoodCreate,self).get_context_data(**kwargs)
		context["category"]=Category.objects.get(pk=self.kwargs["cat_id"])
		return context
		
		
class GoodUpdate(UpdateView,GoodeEditMixin,GoodEditView):
	model = Good
	template_name = "good_edit.html"
	pk_url_kwarg = "good_id"
	def post(self, request,*args,**kwargs):
		self,success_url = reverse("index",kwargs = {"cat_id":Good.objects.get(pk = kwargs["good_id"]).category.id})
		return super(GoodUpdate,self).post(request,*args, **kwargs)
class GoodDelete(DeleteView,GoodEditMixin,GoodEditView):
	model =Good
	template_name = "good_delete.html"
	pr_url_kwarg = "good_id"
	def post(self,request,*args,**kwargs):
		self.success_url = reverse("index",kwargs = {"cat_id":Good.objects.get(pk = kwargs["good_id"]).category.id})
		return super(GoodDelete,self).post(request,*args,**kwargs)
	def get_context_data(self,**kwargs):
		context = super(GoodDelete,self).get_context_data(**kwargs)
		context["good"] = Good.objects.get(pk = kwargs["good_id"])
		return context
