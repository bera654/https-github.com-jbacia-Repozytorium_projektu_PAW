from django.db import models
from django.contrib.auth.models import User


MONTHS = models.IntegerChoices(
    'Miesiace',
    'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień'
)


TRANSACTION_TYPES = (
    ('S', 'Sprzedaż'),
    ('W', 'Wynajem'),
)

class PropertyType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, help_text="Krótki opis rodzaju nieruchomości.")
    typical_features = models.CharField(
        max_length=200,
        blank=True,
        help_text="Typowe cechy tego typu nieruchomości."
    )
    is_residential = models.BooleanField(default=True, help_text="Czy nieruchomość jest mieszkalna.")
    popularity_rank = models.PositiveSmallIntegerField(
        default=0,
        help_text="Ocena standardu (0–10) według użytkowników portalu."
    )

    def __str__(self):
        return self.name
    
    class Meta: 
        ordering = ["name"]


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='agent_profile')
    
    Stanowisko = (
        ('A', 'Agent nieruchomości'),
        ('D', 'Doradca sprzedaży'),
        ('O', 'Osoba prywatna' ),
        ('F', 'Firma' )
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    stanowisko = models.CharField(max_length=1, choices=Stanowisko, default="A")
    region = models.CharField(max_length=2, help_text="Kod regionu lub kraju, np. PL, DE, CZ")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta: 
        ordering = ["last_name"]


class Klient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='klient_profile')
    opiekun = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='moi_klienci')

    PLEC_WYBOR = (
        ("K", "Kobieta"),
        ("M", "Mężczyzna"),
        ("I", "Inna")
    )
    imie = models.CharField(max_length=50, blank=False, null=False)
    nazwisko = models.CharField(max_length=100, blank=False, null=False)
    plec = models.CharField(max_length=1, choices=PLEC_WYBOR, default="I")
    data_dodania = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"
    
    class Meta: 
        ordering = ["nazwisko"]


class Property(models.Model):
    title = models.CharField(max_length=100)
    listing_month = models.IntegerField(choices=MONTHS.choices, default=MONTHS.Styczeń)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES, default='S')
    
    
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    
    property_type = models.ForeignKey(PropertyType, null=True, blank=True, on_delete=models.SET_NULL)
    available_units = models.PositiveIntegerField(default=1, help_text="Liczba pokoi")
    

    square_meters = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Metraż w m²",
        null=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Cena nieruchomości (EUR) lub Miesięczny koszt wynajmu (EUR)",
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=100,
        help_text="Miasto, dzielnica, Kraj",
        null=True,
        blank=True
    )
    description = models.TextField(
        blank=True,
        help_text="Opis nieruchomości"
    )
    
    # Udogodnienia
    pool = models.BooleanField(default=True, help_text="Czy nieruchomość ma basen?")
    sauna = models.BooleanField(default=True, help_text="Czy nieruchomość ma saunę?")
    jacuzzi = models.BooleanField(default=True, help_text="Czy nieruchomość ma jacuzzi?")
    lift = models.BooleanField(default=True, help_text="Czy nieruchomość ma windę?")
    garage = models.BooleanField(default=True, help_text="Czy nieruchomość ma garaz lub prywatne miejsce parkingowe?")
    balcony = models.BooleanField(default=True, help_text="Czy nieruchomość ma balkon?")
    terrace = models.BooleanField(default=True, help_text="Czy nieruchomość ma taras?")
    garden = models.BooleanField(default=True, help_text="Czy nieruchomość ma ogród?")
    AC = models.BooleanField(default=True, help_text="Czy nieruchomość ma klimatyzacja?")
    safety_system = models.BooleanField(default=True, help_text="Czy nieruchomość ma alarm lub całodobową ochronę?")
    needs_renovation = models.BooleanField(default=True, help_text="Czy nieruchomość jest do remontu?")

    def __str__(self):
        return self.title
    
    class Meta: 
        ordering = ["title"]