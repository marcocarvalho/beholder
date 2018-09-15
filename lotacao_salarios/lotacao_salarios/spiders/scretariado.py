# -*- coding: utf-8 -*-
import scrapy


class ScretariadoSpider(scrapy.Spider):
    name = 'scretariado'
    allowed_domains = ['http://www2.camara.leg.br/transparencia/recursos-humanos/servidores/lotacao/consulta-secretarios-parlamentares/layouts_transpar_quadroremuner_consultaSecretariosParlamentares']
    start_urls = ['http://http://www2.camara.leg.br/transparencia/recursos-humanos/servidores/lotacao/consulta-secretarios-parlamentares/layouts_transpar_quadroremuner_consultaSecretariosParlamentares/']

    def parse(self, response):
        pass
