from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class Pojisteni(models.Model):
    typ = models.CharField(max_length=20, verbose_name="Typ pojištění")
    castka = models.CharField(max_length=20, verbose_name="Částka")
    predmet = models.CharField(max_length=20, verbose_name="Předmět pojištění")
    platnost_od = models.CharField(max_length=10, verbose_name="Platnost od")
    platnost_do = models.CharField(max_length=10, verbose_name="Platnost do")

    class Meta:
        verbose_name = "Pojištění"
        verbose_name_plural = "Pojištění"

    def __str__(self):
        return "{0} | Částka: {1} | Předmět: {2} | Platnost od: {3} | Platnost do: {4}"\
            .format(self.typ, self.castka, self.predmet, self.platnost_od, self.platnost_do)


class Pojistenec(models.Model):
    jmeno = models.CharField(max_length=20, verbose_name="Jméno")
    prijmeni = models.CharField(max_length=20, verbose_name="Příjmení")
    ulice = models.CharField(max_length=20, verbose_name="Ulice a číslo popisné")
    mesto = models.CharField(max_length=20, verbose_name="Město")
    psc = models.CharField(max_length=6, verbose_name="PSČ")
    email = models.CharField(max_length=30, verbose_name="E-mail")
    telefon = models.CharField(max_length=13, verbose_name="Telefon")
    #pojisteni = models.ForeignKey(Pojisteni, on_delete=models.SET_NULL, null=True, verbose_name="Sjednaná pojištění")
    jaka_pojisteni = models.ManyToManyField(Pojisteni)

    class Meta:
        verbose_name = "Pojištěnec"
        verbose_name_plural = "Pojištěnci"

    def __init__(self, *args, **kwargs):
        super(Pojistenec, self).__init__(*args, **kwargs)

    def __str__(self):
        insurance = [i.typ for i in self.jaka_pojisteni.all()]
        return "Jméno: {0} | Příjmení: {1} | Ulice a č. p.: {2} | Město: {3} | PSČ: {4} | E-mail: {5} | Telefon {6}" \
               "| Pojištění {7}".\
            format(self.jmeno, self.prijmeni, self.ulice, self.mesto, self.psc, self.email, self.telefon, insurance)


class UzivatelManager(BaseUserManager):
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user


class Uzivatel(AbstractBaseUser):
    email = models.EmailField(max_length=20, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"

    objects = UzivatelManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "email: {}".format(self.email)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
