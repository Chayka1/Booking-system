from django.db import models

class Position(models.Model):
    title = models.CharField(max_length=50, verbose_name="Назва посади")

    class Meta:
        verbose_name = "Посада"
        verbose_name_plural = "Посади"

    def __str__(self):
        return self.title

class Barber(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я майстра")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Посада")
    services = models.ManyToManyField('Service', through='BarberService', verbose_name="Послуги")
    is_active_today = models.BooleanField(default=True, verbose_name="Активний сьогодні")

    class Meta:
        verbose_name = "Майстер"
        verbose_name_plural = "Майстри"

    def __str__(self):
        return f"{self.name} ({self.position.title})"

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва послуги")
    description = models.TextField(verbose_name="Опис послуги", blank=True, null=True)

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"

    def __str__(self):
        return self.name

class BarberService(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, verbose_name="Майстер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Послуга")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    class Meta:
        verbose_name = "Послуга майстра"
        verbose_name_plural = "Послуги майстрів"

    def __str__(self):
        return f"{self.barber.name} - {self.service.name} ({self.price} грн)"

class BarberSchedule(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, verbose_name="Майстер")
    day_of_week = models.CharField(
        max_length=1,
        choices=[
            ('0', 'Понеділок'),
            ('1', 'Вівторок'),
            ('2', 'Середа'),
            ('3', 'Четвер'),
            ('4', 'П’ятниця'),
            ('5', 'Субота'),
            ('6', 'Неділя'),
        ],
        verbose_name="День тижня"
    )
    start_time = models.TimeField(verbose_name="Початок роботи")
    end_time = models.TimeField(verbose_name="Кінець роботи")

    class Meta:
        verbose_name = "Розклад майстра"
        verbose_name_plural = "Розклади майстрів"

    def __str__(self):
        return f"{self.barber} — {self.day_of_week} ({self.start_time}-{self.end_time})"

class Booking(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ім’я клієнта")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище клієнта")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, verbose_name="Майстер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Послуга")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Час")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна", null=True, blank=True)

    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.barber.name} ({self.service.name})"
