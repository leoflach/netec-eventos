"""Gera o conteúdo HTML (sem <script>/<style>) para a página do WordPress do NETEC
a partir de eventos.json. Uso: python3 gerar_wp.py [AAAA-MM-DD]"""
import json, sys, html, datetime as dt

d = json.load(open('eventos.json'))
hoje = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
P = lambda s: dt.date.fromisoformat(s) if s else None
f = lambda x: x.strftime('%d/%m/%Y')
E = html.escape

def rng(a, b):
    if a and b:
        if a == b: return f(a)
        if (a.year, a.month) == (b.year, b.month): return f"{a.day:02d}–{f(b)}"
        return f"{f(a)} a {f(b)}"
    if b: return "Até " + f(b)
    if a: return "A partir de " + f(a)
    return ""

for e in d['eventos']:
    e['_ei'], e['_ef'], e['_si'], e['_sf'] = P(e['ev_ini']), P(e['ev_fim']), P(e['sub_ini']), P(e['sub_fim'])
    e['_ev'] = rng(e['_ei'], e['_ef']) or e['ev_txt'] or 'A confirmar'
    st = rng(e['_si'], e['_sf'])
    e['_sub'] = st or e['sub_txt'] or 'Consultar site'
    if st and e['sub_txt'] and (not e['_sf'] or f(e['_sf']) not in e['sub_txt']): e['_sub'] += ' · ' + e['sub_txt']

def key(e):
    if not e['_ei']: return (2, dt.date.max, e['nome'])
    passado = (e['_ef'] or e['_ei']) < hoje
    return (1 if passado else 0, e['_ei'] if not passado else dt.date(9999,1,1) - (e['_ei'] - dt.date(2000,1,1)), e['nome'])

C = {'brand': '#14325c', 'b2': '#1f6f8b', 'line': '#e3e6ec', 'muted': '#5c6577', 'acc': '#e0a423'}
TH = f"background:{C['brand']};color:#fff"
TD = ""

