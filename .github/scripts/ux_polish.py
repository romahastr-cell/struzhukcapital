from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css_marker = '@media(prefers-reduced-motion:reduce)'
css = r'''
/* === 2026 POLISH v2: living mathematics === */
:focus-visible{outline:3px solid rgba(108,60,255,.32);outline-offset:3px}
.site-header{transition:background .35s var(--ease),box-shadow .35s var(--ease),border-color .35s var(--ease)}
.site-header.is-scrolled{background:rgba(8,7,14,.88);border-bottom-color:rgba(157,124,255,.16);box-shadow:0 14px 38px rgba(7,5,18,.16)}
.site-header.is-scrolled .brand img{transform:scale(.92);box-shadow:0 8px 28px rgba(93,54,210,.18)}
.brand img{transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.hero-inner{position:relative;z-index:2}
.math-field{position:absolute;inset:0;z-index:1;pointer-events:none;overflow:hidden;opacity:.22;mask-image:linear-gradient(to bottom,rgba(0,0,0,.85),transparent 92%)}
.math-symbol{position:absolute;color:rgba(229,221,255,.34);font:700 clamp(10px,1.1vw,15px)/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.02em;white-space:nowrap;text-shadow:0 0 22px rgba(117,82,255,.22);animation:mathDrift var(--dur,18s) ease-in-out infinite alternate;transform:translate3d(0,0,0) rotate(var(--rot,0deg))}
@keyframes mathDrift{50%{transform:translate3d(var(--dx,18px),var(--dy,-24px),0) rotate(calc(var(--rot,0deg) + 2deg));opacity:.72}}
.ticker{background:linear-gradient(120deg,rgba(255,255,255,.82),rgba(248,246,255,.72),rgba(255,255,255,.86));background-size:220% 100%;animation:tickerFlow 8s ease-in-out infinite}
.ticker::after{content:'LIVE';position:absolute;right:13px;top:10px;padding:3px 7px;border-radius:999px;background:rgba(108,60,255,.07);color:#7755e9;font-size:8px;font-weight:900;letter-spacing:.13em;animation:livePulse 2s ease-in-out infinite}
@keyframes tickerFlow{50%{background-position:100% 50%}}@keyframes livePulse{50%{opacity:.55;transform:scale(.96)}}
.tabs{scroll-snap-type:x proximity;mask-image:linear-gradient(90deg,transparent 0,#000 16px,#000 calc(100% - 20px),transparent 100%)}
.tab{scroll-snap-align:center}.tab.active::after{content:'';position:absolute;left:22%;right:22%;bottom:5px;height:2px;border-radius:999px;background:rgba(255,255,255,.75);box-shadow:0 0 12px rgba(255,255,255,.5)}
.card{transform:translateZ(0)}
.card::after{content:'';position:absolute;inset:-1px;border-radius:inherit;pointer-events:none;background:linear-gradient(120deg,transparent 18%,rgba(255,255,255,.52) 34%,transparent 48%);transform:translateX(-120%);opacity:0}
.card:hover::after{opacity:.34;animation:cardSheen 1.05s var(--ease)}
@keyframes cardSheen{to{transform:translateX(120%)}}
.btn,.liquid{--bx:50%;--by:50%}
.btn::after,.liquid::after{content:'';position:absolute;inset:0;z-index:-1;border-radius:inherit;background:radial-gradient(120px circle at var(--bx) var(--by),rgba(255,255,255,.34),transparent 62%);opacity:0;transition:opacity .25s}
.btn:hover::after,.liquid:hover::after{opacity:1}
.fx-ripple{position:absolute;border-radius:50%;pointer-events:none;background:rgba(255,255,255,.46);transform:translate(-50%,-50%) scale(0);animation:fxRipple .58s ease-out forwards}
@keyframes fxRipple{to{transform:translate(-50%,-50%) scale(1);opacity:0}}
.km.value-flash{animation:valueFlash .52s var(--ease)}
@keyframes valueFlash{0%{transform:scale(.985)}45%{transform:scale(1.018);box-shadow:0 14px 38px rgba(85,50,190,.11),inset 0 1px 0 #fff}100%{transform:none}}
.bar{will-change:height,filter}.bar:hover{filter:brightness(1.14) saturate(1.08)}
.pie-wrap{position:relative;overflow:hidden}.pie-wrap::after{content:'';position:absolute;width:240px;height:240px;right:-120px;top:-130px;border-radius:50%;background:radial-gradient(circle,rgba(108,60,255,.10),transparent 68%);pointer-events:none;animation:orbFloat 9s var(--ease) infinite}
.table-wrap,.yearbox{overscroll-behavior:contain;scrollbar-color:rgba(108,60,255,.24) transparent;scrollbar-width:thin}
.table-wrap::-webkit-scrollbar,.yearbox::-webkit-scrollbar{width:8px;height:8px}.table-wrap::-webkit-scrollbar-thumb,.yearbox::-webkit-scrollbar-thumb{background:rgba(108,60,255,.20);border-radius:999px}
@media(max-width:560px){.ticker{padding-right:52px}.ticker b{display:inline-block;margin-top:3px}.math-symbol:nth-child(n+9){display:none}.tabs{mask-image:linear-gradient(90deg,transparent,#000 10px,#000 calc(100% - 12px),transparent)}}
'''

