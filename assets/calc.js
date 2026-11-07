/* Stillprice live calculator. Port of calc.py; keep in sync. Data: window.SP_APPS (from data/apps.json at build). */
(function(){
function m(x){var s=x.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});return '$'+(s.slice(-3)=='.00'?s.slice(0,-3):s);}
function n(x){return x.toLocaleString('en-US');}
function cheapest(o){o=o.filter(function(a){return a.total!==null});return o.reduce(function(a,b){return b.total<a.total?b:a});}
var pl=function(k,w){return k>1?w+'s':w;};
var M={
gorgias:function(p,conv,seats,ai){var opts=p.plans.map(function(r){var name=r[0],base=r[1],tix=r[2],over=r[3],inc=r[4];var et=Math.max(0,conv-tix),ea=Math.max(0,ai-inc);var t=base+et*over+ea*p.ai_unit;
 return {total:t,plan:name,math:[name+' plan '+m(base)+'/mo (includes '+n(tix)+' tickets, '+inc+' AI interactions)','Tickets: '+n(conv)+' (AI handled ones count as tickets too) → '+n(et)+' over × '+m(over)+' = '+m(et*over),'AI interactions: '+n(ai)+' − '+inc+' included = '+n(ea)+' × '+m(p.ai_unit)+' = '+m(ea*p.ai_unit)]};});
 var o=cheapest(opts);o.math.push('Cheapest plan at this size: '+o.plan+' = '+m(o.total)+'/mo. If AI goes over your committed allowance, Gorgias lists '+m(p.ai_overage_note)+' per interaction.');return o;},
tidio:function(p,conv,seats,ai){var h=conv-ai,lp=p.lyro[0],lc=p.lyro[1],cp=p.cs_starter[0],cc=p.cs_starter[1];
 if(conv<=lc&&h<=cc)return {total:lp+cp,plan:'Lyro AI Agent + Customer Service Starter',math:['Lyro conversations: all '+n(conv)+' chats get a Lyro reply → Lyro plan '+m(lp)+' (up to '+lc+')','Human replied conversations: '+n(h)+' → Customer Service Starter '+m(cp)+' (up to '+cc+')','Total '+m(lp)+' + '+m(cp)+' = '+m(lp+cp)+'/mo']};
 return {total:null,plan:'Higher Lyro / Customer Service tiers',math:['Needs about '+n(conv)+' Lyro conversations and '+n(h)+' human conversations a month.',"Tidio's public prices we could confirm stop at "+lc+' Lyro conversations ('+m(lp)+') and 250 human conversations (from $59). Not public, check site.']};},
intercom:function(p,conv,seats,ai){var s=seats*p.seat,f=ai*p.fin;return {total:s+f,plan:'Essential × '+seats+' '+pl(seats,'seat')+' + Fin',math:['Seats: '+seats+' × '+m(p.seat)+' (monthly) = '+m(s),'Fin outcomes: '+n(ai)+' × '+m(p.fin)+' = '+m(f),'Total '+m(s+f)+'/mo. Outcomes can exceed full resolutions, since a handoff via a Fin workflow also counts.']};},
zendesk:function(p,conv,seats,ai){var s=seats*p.seat,inc=seats*p.incl_per_seat,ex=Math.max(0,ai-inc),u=ex*p.payg;return {total:s+u,plan:'Suite Team × '+seats+' + pay as you go resolutions',math:['Seats: '+seats+' × '+m(p.seat)+' (monthly) = '+m(s),'Automated resolutions: '+n(ai)+' − '+inc+' included = '+n(ex)+' × '+m(p.payg)+' = '+m(u),'Total '+m(s+u)+'/mo. With committed resolutions at '+m(p.committed)+': '+m(s+ex*p.committed)+'/mo.']};},
hubspot:function(p,conv,seats,ai){var s=seats*p.seat,ex=Math.max(0,ai-p.incl_res),u=ex*p.unit;return {total:s+u,plan:'Professional × '+seats+' '+pl(seats,'seat'),math:['Seats: '+seats+' × '+m(p.seat)+' (monthly) = '+m(s),'Resolutions: '+n(ai)+' − ~'+p.incl_res+' covered by 3,000 included credits = '+n(ex)+' × '+m(p.unit)+' = '+m(u),'Total '+m(s+u)+'/mo, plus '+m(p.onboarding)+' one time onboarding.']};},
free:function(){return {total:0,plan:'Free',math:['Free app, no usage fee listed. $0/mo.']};},
richpanel:function(p,conv,seats,ai){var s=seats*p.seat,use=conv*p.per_conv,a=Math.max(p.ai_min,use);return {total:s+a,plan:seats+' helpdesk '+pl(seats,'seat')+' + AI meter',math:['Seats: '+seats+' × '+m(p.seat)+' (monthly) = '+m(s),'AI: '+n(conv)+' AI handled conversations × ~'+m(p.per_conv)+' = '+m(use)+'; minimum '+m(p.ai_min)+' → '+m(a),'Total ≈ '+m(s+a)+'/mo (approximate: AI cost depends on tokens).']};},
reamaze:function(p,conv,seats,ai){var s=seats*p.seat,inc=seats*p.incl_per_seat,ex=Math.max(0,ai-inc),u=ex*p.unit;return {total:s+u,plan:'Basic × '+seats+' '+pl(seats,'user'),math:['Users: '+seats+' × '+m(p.seat)+' = '+m(s),'AI resolutions: '+n(ai)+' − '+inc+' included = '+n(ex)+' × '+m(p.unit)+' = '+m(u),'Total '+m(s+u)+'/mo']};},
freshdesk:function(p,conv,seats,ai){var s=seats*p.seat,k=Math.ceil(conv/p.pack_size),u=k*p.pack;return {total:s+u,plan:'Growth × '+seats+' (annual) + session packs',math:['Seats: '+seats+' × '+m(p.seat)+' (annual billing) = '+m(s),'AI sessions: '+n(conv)+' AI handled conversations → '+k+' packs × '+m(p.pack)+' = '+m(u),'Total '+m(s+u)+'/mo']};},
zipchat:function(p,conv){for(var i=0;i<p.plans.length;i++){var r=p.plans[i];if(conv<=r[2])return {total:r[1],plan:r[0],math:[n(conv)+' conversations fits '+r[0]+' (~'+n(r[2])+' conversations) → '+m(r[1])+'/mo (monthly billing)']};}
 return {total:p.scale_plus_annual,plan:'Scale Plus (annual)',math:[n(conv)+' conversations exceeds Scale (~2,500). Scale Plus covers ~6,000 → '+m(p.scale_plus_annual)+'/mo billed annually (monthly billing price not public).']};},
siena:function(p,conv,seats,ai){var u=ai*p.unit;return {total:p.platform+u,plan:'Platform + automation pack',math:['Platform fee '+m(p.platform),'Automated tickets: '+n(ai)+' × '+m(p.unit)+' = '+m(u),'Total '+m(p.platform+u)+'/mo + support and implementation (not public)']};},
chatty:function(p,conv){var opts=p.plans.map(function(r){var ex=Math.max(0,conv-r[2]),t=r[1]+ex*p.unit;return {total:t,plan:r[0],math:[r[0]+' '+m(r[1])+' includes '+n(r[2])+' AI conversations; '+n(ex)+' extra × '+m(p.unit)+' = '+m(ex*p.unit)+' → '+m(t)]};});
 var o=cheapest(opts);o.math.push('Cheapest plan at this size: '+o.plan+' = '+m(o.total)+'/mo');return o;},
helpcenter:function(p,conv){var opts=p.plans.map(function(r){var ex=Math.max(0,conv-r[2]),t=r[1]+ex*r[3];return {total:t,plan:r[0],math:[r[0]+' '+m(r[1])+' includes '+n(r[2])+' tickets; '+n(ex)+' extra × '+m(r[3])+' = '+m(ex*r[3])+' → '+m(t)]};});
 var o=cheapest(opts);o.math.push('Cheapest plan at this size: '+o.plan+' = '+m(o.total)+'/mo (no AI agent, AI FAQs only)');return o;},
aide:function(p,conv){var opts=[];for(var i=0;i<p.plans.length;i++){var r=p.plans[i],name=r[0],price=r[1],included=r[2],overRate=r[3]||0,overCap=r[4]||0,extra=Math.max(0,conv-included),extraCost=extra*overRate;if(extra===0){opts.push({total:price,plan:name,math:[n(conv)+' conversations, assuming at least one AI reply each, fits '+name+' ('+n(included)+' AI replies/mo included) → '+m(price)+'/mo (monthly billing, no seat fees)']});continue;}if(!overRate||extraCost>overCap+1e-9)continue;var t=price+extraCost;opts.push({total:t,plan:name,math:[name+' '+m(price)+'/mo includes '+n(included)+' AI replies',n(conv)+' conversations, assuming at least one AI reply each → '+n(extra)+' extra × '+m(overRate)+' = '+m(extraCost),'Total '+m(price)+' + '+m(extraCost)+' = '+m(t)+'/mo (monthly billing, no seat fees). Extra replies cap at '+m(overCap)+'/mo, then AI pauses.']});}if(!opts.length)return {total:null,plan:'Above published paid caps',math:['This many AI replies is above the published paid plans and their extra reply caps.']};var o=cheapest(opts);if(opts.length>1)o.math.push('Cheapest plan at this size: '+o.plan+' = '+m(o.total)+'/mo');return o;}
};
function run(conv,seats,rate){var ai=Math.floor(conv*rate+1e-9);return window.SP_APPS.map(function(a){var r=M[a.model](a.params,conv,seats,ai);r.app=a;return r;})
 .sort(function(x,y){if(x.total===null)return 1;if(y.total===null)return -1;return x.total-y.total;});}
