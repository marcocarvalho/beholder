# -*- coding: utf-8 -*-
import scrapy

class SecretariadolistSpider(scrapy.Spider):
    name = 'secretariadolist'
    allowed_domains = ['www2.camara.leg.br']
    start_urls = ['http://www2.camara.leg.br/transparencia/recursos-humanos/servidores/lotacao/consulta-secretarios-parlamentares/layouts_transpar_quadroremuner_consultaSecretariosParlamentares']

    def parse(self, response):
        checked = response.css('#lotacao option:checked')
        if checked.extract_first() is not None:
            congressman_id = checked.xpath('@value').extract_first();
            congressman    = checked.css('::text').extract_first()
            for line in response.css('.tabela-padrao-bootstrap tbody tr'):
                arr = line.css('td::text').extract()
                yield {
                  'secretary_id': arr[0],
                  'secretary': arr[1],
                  'congressman': congressman,
                  'congressman_id': congressman_id
                }

            next_page = response.css('li.next a::attr(href)').extract_first()

            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        else:
            for option in response.css('#lotacao option'):
              congressman_id = option.xpath('@value').extract_first()
              if congressman_id == '':
                continue
              yield scrapy.FormRequest.from_response(
                  response,
                  formname='formCne',
                  formdata={'lotacao': congressman_id, 'form.button.pesquisar': 'Pesquisar', 'form.submitted': '1'},
                  callback=self.parse)
