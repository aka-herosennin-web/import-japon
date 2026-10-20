import os, json, urllib.parse, urllib.request, html, pathlib, datetime, re, sys
ROOT=pathlib.Path(__file__).parent; OUT=ROOT/'site'; OUT.mkdir(exist_ok=True)
AFF='971294'
API='https://www.play-asia.com/l402/v1/catalog'
SEARCHES=['japan region only','japan psn','japan eshop','japan time card','japanese yen','japan nintendo']
HEAD={'User-Agent':'ImportGamesCatalog/0.1 (small independent affiliate site)','Accept':'application/json'}

def fetch(q):
    params=urllib.parse.urlencode({'q':q,'limit':100,'currency':'EUR','affiliate_id':AFF})
    req=urllib.request.Request(API+'?'+params,headers=HEAD)
    with urllib.request.urlopen(req,timeout=22) as resp: return json.load(resp).get('products',[])

def safe(x):return html.escape(str(x or ''),quote=True)
def is_aff_url(url):
    try:
        u=urllib.parse.urlsplit(url)
        return u.scheme=='https' and u.hostname in ('www.play-asia.com','play-asia.com') and urllib.parse.parse_qs(u.query).get('tagid')==[AFF]
    except: return False

def keep(p):
    name=str(p.get('name','')).lower(); plat=str(p.get('platform','')).lower(); version=str(p.get('version_code','')).upper()
    return (version=='JP' or 'japan region only' in name or 'japanese account' in name or 'japan account' in name) and (not any(z in name for z in ['buffalo','restaurant','gift card 10 usd'])) and is_aff_url(p.get('url','')) and p.get('in_stock')==1 and bool(p.get('pax'))

def display(p):
    n=safe(p.get('name')); url=safe(p.get('url')); price=p.get('price') or {}; eur=price.get('eur'); pr=f'{float(eur):.2f} €'.replace('.',',') if isinstance(eur,(int,float)) else 'Voir le tarif actuel'
    platform=safe(p.get('platform') or 'Plateforme non renseignée'); ver=safe(p.get('version_code') or 'Non indiquée')
    # Deliberately do not display images before permission is confirmed.
    return f'<article class="product"><div class="product-top"><span class="chip">Région : {ver}</span><span class="stock">Disponible selon le catalogue</span></div><h2>{n}</h2><p class="sub">{platform}</p><div class="bottom"><strong>{pr}</strong><a class="btn" target="_blank" rel="sponsored nofollow noopener noreferrer" href="{url}">Voir chez Play-Asia ↗</a></div><p class="fine">Vérifiez la région du compte et les langues sur la fiche du vendeur avant achat.</p></article>'