def tabela(lista):
    h = [f'<div style="overflow-x:auto"><table class="netec-eventos" style="width:100%" border="1" cellpadding="6">',
         '<thead><tr>' + ''.join(f'<th style="{TH}">{c}</th>' for c in
         ['Evento', 'Âmbito', 'Site', 'Periodicidade', 'Local (cidade · país)', 'Período de submissão', 'Período do evento', 'Ano']) + '</tr></thead><tbody>']
    for e in sorted(lista, key=key):
        situ = ''
        if e['_ei']:
            fim = e['_ef'] or e['_ei']
            if fim < hoje: situ = ' <em style="color:#6b7280">(realizado)</em>'
        ast = ' <span title="Informação a confirmar no site oficial" style="color:#9a6400">*</span>' if e.get('confirmado') is False else ''
        sub = [E(e['sigla'])] + ([E(e['edicao'])] if e['edicao'] else []) + [E(e['area'])]
        obs = f'<br><small>{E(e["obs"])}</small>' if e['obs'] else ''
        h.append('<tr>'
                 f'<td><strong>{E(e["nome"])}</strong>{ast}<br><small>{" · ".join(sub)}</small>{obs}</td>'
                 f'<td>{E(e["ambito"])}</td>'
                 f'<td><a href="{E(e["site"])}" target="_blank" rel="noopener">Acessar</a></td>'
                 f'<td>{E(e["periodicidade"])}</td>'
                 f'<td>{E(e["cidade"])} · {E(e["pais"])}</td>'
                 f'<td>{E(e["_sub"])}</td>'
                 f'<td>{E(e["_ev"])}{situ}</td>'
                 f'<td>{e["ano"]}</td></tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)

ev = d['eventos']
nac = [e for e in ev if e['ambito'] == 'Nacional']
inter = [e for e in ev if e['ambito'] == 'Internacional']
abertos = sorted([e for e in ev if e['_sf'] and e['_sf'] >= hoje and (not e['_si'] or e['_si'] <= hoje)], key=lambda e: e['_sf'])
proximos = sorted([e for e in ev if e['_ei'] and (e['_ef'] or e['_ei']) >= hoje and (e['_ei'] - hoje).days <= 90], key=lambda e: e['_ei'])
paises = {e['pais'] for e in ev if 'confirmar' not in e['pais'].lower()}

card = f"display:inline-block;min-width:150px;margin:0 8px 8px 0;padding:12px 14px;border:1px solid {C['line']};border-radius:10px;background:#fff;vertical-align:top"
def kpi(n, t): return f'<div style="{card}"><div style="font-size:26px;font-weight:700;color:{C["brand"]}">{n}</div><div style="font-size:13px;color:{C["muted"]}">{t}</div></div>'

out = []
P_ = 'style="margin:0 0 14px"'
out.append(f'<p {P_}>Painel do Grupo de Pesquisa <strong>NETEC/UFSC</strong> com os principais <strong>congressos e eventos científicos de Administração, Contabilidade, Finanças e Administração Pública</strong>, nacionais e internacionais. Para cada evento: site oficial, periodicidade, local (cidade e país), período de submissão de trabalhos, período de realização e ano da edição.</p>')
out.append(f'<p {P_}>Base com <strong>{len(ev)} eventos</strong> ({len(nac)} nacionais e {len(inter)} internacionais), revisada periodicamente a partir dos sites oficiais. Última atualização: <strong>{f(dt.date.fromisoformat(d["atualizado_em"]))}</strong>. Confira sempre o site oficial antes de submeter.</p>')
out.append('<h2 id="painel" style="margin:28px 0 10px">Painel interativo</h2>')
out.append(f'<p {P_}>Busque por nome, sigla, cidade ou país; filtre por âmbito, área, situação e submissões abertas; alterne entre tabela, cartões e calendário. <a href="https://leoflach.github.io/netec-eventos/" target="_blank" rel="noopener">Abrir o painel em tela cheia</a>.</p>')
out.append('<iframe src="https://leoflach.github.io/netec-eventos/" width="100%" height="1150" frameborder="0" title="Painel interativo de eventos científicos NETEC"></iframe>')
out.append(f'<h2 id="lista" style="margin:32px 0 10px">Lista completa de eventos</h2>')
out.append(f'<p {P_}>Ir para: <a href="#nacionais">Congressos nacionais</a> · <a href="#internacionais">Congressos internacionais</a> · <a href="#sobre">Sobre este painel</a></p>')
out.append(f'<h3 id="nacionais" style="margin:24px 0 10px">Congressos nacionais ({len(nac)})</h3>')
out.append(tabela(nac))
out.append(f'<h3 id="internacionais" style="margin:28px 0 10px">Congressos internacionais ({len(inter)})</h3>')
out.append(tabela(inter))
out.append('<h2 id="sobre" style="margin:32px 0 10px">Sobre este painel</h2>')
out.append(f'<p {P_}><strong>Critério de âmbito.</strong> {E(d["criterio_ambito"])}</p>')
out.append(f'<p {P_}>Para cada evento aparece a edição mais recente com datas e local divulgados; quando a próxima edição ainda não foi anunciada, isso é indicado nas observações. Itens marcados com <span style="color:#9a6400">*</span> têm informações a confirmar.</p>')
out.append(f'<p {P_}><strong>Fontes:</strong> {E(d.get("fontes",""))} Dados abertos em <a href="https://github.com/leoflach/netec-eventos" target="_blank" rel="noopener">github.com/leoflach/netec-eventos</a>.</p>')
out.append(f'<p {P_}>Sentiu falta de algum evento ou encontrou uma data errada? Escreva para o NETEC.</p>')
open('wp_conteudo.html', 'w').write('\n'.join(out))
print(len('\n'.join(out)), 'chars;', len(abertos), 'abertos;', len(proximos), 'proximos')