window.SPCalc={run:run,m:m};
if(typeof document==='undefined')return;
var KEY='sp_calc_unlocked',$=function(i){return document.getElementById(i)};
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]});}
var used=false;
function render(){var conv=Math.max(1,parseInt($('c-conv').value)||1),seats=Math.max(1,parseInt($('c-seats').value)||1),rate=Math.min(100,Math.max(0,parseInt($('c-rate').value)||0))/100;
 var res=run(conv,seats,rate),paid=res.filter(function(r){return r.total!==null&&r.app.model!=='free'});var top=paid[0];
 $('c-head').innerHTML='<p class=eyebrow style="margin:0 0 8px">Cheapest paid AI option at '+n(conv)+' conversations</p><p class=big>'+esc(top.app.name)+' <span>'+m(top.total)+'/mo</span></p><p class=muted style="margin:0">'+esc(top.plan)+'. Most expensive listed: '+esc(paid[paid.length-1].app.name)+' at '+m(paid[paid.length-1].total)+'/mo. Shopify Inbox is listed free, see the full list.</p>';
 var rows=res.map(function(r){return '<details class=crow><summary><span class=cn>'+esc(r.app.name)+'</span><span class=cp>'+esc(r.plan)+'</span><b class=ct>'+(r.total===null?"<span class='tag np'>Not public</span>":m(r.total))+'</b></summary><ul>'+r.math.map(function(l){return '<li>'+esc(l)+'</li>'}).join('')+'</ul><p class=muted style="margin:6px 0 0;font-size:14px">How it bills: '+esc(r.app.ai_billing||'')+' <a href="'+esc(r.app.pricing_url)+'" rel=noopener target=_blank>Official pricing</a> · checked '+esc(r.app.checked)+'</p></details>';}).join('');
 $('c-rows').innerHTML=rows;
 if(!used){used=true;try{window.umami&&umami.track('calc-used')}catch(e){}}
}
function unlock(){document.body.classList.add('sp-unlocked');}
document.addEventListener('DOMContentLoaded',function(){
 ['c-conv','c-seats','c-rate'].forEach(function(i){$(i).addEventListener('input',function(){if(i=='c-conv')$('c-slide').value=$(i).value;render();});});
 $('c-slide').addEventListener('input',function(){$('c-conv').value=this.value;render();});
 try{if(localStorage.getItem(KEY))unlock();}catch(e){}
 $('c-form').addEventListener('submit',function(ev){ev.preventDefault();var em=$('c-email').value.trim();if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)){$('c-err').textContent='Please enter a valid email.';return;}
  window.open('https://stillprice.substack.com/subscribe?email='+encodeURIComponent(em),'_blank','noopener');
  try{localStorage.setItem(KEY,'1')}catch(e){} try{window.umami&&umami.track('email-submitted')}catch(e){} unlock();});
 render();});
})();
if(typeof module!=='undefined')module.exports=null;