def page(products, updated, test=False):
    cards=''.join(display(x) for x in products) if products else '<div class="empty">Aucun produit japonais disponible dans notre sélection. Le catalogue sera actualisé lors du prochain relevé.</div>'
    opts=''.join('<option>'+safe(x)+'</option>' for x in sorted(set(p.get('platform') or 'Autre' for p in products)))
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="Sélection de jeux et cartes numériques pour comptes japonais, avec région et prix indicatifs. Vérifiez la compatibilité avant achat."><title>Import Japon — Sélection jeux et cartes</title><style>
:root{{--bg:#0b1020;--card:#151d32;--text:#f4f6fa;--muted:#aab4c7;--edge:#2a3651;--pink:#fc627d}}*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 50% -10%,#263251,#0b1020 60%);font:16px/1.55 system-ui,sans-serif;color:var(--text)}}.wrap{{max-width:1160px;margin:auto;padding:0 24px}}header{{border-bottom:1px solid var(--edge);background:#0a1020b8}}header .wrap{{padding:20px 24px;display:flex;align-items:center;justify-content:space-between}}.logo{{font-weight:850;letter-spacing:.04em}}.logo span{{color:var(--pink)}}.eyebrow{{text-transform:uppercase;font-size:.72rem;letter-spacing:.16em;color:#ff9aaf}}.hero{{padding:65px 0 35px}}h1{{font-size:clamp(2.1rem,5vw,4rem);line-height:1.12;margin:12px 0;max-width:760px}}.intro{{color:var(--muted);max-width:720px}}.warning{{border:1px solid #605039;background:#322717;padding:14px 18px;border-radius:12px;color:#ffe1b0;margin:20px 0 32px}}.tools{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:20px}}input,select{{font:inherit;background:var(--card);border:1px solid var(--edge);border-radius:10px;color:var(--text);padding:11px 12px;min-width:170px}}input{{flex:1}}.count{{color:var(--muted);margin:8px 0 18px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(275px,1fr));gap:16px;margin:0 0 50px}}.product{{border:1px solid var(--edge);background:linear-gradient(145deg,#1a243d,#10182b);border-radius:17px;padding:20px;display:flex;flex-direction:column;min-height:255px}}.product-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:9px}}.chip{{background:#30314c;color:#e3d6ff;padding:4px 8px;border-radius:6px;font-size:.75rem}}.stock{{font-size:.7rem;color:#86efac;text-align:right}}h2{{font-size:1.11rem;line-height:1.35;margin:20px 0 5px}}.sub{{color:var(--muted);margin:0 0 12px}}.bottom{{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:12px}}strong{{font-size:1.35rem}}.btn{{background:var(--pink);color:#170a13;text-decoration:none;font-weight:750;border-radius:9px;padding:9px 12px;text-align:center;font-size:.86rem}}.fine{{color:var(--muted);font-size:.76rem;margin:12px 0 0}}footer{{border-top:1px solid var(--edge);padding:25px 0 50px;color:var(--muted);font-size:.88rem}}footer p{{max-width:800px}}.empty{{padding:28px;background:var(--card);border-radius:12px;color:var(--muted)}}@media(max-width:550px){{.bottom{{flex-wrap:wrap}}.btn{{width:100%}}}}
</style></head><body><header><div class="wrap"><div class="logo">IMPORT<span>JAPON</span></div><span style="color:var(--muted);font-size:.82rem">Sélection indépendante</span></div></header><main class="wrap"><section class="hero"><div class="eyebrow">Jeux & cartes numériques · Comptes japonais</div><h1>Les éditions japonaises, sans mauvaises surprises.</h1><p class="intro">Un catalogue restreint de produits numériques associés au Japon. Prix relevés automatiquement, lien direct vers le vendeur et indication explicite de région. La présence d'un produit ici ne garantit pas sa compatibilité avec votre compte.</p></section><div class="warning">⚠️ <b>Important :</b> une carte ou un code de région JP peut nécessiter un compte japonais. Vérifiez les restrictions, la langue, la plateforme et les conditions de remboursement chez Play-Asia avant toute commande.</div><div class="tools"><input id="search" type="search" placeholder="Rechercher un produit…" aria-label="Rechercher un produit"><select id="platform"><option value="">Toutes les plateformes</option>{opts}</select></div><p id="count" class="count">{len(products)} produits · Dernière actualisation : {safe(updated)}{' · Aperçu simulé' if test else ''}</p><div class="grid" id="grid">{cards}</div></main><footer><div class="wrap"><p><b>Transparence :</b> certains liens sont affiliés : une commande éligible peut nous rapporter une commission sans surcoût pour vous.</p><p>Site indépendant non officiel, non exploité par Play-Asia, Nintendo, Sony ou les éditeurs mentionnés. Les informations de catalogue et prix peuvent évoluer ; la fiche du vendeur fait foi.</p><p>Images non affichées en attendant la confirmation des droits de réutilisation. Ce site de démonstration reste en <b>noindex</b> jusqu'à validation des informations légales et commerciales.</p></div></footer><script>let s=document.querySelector('#search'),p=document.querySelector('#platform'),g=document.querySelector('#grid');function filter(){{let q=s.value.toLocaleLowerCase('fr'),v=p.value,n=0;for(let e of g.querySelectorAll('.product')){{let ok=e.innerText.toLocaleLowerCase('fr').includes(q)&&(!v||e.querySelector('.sub').innerText===v);e.hidden=!ok;if(ok)n++}}document.querySelector('#count').textContent=n+' produit(s) affiché(s) · Actualisé : {safe(updated)}'}}s.addEventListener('input',filter);p.addEventListener('change',filter);</script></body></html>'''

def main():
    test='--demo' in sys.argv
    if test:
        products=[{'pax':'PAX0007244040','name':'Final Fantasy XIV Online 30-Day Time Card (Japan Region Only)','platform':'PC','version_code':'JP','price':{'eur':11.49},'in_stock':1,'url':'https://www.play-asia.com/fr/final-fantasy-xiv-online-30--day-time-card-japan-region-only/13/7094s7?tagid=971294'}]
    else:
        data={}; successes=0
        for term in SEARCHES:
            try:
                rows=fetch(term);successes+=1
                print(f'{term}: {len(rows)} retournés')
                for p in rows:
                    if keep(p):data[p['pax']]=p
            except Exception as e:print(f'{term}: erreur {e}',file=sys.stderr)
        if successes==0:raise SystemExit('Aucun appel API réussi : publication inchangée')
        products=list(data.values())[:30]
        if not products:raise SystemExit('Aucun produit pertinent : publication inchangée')
    now=datetime.datetime.now(datetime.timezone.utc).strftime('%d/%m/%Y %H:%M UTC')
    (OUT/'index.html').write_text(page(products,now,test),encoding='utf-8')
    print('Site généré :',len(products),'produit(s)')
if __name__=='__main__':main()
