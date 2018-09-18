# -*- coding: utf-8 -*-
import scrapy
import json

class CongressmanSpider(scrapy.Spider):
    name = 'congressman'
    allowed_domains = ['dadosabertos.camara.leg.br']

    def start_requests(self):
        for sex in ['M', 'F']:
            req = scrapy.Request(
                    'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo='+sex+'&itens=100&ordem=ASC&ordenarPor=nome',
                    callback=self.parse,
                    headers={'accept': 'application/json'})
            req.meta['sex'] = sex
            yield req

    def parse(self, response):
        sex   = response.meta.get('sex')
        jresp = json.loads(response.body_as_unicode())
        for congressman in jresp['dados']:
            congressman['sex'] = sex
            yield congressman

        for link in jresp['links']:
            if link['rel'] == 'next':
                req = scrapy.Request(link['href'], callback=self.parse, headers={'accept': 'application/json'})
                req.meta['sex'] = sex
                yield req