if '2026 POLISH v2' not in s:
    if css_marker not in s:
        raise RuntimeError('CSS marker missing')
    s = s.replace(css_marker, css + '\n' + css_marker, 1)

pro_pattern = r"function calcPRO\(\)\{.*?\}\nfunction calcLIGHT"
pro_repl = r'''function calcPRO(){const S=+$('#p-start').value||0,P=+$('#p-monthly').value||0,Y=+$('#p-years').value||0,apr=+$('#p-rate').value||0,type=$('#p-rateType').value,cap=$('#p-cap').value,reinv=$('#p-reinv').value==='yes',months=Math.max(0,Math.round(Y*12));let im=monthlyFromAPR(apr,type);if(cap==='day'){const id=dailyFromAPR(apr,type);im=Math.pow(1+id,30.4167)-1}let bal=S,own=S,vals=[],labs=[],yearInterest=0,rows=[],paidInterest=0;for(let m=1;m<=months;m++){bal+=P;own+=P;const intr=bal*im;yearInterest+=intr;if(reinv)bal+=intr;else paidInterest+=intr;if(m%12===0){const wealth=bal+(reinv?0:paidInterest);vals.push(Math.round(wealth));labs.push(`${m/12} год`);rows.push({year:m/12,balance:Math.round(wealth),earned:Math.round(yearInterest),deposit:P*12});yearInterest=0}}const fv=Math.round(bal+(reinv?0:paidInterest)),profit=Math.round(reinv?bal-own:paidInterest);$('#p-sum').textContent=fmt(fv);$('#p-own').textContent=fmt(own);$('#p-profit').textContent=fmt(profit);$('#p-eff').textContent=((Math.pow(1+im,12)-1)*100).toFixed(2)+'%';drawBars('p-bars',vals,labs);animatePie('pie',own,Math.max(0,profit));const tb=$('#yearTable tbody');tb.innerHTML='';rows.forEach(r=>{const tr=document.createElement('tr');tr.innerHTML=`<td>${r.year} год</td><td>${fmt(r.balance)} ₽</td><td>${fmt(r.earned)} ₽</td><td>${fmt(r.deposit)} ₽</td>`;tb.appendChild(tr)});const sh=makeShare(`PRO: старт ${fmt(S)} ₽, пополнение ${fmt(P)} ₽/мес, срок ${Y} лет, ставка ${apr}%.\nИтог: ${fmt(fv)} ₽. Внесено: ${fmt(own)} ₽. Доход: ${fmt(profit)} ₽.`);$('#p-share-tg').href=sh.tg;$('#p-share-wa').href=sh.wa;toast('PRO рассчитан')}
function calcLIGHT'''
s2, n = re.subn(pro_pattern, pro_repl, s, count=1, flags=re.S)
if n != 1:
    raise RuntimeError(f'calcPRO patch failed: {n}')
s = s2

