# Eventos científicos em Administração e Contabilidade · NETEC/UFSC

Painel com congressos nacionais e internacionais da área: nome, âmbito, site, periodicidade, local, período de submissão, período do evento e ano.

- Painel interativo: https://leoflach.github.io/netec-eventos/
- Página no site do grupo: https://netec.paginas.ufsc.br/eventos-cientificos/
- Dados abertos: [`eventos.json`](eventos.json)

## Como atualizar
1. Edite `eventos.json` (um objeto por evento; datas no formato `AAAA-MM-DD`; deixe vazio o que não foi divulgado e explique em `sub_txt`/`ev_txt`).
2. Atualize `atualizado_em`.
3. Rode `python3 build.py` para regenerar `index.html` (painel) e `wp_conteudo.html` (conteúdo em HTML simples para colar na página do WordPress, aba "Texto").

Campos: `nome, sigla, ambito (Nacional|Internacional), area, site, periodicidade, cidade, pais, sub_ini, sub_fim, sub_txt, ev_ini, ev_fim, ev_txt, ano, edicao, obs, confirmado`.

Critério de âmbito: Nacional = organizado e realizado no Brasil; Internacional = associação estrangeira/internacional ou realizado fora do Brasil.
