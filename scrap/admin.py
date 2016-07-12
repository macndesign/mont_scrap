from django.contrib import admin
from django.template.defaultfilters import truncatewords
from .models import Auction, Lot, Images


class LotInline(admin.TabularInline):
    model = Lot
    readonly_fields = ('name', 'lot_detail', 'situation', 'description', 'starting_bid', 'minimum_increment')

    def lot_detail(self, obj):
        return '<a class="default" href="/admin/scrap/lot/%s/change/">Detail</a>' % obj.pk

    lot_detail.allow_tags = True


class AuctionAdmin(admin.ModelAdmin):
    model = Auction
    list_filter = ('kind', 'date')
    list_display = ('description', 'kind', 'date')
    inlines = [
        LotInline,
    ]


class ImagesInline(admin.TabularInline):
    model = Images
    readonly_fields = ('admin_image',)

    def admin_image(self, obj):
        return '<img src="%s"/>' % obj.image.url

    admin_image.allow_tags = True


class LotAdmin(admin.ModelAdmin):
    model = Lot
    search_fields = ('name', 'description')
    list_display = ('name_without_lot', 'truncate_description')
    list_filter = ('auction', 'insurance', 'situation')
    inlines = [
        ImagesInline,
    ]

    def truncate_description(self, obj):
        return truncatewords(obj.description, 50)

    truncate_description.short_description = 'description'

    def name_without_lot(self, obj):
        return obj.name.lower().replace('lote', '').strip()

    name_without_lot.short_description = 'lot'


class ImagesAdmin(admin.ModelAdmin):
    model = Images
    list_display = ('admin_image', 'image')

    def admin_image(self, obj):
        return '<img src="%s"/>' % obj.image.url

    admin_image.allow_tags = True


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Lot, LotAdmin)
admin.site.register(Images, ImagesAdmin)
