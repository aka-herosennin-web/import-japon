import os, json, urllib.parse, urllib.request, html, pathlib, datetime, re, sys
ROOT=pathlib.Path(__file__).parent; OUT=ROOT/'site'; OUT.mkdir(exist_ok=True)
AFF='971294'
# Les images proviennent de l'API Play-Asia : activer seulement si leur usage est autorisé.
SHOW_COVERS=True
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

def kind(p):
    n=str(p.get('name','')).lower()
    if any(v in n for v in ('eshop','nintendo','switch online')): return 'Nintendo eShop'
    if any(v in n for v in ('psn','playstation','ps plus')): return 'PlayStation / PSN'
    if any(v in n for v in ('time card','prepaid','subscription','xiv online')): return 'Abonnements'
    return 'Autres codes japonais'

def display(p):
    n=safe(p.get('name')); url=safe(p.get('url')); price=p.get('price') or {}; eur=price.get('eur')
    pr=f'{float(eur):.2f} €'.replace('.',',') if isinstance(eur,(int,float)) else 'Voir le tarif actuel'
    platform=safe(p.get('platform') or 'Plateforme non renseignée'); ver=safe(p.get('version_code') or 'Non indiquée'); group=safe(kind(p))
    img_url = p.get('image_url') or ''
    img = ('<img src="'+safe(img_url)+'" alt="Jaquette ou visuel produit : '+n+'" loading="lazy" referrerpolicy="no-referrer" onerror="this.hidden=true">') if SHOW_COVERS and str(img_url).startswith('https://s.pacn.ws/') else ''
    return f'''<article class="product" data-kind="{group}"><div class="product-top"><span class="chip">Région : {ver}</span><span class="stock">● En stock*</span></div><div class="visual" aria-hidden="true"><span class="visual-label">{group}</span>{img}<span class="visual-ideogram">日本</span><span class="visual-platform">{platform}</span></div><div class="product-copy"><p class="category">{group} · {platform}</p><h2>{n}</h2><div class="bottom"><div><small>Prix indicatif</small><strong>{pr}</strong></div><a class="btn" target="_blank" rel="sponsored nofollow noopener noreferrer" href="{url}">Voir sur Play-Asia ↗</a></div><p class="fine">*Données lors du dernier relevé. Vérifiez région d'activation, langues et conditions chez le vendeur.</p></div></article>'''

def page(products, updated, test=False):
    cards=''.join(display(x) for x in products) if products else '<div class="empty">Aucun produit japonais disponible dans notre sélection. Le catalogue sera actualisé lors du prochain relevé.</div>'
    opts=''.join('<option>'+safe(x)+'</option>' for x in sorted(set(kind(p) for p in products)))
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="Sélection de jeux et cartes numériques pour comptes japonais, avec région et prix indicatifs. Vérifiez la compatibilité avant achat."><title>Import Japon — Sélection jeux et cartes</title><style>