light_pattern = r"function calcLIGHT\(\)\{.*?\}\nfunction calcLOSE"
light_repl = r'''function calcLIGHT(){const P=+$('#l-start').value||0,rate=+$('#l-rate').value||0,per=$('#l-ratep').value,days=Math.max(1,Math.round(+$('#l-days').value||1));let rd=rate/100;if(per==='month')rd=Math.pow(1+rd,1/30.4167)-1;if(per==='year')rd=Math.pow(1+rd,1/365)-1;let bal=P,total=0,rows=[[1,P,0]];for(let d=2;d<=days;d++){const intr=bal*rd;bal+=intr;total+=intr;rows.push([d,bal,intr])}$('#l-sum').textContent=fmt(Math.round(bal));$('#l-profit').textContent=fmt(Math.round(total));$('#l-meta').textContent=rate+'% '+(per==='day'?'в день':per==='month'?'в месяц':'в год');const tbody=$('#l-table tbody');tbody.innerHTML='';rows.forEach(([d,b,i])=>{const tr=document.createElement('tr');tr.innerHTML=`<td>${d}</td><td>${fmt(Math.round(b))}</td><td>${i.toLocaleString('ru-RU',{minimumFractionDigits:2,maximumFractionDigits:2})} ₽ · ${(rd*100).toFixed(4)}%</td>`;tbody.appendChild(tr)});let csv='День;Баланс, ₽;Заработано, ₽;Дневная ставка, %\n'+rows.map(([d,b,i])=>`${d};${b.toFixed(2)};${i.toFixed(2)};${(rd*100).toFixed(6)}`).join('\n');$('#l-csv').onclick=()=>{const blob=new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`strategy_light_${days}d.csv`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500)};const preview=rows.slice(0,18).map(([d,b,i])=>`${d}. ${fmt(Math.round(b))} ₽ (+${i.toFixed(2)} ₽)`).join('\n'),sh=makeShare(`LIGHT: ${fmt(P)} ₽, ${rate}% ${per==='day'?'в день':per==='month'?'в месяц':'в год'}, ${days} дней.\nИтог: ${fmt(Math.round(bal))} ₽.\n\n${preview}${rows.length>18?'\n…':''}`);$('#l-share-tg-table').href=sh.tg;$('#l-share-wa-table').href=sh.wa;toast('LIGHT рассчитан')}
function calcLOSE'''
s2, n = re.subn(light_pattern, light_repl, s, count=1, flags=re.S)
if n != 1:
    raise RuntimeError(f'calcLIGHT patch failed: {n}')
s = s2

init_marker = "quickCalc();calcPRO();calcLIGHT();calcLOSE();calcGOAL();calcNEED();calcINFL();"
enhancement = r'''
/* 2026 POLISH v2 interactions */
(function(){
  const header=$('.site-header');
  const onScroll=()=>header?.classList.toggle('is-scrolled',scrollY>36);
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  const hero=$('.hero');
  if(hero&&!hero.querySelector('.math-field')&&motionOK()){
    const field=document.createElement('div');field.className='math-field';
    const formulas=['FV=P(1+r)^n','Σ cashflow','1+r/12','PV → FV','Δt × rate','compound()','rₑ=(1+rₙ/m)^m−1','∞','∑','₽ → time','xⁿ','growth ≠ linear'];
    formulas.forEach((txt,i)=>{const el=document.createElement('span');el.className='math-symbol';el.textContent=txt;el.style.left=(4+(i*17)%90)+'%';el.style.top=(8+(i*23)%78)+'%';el.style.setProperty('--dur',(14+(i%5)*3)+'s');el.style.setProperty('--dx',((i%2?1:-1)*(12+(i%4)*7))+'px');el.style.setProperty('--dy',(-(12+(i%5)*8))+'px');el.style.setProperty('--rot',((i%3-1)*4)+'deg');field.appendChild(el)});hero.insertBefore(field,hero.firstChild);
  }
  $$('.tab').forEach(tab=>tab.addEventListener('click',()=>{const strip=tab.parentElement;if(!strip)return;const target=tab.offsetLeft-(strip.clientWidth-tab.offsetWidth)/2;strip.scrollTo({left:Math.max(0,target),behavior:motionOK()?'smooth':'auto'})}));
  if(matchMedia('(hover:hover) and (pointer:fine)').matches){$$('.btn,.liquid').forEach(btn=>btn.addEventListener('pointermove',e=>{const r=btn.getBoundingClientRect();btn.style.setProperty('--bx',((e.clientX-r.left)/r.width*100)+'%');btn.style.setProperty('--by',((e.clientY-r.top)/r.height*100)+'%')}))}
  $$('.btn,.liquid').forEach(btn=>btn.addEventListener('click',e=>{if(!motionOK())return;const r=btn.getBoundingClientRect(),d=Math.max(r.width,r.height)*1.5,sp=document.createElement('span');sp.className='fx-ripple';sp.style.width=sp.style.height=d+'px';sp.style.left=(e.clientX-r.left)+'px';sp.style.top=(e.clientY-r.top)+'px';btn.appendChild(sp);setTimeout(()=>sp.remove(),650)}));
  $$('.km b').forEach(node=>{new MutationObserver(()=>{const card=node.closest('.km');if(!card)return;card.classList.remove('value-flash');void card.offsetWidth;card.classList.add('value-flash')}).observe(node,{childList:true,characterData:true,subtree:true})});
})();
'''
if '2026 POLISH v2 interactions' not in s:
    if init_marker not in s:
        raise RuntimeError('init marker missing')
    s = s.replace(init_marker, enhancement + '\n' + init_marker, 1)

p.write_text(s, encoding='utf-8')

sw = Path('service-worker.js')
if sw.exists():
    t = sw.read_text(encoding='utf-8')
    t = re.sub(r"const CACHE = '.*?';", "const CACHE = 'sk-v3-2026-polish';", t, count=1)
    sw.write_text(t, encoding='utf-8')
