from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import Pojistenec, Uzivatel, Pojisteni
from .forms import PojistenecForm, UzivatelForm, LoginForm, PojisteniForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class PojistenecIndex(generic.ListView):

    template_name = "pojisteni/pojistenec_index.html"
    context_object_name = "pojisteni"

    def get_queryset(self):
        return Pojistenec.objects.all().order_by("-id")


class PojisteniIndex(generic.ListView):

    template_name = "pojisteni/pojisteni_index.html"
    context_object_name = "pojisteni"

    def get_queryset(self):
        return Pojisteni.objects.all().order_by("-id")


class DetailPojistenceView(generic.DetailView):

    model = Pojistenec
    template_name = "pojisteni/pojistenec_detail.html"

    def get(self, request, pk):
        try:
            pojistenec = self.get_object()
        except:
            return redirect("pojistenec_index")
        return render(request, self.template_name, {"pojistenec": pojistenec})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if "create" in request.POST:
                return redirect("pridej_pojisteni")
            elif "edit" in request.POST:
                return redirect("edit_pojistenec", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Nemáš práva pro smazání pojištěnce.")
                    return redirect(reverse("pojistenec_index"))
                else:
                    self.get_object().delete()
        return redirect(reverse("pojistenec_index"))


class DetailPojisteniView(generic.DetailView):

    model = Pojisteni
    template_name = "pojisteni/pojisteni_detail.html"

    def get(self, request, pk):
        try:
            pojisteni = self.get_object()
        except:
            return redirect("pojistenec_index")
        return render(request, self.template_name, {"pojisteni": pojisteni})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_pojisteni", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Nemáš práva pro smazání pojištění.")
                    return redirect(reverse("pojistenec_index"))
                else:
                    self.get_object().delete()
        return redirect(reverse("pojistenec_index"))


class EditPojistenec(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = "pojisteni/vytvor_pojistence.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu pojištěnce.")
            return redirect(reverse("pojistenec_index"))
        try:
            pojistenec = Pojistenec.objects.get(pk=pk)
        except:
            messages.error(request, "Tento pojištěnec neexistuje.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(instance=pojistenec)
        return render(request, self.template_name, {"form": form})

    def post (self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu pojištěnce.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(request.POST)

        if form.is_valid():
            jmeno = form.cleaned_data["jmeno"]
            prijmeni = form.cleaned_data["prijmeni"]
            ulice = form.cleaned_data["ulice"]
            mesto = form.cleaned_data["mesto"]
            psc = form.cleaned_data["psc"]
            email = form.cleaned_data["email"]
            telefon = form.cleaned_data["telefon"]
            jaka_pojisteni = form.cleaned_data["jaka_pojisteni"]
            try:
                pojistenec = Pojistenec.objects.get(pk=pk)
            except:
                messages.error(request, "Tento pojištěnec neexistuje.")
                return redirect(reverse("pojistenec_index"))
            pojistenec.jmeno = jmeno
            pojistenec.prijmeni = prijmeni
            pojistenec.ulice = ulice
            pojistenec.mesto = mesto
            pojistenec.psc = psc
            pojistenec.email = email
            pojistenec.telefon = telefon
            pojistenec.jaka_pojisteni.set(jaka_pojisteni)
            pojistenec.save()
            return redirect("pojistenec_detail", pk=pojistenec.id)
        return render(request, self.template_name, {"form": form})


class VytvorPojisteni(LoginRequiredMixin, generic.edit.CreateView):

    form_class = PojisteniForm
    template_name = "pojisteni/vytvor_pojisteni.html"

    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání pojištění.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání pojištění.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("pojistenec_index")
        return render(request, self.template_name, {"form": form})


class VytvorPojistence(LoginRequiredMixin, generic.edit.CreateView):

    form_class = PojistenecForm
    template_name = "pojisteni/vytvor_pojistence.html"

    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání pojištěnce.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání pojištěnce.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("pojistenec_index")
        return render(request, self.template_name, {"form": form})


class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = "pojisteni/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("pojistenec_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            uzivatel = form.save(commit=False)
            password = form.cleaned_data["password"]
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect("pojistenec_index")

        return render(request, self.template_name, {"form": form})


class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "pojisteni/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("pojistenec_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return render(redirect(reverse("pojistenec_index")))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("pojistenec_index")
            else:
                messages.error(request, "Tento účet neexistuje.")
        return render(request, self.template_name, {"form": form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "Nemůžeš se odhlášit, pokud nejsi přihlášený.")
    return redirect(reverse("login"))


class Home(generic.TemplateView):

    template_name = "pojisteni/home.html"
    context_object_name = "home"