:root{{--bg:#090e1b;--card:#172036;--text:#f7f7fc;--muted:#aeb9d0;--edge:#33405b;--pink:#ff7791;--mint:#80e7b5}}*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:radial-gradient(ellipse at 85% -5%,#402c65 0,transparent 44%),radial-gradient(ellipse at 0 8%,#203d5d 0,transparent 42%),var(--bg);font:15px/1.6 system-ui,sans-serif;color:var(--text)}}.wrap{{max-width:1200px;margin:auto;padding:0 24px}}header{{border-bottom:1px solid #ffffff1a;background:#080e1bc9;backdrop-filter:blur(12px)}}header .wrap{{padding:20px 24px;display:flex;align-items:center;justify-content:space-between}}.logo{{font-weight:900;letter-spacing:.055em;font-size:1.12rem}}.logo span{{color:var(--pink)}}.eyebrow{{text-transform:uppercase;font-size:.74rem;letter-spacing:.16em;color:#ffadbc;font-weight:700}}.hero{{padding:82px 0 38px}}h1{{font-size:clamp(2.5rem,5.5vw,5rem);line-height:1.08;margin:15px 0 22px;max-width:850px;letter-spacing:-.05em}}.intro{{color:var(--muted);max-width:690px;font-size:1.07rem;line-height:1.85}}.warning{{border:1px solid #987448;background:#342718c9;padding:17px 20px;border-radius:15px;color:#ffe5b8;margin:20px 0 38px}}.tools{{display:grid;grid-template-columns:1fr 260px;gap:12px;margin-bottom:20px}}input,select{{font:inherit;background:#152039;border:1px solid #374562;border-radius:11px;color:var(--text);padding:14px;min-width:0}}input:focus,select:focus{{outline:2px solid var(--pink);outline-offset:2px}}input::placeholder{{color:#98a5bf}}.count{{color:var(--muted);margin:10px 0 23px}}.grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:19px;margin:0 0 65px}}.product{{border:1px solid var(--edge);background:linear-gradient(155deg,#1a2740,#111b2c);border-radius:19px;overflow:hidden;display:flex;flex-direction:column;min-width:0;transition:transform .15s,border-color .15s}}.product:hover{{transform:translateY(-3px);border-color:#ff779170}}.product[hidden]{{display:none}}.product-top{{padding:15px 16px 0;display:flex;justify-content:space-between;gap:8px;align-items:center}}.chip{{background:#5f4b814d;color:#edddff;padding:4px 9px;border-radius:99px;font-size:.72rem}}.stock{{font-size:.7rem;color:var(--mint)}}.visual{{height:148px;margin:13px 16px 0;border:1px solid #ffffff18;border-radius:14px;position:relative;display:grid;place-items:center;overflow:hidden;background:radial-gradient(circle at 65% 70%,#643762,transparent 60%),linear-gradient(120deg,#263a60,#131d35)}}.product:nth-child(4n+2) .visual{{background:radial-gradient(circle at 65% 70%,#21615d,transparent 60%),linear-gradient(120deg,#254456,#131d35)}}.product:nth-child(4n+3) .visual{{background:radial-gradient(circle at 65% 70%,#5d3c30,transparent 60%),linear-gradient(120deg,#49364e,#131d35)}}.visual:after{{content:"";position:absolute;border:1px solid #ffffff25;width:105px;height:105px;border-radius:100%;box-shadow:0 0 0 28px #ffffff08,0 0 0 58px #ffffff06}}.visual-ideogram{{font-size:3.5rem;font-weight:800;color:#ffffffae}}.visual img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#10192b;z-index:2}}.visual-label,.visual-platform{{position:absolute;font-size:.68rem;color:#ffffffbc}}.visual-label{{top:10px;left:13px}}.visual-platform{{bottom:9px;right:13px}}.product-copy{{padding:16px 18px 20px;display:flex;flex:1;flex-direction:column}}.category{{margin:0;color:var(--pink);font-size:.75rem;font-weight:700}}h2{{font-size:1.13rem;line-height:1.4;letter-spacing:-.015em;margin:8px 0 23px;min-height:65px}}.bottom{{margin-top:auto;border-top:1px solid #ffffff18;padding-top:16px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px}}.bottom small{{display:block;color:var(--muted);font-size:.68rem}}strong{{font-size:1.42rem}}.btn{{background:var(--pink);color:#1d0c17;text-decoration:none;font-weight:800;border-radius:10px;padding:10px 13px;text-align:center;font-size:.86rem}}.btn:hover{{background:#ffa0af}}.fine{{color:#9aabc2;font-size:.75rem;margin:14px 0 0}}footer{{border-top:1px solid var(--edge);padding:27px 0 50px;color:var(--muted);font-size:.86rem}}footer p{{max-width:930px}}.empty{{padding:28px;background:var(--card);border-radius:12px;color:var(--muted)}}@media(max-width:990px){{.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}@media(max-width:640px){{.wrap{{padding:0 16px}}.hero{{padding:53px 0 27px}}.grid{{grid-template-columns:1fr}}.tools{{grid-template-columns:1fr}}h2{{min-height:0}}header .wrap{{gap:7px}}header .wrap>span{{display:none}}}}@media(prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style></head><body><header><div class="wrap"><div class="logo">IMPORT<span>JAPON</span></div><span style="color:var(--muted);font-size:.82rem">Sélection indépendante</span></div></header><main class="wrap"><section class="hero"><div class="eyebrow">Jeux & cartes numériques · Comptes japonais</div><h1>Le Japon à portée de console.</h1><p class="intro">Cartes prépayées, abonnements et jeux numériques pour comptes japonais. Une sélection limitée, actualisée automatiquement avec les liens du vendeur. Vérifiez toujours les restrictions de région avant achat.</p></section><div class="warning">⚠️ <b>Important :</b> une carte ou un code de région JP peut nécessiter un compte japonais. Vérifiez les restrictions, la langue, la plateforme et les conditions de remboursement chez Play-Asia avant toute commande.</div><div class="tools"><input id="search" type="search" placeholder="Rechercher un produit…" aria-label="Rechercher un produit"><select id="platform" aria-label="Filtrer par catégorie"><option value="">Toutes les catégories</option>{opts}</select></div><p id="count" class="count">{len(products)} produits · Dernière actualisation : {safe(updated)}{' · Aperçu simulé' if test else ''}</p><div class="grid" id="grid">{cards}</div></main><footer><div class="wrap"><p><b>Transparence :</b> certains liens sont affiliés : une commande éligible peut nous rapporter une commission sans surcoût pour vous.</p><p>Site indépendant non officiel, non exploité par Play-Asia, Nintendo, Sony ou les éditeurs mentionnés. Les informations de catalogue et prix peuvent évoluer ; la fiche du vendeur fait foi.</p><p>Les jaquettes, lorsqu’elles sont affichées, proviennent des URL du catalogue Play-Asia et restent la propriété de leurs ayants droit. Prix et stocks indicatifs ; aucune langue ou compatibilité régionale n’est garantie par ce site. Version en <b>noindex</b> pendant les vérifications.</p></div></footer><script>let s=document.querySelector('#search'),p=document.querySelector('#platform'),g=document.querySelector('#grid');function filter(){{let q=s.value.toLocaleLowerCase('fr'),v=p.value,n=0;for(let e of g.querySelectorAll('.product')){{let ok=e.innerText.toLocaleLowerCase('fr').includes(q)&&(!v||e.dataset.kind===v);e.hidden=!ok;if(ok)n++}}document.querySelector('#count').textContent=n+' produit(s) affiché(s) · Actualisé : {safe(updated)}'}}s.addEventListener('input',filter);p.addEventListener('change',filter);</script></body></html>'''

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
