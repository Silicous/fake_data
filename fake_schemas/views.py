from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import RedirectView, ListView, CreateView, DeleteView, UpdateView, DetailView
from django.views.generic.edit import FormMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

from .forms import FakeSchemaForm, FakeSchemaColumnsForm, FakeSchemaColumnInline, ExportDatasetForm
from .models import FakeSchemas, FakeSchemasColumn
from .tasks import generate_csv_task

# Create your views here.
UserModel = get_user_model()
FAKE_SCHEMA_FIELDS = [ 'name', 'delimiters', 'quotes']


class PageRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        print(args)
        print(kwargs)
        return reverse("list")


class Login(LoginView):
    template_name = "login.html"
    extra_context = {"page_title": "Login"}
    redirect_authenticated_user = True


class Logout(LogoutView):
    template_name = "registration/logout.html"


class MySchemasView(LoginRequiredMixin, ListView):
    queryset = FakeSchemas
    template_name = "schemas/list.html"

    def get_queryset(self):
        return FakeSchemas.objects.filter(author=self.request.user)


class CreateSchemaView(LoginRequiredMixin, CreateWithInlinesView):
    model = FakeSchemas
    form_class = FakeSchemaForm
    template_name = "schemas/create-edit.html"
    inlines = [FakeSchemaColumnInline]

    def get_initial(self):
        data = {"author": self.request.user}
        return data

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "submit":
                return reverse("list")
            if self.request.POST["action"] == "add_column":
                obj = self.object
                return reverse("edit", kwargs={"pk": obj.pk})

        return reverse('list')


class DeleteSchemaView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FakeSchemas
    template_name = "schemas/delete.html"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("list")

    def test_func(self):
        obj = self.get_object()

        if obj.author != self.request.user:
            return messages.error(self.request, "Not an author")

        return True


class EditSchemaView(LoginRequiredMixin, UserPassesTestMixin, UpdateWithInlinesView):
    model = FakeSchemas
    form_class = FakeSchemaForm
    template_name = "schemas/create-edit.html"
    inlines = [FakeSchemaColumnInline]

    def get_success_url(self):
        if "action" in self.request.POST:
            if self.request.POST["action"] == "submit":
                return reverse("list")
            if self.request.POST["action"] == "add_column":
                obj = self.object
                return reverse("edit", kwargs={"pk": obj.pk})

        return reverse('list')

    def test_func(self):
        obj = self.get_object()

        if obj.author != self.request.user:
            return messages.error(self.request, "Not an author")

        return True


class DataSetsView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):

    model = FakeSchemas
    form_class = ExportDatasetForm
    context_object_name = "schema"
    template_name = "schemas/datasets.html"

    def test_func(self):
        obj = self.get_object()

        if obj.author != self.request.user:
            return messages.error(self.request, "Not an author")

        return True

    def post(self, request, *args, **kwargs):
        params = (str(self.get_object().pk), request.POST["rows"])
        generate_csv_task.delay(obj=params[0], rows=params[1])
        return HttpResponseRedirect(reverse("datasets", kwargs={"pk": self.get_object().pk}))
