from django.db import models


class Auction(models.Model):
    description = models.CharField(max_length=120)
    kind = models.CharField(max_length=75, blank=True)
    date = models.DateTimeField()

    class Meta:
        unique_together = ("description", "date")

    def __str__(self):
        return '{} - {}'.format(self.description, self.date.strftime('%d/%m/%Y'))


class Lot(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2)
    minimum_increment = models.DecimalField(max_digits=12, decimal_places=2)
    current_bid = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    description = models.TextField()
    situation = models.CharField(max_length=120)
    insurance = models.BooleanField(default=False)
    auction = models.ForeignKey('Auction', blank=True, null=True)

    def __str__(self):
        return self.description


class Images(models.Model):
    image = models.ImageField(upload_to='images')
    lot = models.ForeignKey('Lot', blank=True, null=True)

    def __str__(self):
        return '{} - {} - {}'.format(
            self.image.name,
            self.lot.description,
            self.lot.auction.description
        )
