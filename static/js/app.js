document.addEventListener('DOMContentLoaded',function(){ 
var body=document.body; 
var search=document.querySelector('[data-app-search]'); 
var text=document.querySelector('[data-text-input]'); 
var count=document.querySelector('[data-character-count]'); 
var form=document.querySelector('[data-analyze-form]'); 
var avatar=document.querySelector('[data-avatar-toggle]'); 
var menu=avatar?avatar.closest('.profile-menu'):null; 
function onAll(selector,eventName,handler){document.querySelectorAll(selector).forEach(function(node){node.addEventListener(eventName,handler);});} 
function addClass(name){body.classList.add(name);} 
function removeClass(name){body.classList.remove(name);} 
onAll('[data-sidebar-open]','click',function(){addClass('sidebar-open');}); 
onAll('[data-sidebar-collapse]','click',function(){body.classList.toggle('sidebar-collapsed');}); 
onAll('[data-open-docs]','click',function(){removeClass('notifications-open');addClass('docs-open');}); 
onAll('[data-close-docs]','click',function(){removeClass('docs-open');}); 
onAll('[data-open-notifications]','click',function(){removeClass('docs-open');addClass('notifications-open');}); 
onAll('[data-close-notifications]','click',function(){removeClass('notifications-open');}); 
var sidebarOverlay=document.querySelector('[data-sidebar-overlay]'); 
if(sidebarOverlay){sidebarOverlay.addEventListener('click',function(){removeClass('sidebar-open');});} 
var drawerOverlay=document.querySelector('[data-drawer-overlay]'); 
if(drawerOverlay){drawerOverlay.addEventListener('click',function(){removeClass('docs-open');removeClass('notifications-open');});} 
if(avatar){if(menu){avatar.addEventListener('click',function(){var open=menu.classList.toggle('is-open');avatar.setAttribute('aria-expanded',open?'true':'false');});}} 
document.addEventListener('click',function(event){if(menu){if(!menu.contains(event.target)){menu.classList.remove('is-open');if(avatar){avatar.setAttribute('aria-expanded','false');}}}if(body.classList.contains('sidebar-open')){if(!event.target.closest('#appSidebar')){if(!event.target.closest('[data-sidebar-open]')){removeClass('sidebar-open');}}}}); 
document.addEventListener('keydown',function(event){if(event.key==='Escape'){removeClass('sidebar-open');removeClass('docs-open');removeClass('notifications-open');if(menu){menu.classList.remove('is-open');}if(avatar){avatar.setAttribute('aria-expanded','false');}}if(event.key==='/'){if(search){if(event.target!==search){if(event.target.tagName!=='INPUT'){if(event.target.tagName!=='TEXTAREA'){event.preventDefault();search.focus();}}}}}}); 

document.querySelectorAll('.meter__fill').forEach(function(meter) {
    var value = meter.getAttribute('data-value');
    if (value) {
        meter.style.width = value + '%';
    }
});
 
function syncCount(){if(text){if(count){var size=text.value.trim().length;count.textContent=size+' character'+(size===1?'':'s');}}} 
syncCount(); 
if(text){text.addEventListener('input',syncCount);} 
onAll('[data-prompt-chip]','click',function(event){if(text){text.value=event.currentTarget.dataset.promptChip?event.currentTarget.dataset.promptChip:'';text.focus();syncCount();}}); 
if(form){form.addEventListener('submit',function(){addClass('is-submitting');});} 
function splitPipe(value){if(!value){return [];}return value.split('|').map(function(item){return item.trim();}).filter(Boolean);} 
if(window.Chart){document.querySelectorAll('.chart-canvas[data-chart]').forEach(function(canvas){var labels=splitPipe(canvas.dataset.labels);var values=splitPipe(canvas.dataset.values).map(Number);var ctx=canvas.getContext('2d');if(!ctx){return;}if(!labels.length){return;}if(!values.length){return;}if(values.every(function(item){return !item;})){return;}if(canvas.dataset.chart==='confidence-trend'){var gradient=ctx.createLinearGradient(0,0,0,280);gradient.addColorStop(0,'rgba(99,102,241,.34)');gradient.addColorStop(1,'rgba(99,102,241,0)');new Chart(ctx,{type:'line',data:{labels:labels,datasets:[{data:values,borderColor:'#818CF8',backgroundColor:gradient,fill:true,tension:.38,borderWidth:2,pointRadius:3,pointBackgroundColor:'#C7D2FE'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{color:'rgba(148,163,184,.68)',maxRotation:0,autoSkip:true}},y:{min:0,max:100,ticks:{color:'rgba(148,163,184,.68)',callback:function(value){return value+'%';}},grid:{color:'rgba(148,163,184,.08)'}}}}});}if(canvas.dataset.chart==='verdict-share'){new Chart(ctx,{type:'doughnut',data:{labels:labels,datasets:[{data:values,backgroundColor:['#EF4444','#22C55E'],borderWidth:2,hoverOffset:6}]},options:{responsive:true,maintainAspectRatio:false,cutout:'72%',plugins:{legend:{display:false}}}});}});} 
if(search){var items=Array.prototype.slice.call(document.querySelectorAll('[data-searchable],.history-table tbody tr'));search.addEventListener('input',function(){var value=search.value.trim().toLowerCase();items.forEach(function(item){var source=item.dataset.searchable?item.dataset.searchable:item.textContent;var textValue=source.toLowerCase();if(value){if(textValue.indexOf(value)===-1){item.classList.add('is-filtered-out');}else{item.classList.remove('is-filtered-out');}}else{item.classList.remove('is-filtered-out');}});});} 
document.querySelectorAll('a[href]').forEach(function(link){link.addEventListener('click',function(event){var href=link.getAttribute('href');if(!href){return;}if(href.charAt(0)==='#'){return;}if(link.target==='_blank'){return;}if(event.metaKey){return;}if(event.ctrlKey){return;}if(event.shiftKey){return;}if(event.altKey){return;}var url=new URL(link.href,window.location.href);if(url.origin===window.location.origin){body.classList.add('is-navigating');}});}); 
document.querySelectorAll('.button,.icon-button,.avatar-button,.nav-link,.suggestion-chip').forEach(function(node){node.addEventListener('pointerdown',function(event){var rect=node.getBoundingClientRect();var ripple=document.createElement('span');ripple.className='ripple';ripple.style.left=event.clientX-rect.left+'px';ripple.style.top=event.clientY-rect.top+'px';node.appendChild(ripple);setTimeout(function(){ripple.remove();},620);});}); 
});
