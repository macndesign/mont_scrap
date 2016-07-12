import os
import shutil
import tempfile
from lxml import html
import requests
import datetime
from django.core import files
from django.conf import settings
from django.utils.text import slugify
from django.shortcuts import render
from .models import Auction, Lot, Images

BASE_URL = 'http://www.montenegroleiloes.com.br/'


def extract(request):
    scrap_site()
    return render(request, 'scrap/extract.html', {})


def scrap_site():
    page = requests.get(BASE_URL)
    tree = html.fromstring(page.content)

    boxes = tree.xpath('//div[@class="leilao-box"]')
    for box in boxes:
        date_kind = box.find('div[@class="data-numero"]')
        date = datetime.datetime.strptime(date_kind.find('span[1]').text, '%d/%m/%Y')
        kind = date_kind.find('span[2]').text
        desc = box.find('div[@class="info"]/div[@class="desc_lote"]/h4').text

        auction = Auction(description=desc, date=date, kind=kind)
        auction.save()
        print(auction.description)

        # Get box link
        lot_url = BASE_URL + box.find('a').attrib['href']
        lot_content = requests.get(lot_url)
        lot_tree = html.fromstring(lot_content.content)
        lot_links = lot_tree.xpath('//select[@id="navlotes"]/option/@value')

        for lot_link in lot_links:
            lot_detail_url = BASE_URL + lot_link
            lot_detail_content = requests.get(lot_detail_url)
            lot_detail_tree = html.fromstring(lot_detail_content.content)

            name = lot_detail_tree.xpath('//div[@class="coluna_detalhes"]/div/h2/span/text()')

            principal, starting_bid, minimum_increment, visits = lot_detail_tree.xpath(
                '//div[@class="coluna_detalhes"]/div/p/text()')

            situation = lot_detail_tree.xpath('//div[contains(@class, "status-lote")]/text()')

            current_bid = lot_detail_tree.xpath('//h4[text()="LANCE ATUAL"]/following::span/strong/text()')

            description = lot_detail_tree.xpath('//h2[text()="DESCRIÇÃO DO LOTE"]/following::p[1]/text()')
            if not description:
                description = lot_detail_tree.xpath('//div[contains(@class, "row-descricao")]/text()')

            insurance = lot_detail_tree.xpath('//h2[text()="DESCRIÇÃO DO LOTE"]/following::p[1]/b/text()')

            lot = Lot(name=name[0].strip() if name else '',
                      starting_bid=starting_bid.replace('R$', '').strip().replace('.', '').replace(',', '.'),
                      minimum_increment=minimum_increment.replace('R$', '').strip().replace('.', '').replace(',', '.'),
                      current_bid=current_bid[0].strip().replace('.', '').replace(',', '.') if current_bid else '0.0',
                      description=description[0].strip() if description else '',
                      situation=situation[0].strip() if situation else '',
                      insurance=True if insurance else False)

            lot.save()
            print(lot.description)

            images_url = lot_detail_tree.xpath('//div[@class="coluna_esquerda"]/a/@href')
            if images_url:
                images_content = requests.get(BASE_URL + images_url[0])
                images_tree = html.fromstring(images_content.content)
                images_links = images_tree.xpath('//a/@href')
                image_urls = [BASE_URL + link for link in images_links]

                auction.lot_set.add(lot)

                for image_url in image_urls:
                    request = requests.get(image_url, stream=True)

                    if request.status_code != requests.codes.ok:
                        continue

                    file_name = '{}-{}-{}-{}-{}'.format(slugify(
                        principal.strip()),
                        date.year, date.month, date.day,
                        image_url.split('/')[-1])

                    lf = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break

                        lf.write(block)

                    image = Images()
                    image.image.save(file_name, files.File(lf))
                    lot.images_set.add(image)
