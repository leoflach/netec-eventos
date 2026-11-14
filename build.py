"""Gera index.html (painel interativo, com os dados embutidos como reserva) e wp_conteudo.html a partir de eventos.json."""
import json, subprocess, sys
d = json.load(open('eventos.json'))
s = json.dumps(d, ensure_ascii=False).replace('</', '<\\/')
open('index.html', 'w').write(open('template.html').read().replace('__DATA__', s))
subprocess.run([sys.executable, 'gerar_wp.py'] + sys.argv[1:], check=True)
import re
sm=open('sitemap.xml').read(); sm=re.sub(r'<lastmod>[^<]*</lastmod>', '<lastmod>'+d['atualizado_em']+'</lastmod>', sm); open('sitemap.xml','w').write(sm)
print('ok:', len(d['eventos']), 'eventos')
