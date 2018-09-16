Objetivo
--------
Coletar as informações de salário e posição dos comissionados da camara dos deputados para cruzamento de dados, análise e estatística.

Rodando
-------

```
  docker-compose run -it --rm scrapy sh
  scrapy crawl secretariadolist -o secretariado.json -t json
  scrapy crawl secretariadoinfo -a file=secretariado.json -o secretariado_info.json -t json
```

TODO
----

- [ ] Identificar o sexo dos comissionados
- [ ] download da informação dos parlamentares (partido, sexo)
- [ ] cruzamento dos dados
- [ ] paginas web estáticas
- [ ] gráficos
- [ ] publicação
