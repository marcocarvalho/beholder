# -*- coding: utf-8 -*-
import scrapy
import datetime
import json

class SecretariadoinfoSpider(scrapy.Spider):
    name = 'secretariadoinfo'
    allowed_domains = ['www2.camara.leg.br']

    # period in format YYYYMM
    def __init__(self, list=None, file=None, period=None, *args, **kwargs):
        self.period = period
        if list is not None and file is None:
            self.list = list
        elif file is not None:
            self.list = self.parse_secretary_file(file)

        super(SecretariadoinfoSpider, self).__init__(*args, **kwargs)

    def parse_secretary_file(self, file):
        return json.load(open(file, 'r'))

    def start_requests(self):
        last_month = self.last_month()
        if self.list is not None:
            for item in self.list:
                secretary    = item.get('secretary')
                secretary_id = item.get('secretary_id')
                req = scrapy.FormRequest(
                    'http://www2.camara.leg.br/transpnet/consulta',
                    formdata={'periodoFolha': last_month, 'nome': secretary},
                    callback=self.parse)
                req.meta['secretary_id']    = secretary_id
                req.meta['secretary']       = secretary
                req.meta['reference_month'] = last_month
                yield req

    def last_month(self):
        today = datetime.date.today()
        first = today.replace(day=1)
        lastMonth = first - datetime.timedelta(days=1)
        return lastMonth.strftime("%Y%m")

    def parse(self, response):
        secretary    = response.meta.get('secretary')
        secretary_id = response.meta.get('secretary_id')
        last_month   = response.meta.get('last_month')

        if secretary is None:
            yield {
                'secretary_id': secretary_id,
                'secretary': response.css('#content h3::text').extract_first(),
                'relationship': response.xpath("//table[@summary='Dados do Servidor']/tr[1]/td[1]/text()[2]").extract_first().rstrip(),
                'position': response.xpath("//table[@summary='Dados do Servidor']/tr[1]/td[3]/text()[2]").extract_first().strip(),
                'level': response.xpath("//table[@summary='Dados do Servidor']/tr[1]/td[4]/text()[2]").extract_first().strip(),
                'since': response.xpath("//table[@summary='Dados do Servidor']/tr[1]/td[2]/text()[2]").extract_first().strip(),
                'gross_salary': response.xpath("//table[@summary='Remunerações']/tbody/tr[5]/td[2]/text()").extract_first().strip().replace(',', ''),
                'net_salary': response.xpath("//table[@summary='Remunerações']/tbody/tr[16]/td[2]/text()").extract_first().strip().replace(',', '')
            }
        else:
            href = response.xpath("//a[contains(text(),\""+secretary+"\")]/@href").extract_first()
            if href is not None:
                req = response.follow(href, callback=self.parse)
                req.meta['secretary_id']    = secretary_id
                req.meta['reference_month'] = last_month
                yield req
