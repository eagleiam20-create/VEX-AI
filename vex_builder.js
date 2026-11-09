(() => {
  'use strict';

  if (window.__VEX_BUILDER_LOADED__) return;
  window.__VEX_BUILDER_LOADED__ = true;

  const style = document.createElement('style');
  style.textContent = `
  #vexBuilderLaunch{margin-left:auto;background:#fff;color:#000;border:0;border-radius:18px;padding:9px 14px;font-weight:700;font-size:12px}
  #vexBuilderOverlay{position:fixed;inset:0;z-index:1000;background:#000;color:#fff;display:none;font-family:inherit}
  #vexBuilderOverlay.open{display:flex;flex-direction:column}
  #vexBuilderHead{height:58px;flex-shrink:0;border-bottom:1px solid #292929;display:flex;align-items:center;gap:12px;padding:0 18px}
  #vexBuilderHead strong{letter-spacing:1.5px}
  #vexBuilderHead button,#vexBuilderActions button{background:#080808;color:#fff;border:1px solid #383838;border-radius:10px;padding:9px 12px;cursor:pointer}
  #vexBuilderBody{display:grid;grid-template-columns:minmax(260px,340px) 1fr;min-height:0;flex:1}
  #vexBuilderSide{border-right:1px solid #292929;padding:18px;overflow:auto}
  #vexBuilderSide label{display:block;color:#aaa;font-size:12px;margin:12px 0 7px}
  #vexBuilderPrompt{width:100%;min-height:130px;resize:vertical;background:#080808;color:#fff;border:1px solid #383838;border-radius:12px;padding:12px;outline:none}
  #vexBuilderGenerate{width:100%;margin-top:12px;padding:12px;background:#fff;color:#000;border:0;border-radius:12px;font-weight:800;cursor:pointer}
  #vexBuilderStatus{color:#aaa;font-size:12px;line-height:1.6;margin-top:12px;white-space:pre-wrap}
  #vexBuilderPreview{min-width:0;display:flex;flex-direction:column;padding:14px;gap:10px}
  #vexBuilderActions{display:flex;gap:8px;flex-wrap:wrap}
  #vexBuilderFrame{width:100%;flex:1;min-height:250px;background:#fff;border:1px solid #333;border-radius:12px}
  #vexBuilderCode{width:100%;height:190px;resize:vertical;background:#080808;color:#ddd;border:1px solid #333;border-radius:10px;padding:10px;font:12px/1.5 monospace}
  @media(max-width:760px){
    #vexBuilderBody{grid-template-columns:1fr;grid-template-rows:auto 1fr}
    #vexBuilderSide{border-right:0;border-bottom:1px solid #292929;max-height:42vh}
    #vexBuilderPreview{min-height:0}
    #vexBuilderFrame{min-height:230px}
  }`;
  document.head.appendChild(style);

  const overlay = document.createElement('section');
  overlay.id = 'vexBuilderOverlay';
  overlay.innerHTML = `
    <header id="vexBuilderHead">
      <strong>VEX AI · CODE BUILDER</strong>
      <span style="color:#888;font-size:11px">Browser-based project builder</span>
      <span style="flex:1"></span>
      <button id="vexBuilderClose">Close ×</button>
    </header>
    <div id="vexBuilderBody">
      <aside id="vexBuilderSide">
        <div style="font-size:19px;font-weight:800">Create a project</div>
        <p style="color:#999;font-size:12px;line-height:1.6">
          Describe the website or small app. VEX creates a browser preview from its built-in project templates.
        </p>
        <label for="vexBuilderPrompt">Your project idea</label>
        <textarea id="vexBuilderPrompt" placeholder="Example: Build a quiz app with 5 questions and a score screen."></textarea>
        <button id="vexBuilderGenerate">Generate project</button>
        <div id="vexBuilderStatus">Ready. Supported templates: calculator, quiz, expense tracker, todo, notes, portfolio and landing page.</div>
      </aside>
      <main id="vexBuilderPreview">
        <div id="vexBuilderActions">
          <button id="vexBuilderRun">Run preview</button>
          <button id="vexBuilderCheck">Check code</button>
          <button id="vexBuilderCopy">Copy HTML</button>
          <button id="vexBuilderDownload">Download HTML</button>
          <button id="vexBuilderZip">Download ZIP</button>
        </div>
        <iframe id="vexBuilderFrame" title="VEX project preview" sandbox="allow-scripts allow-forms"></iframe>
        <textarea id="vexBuilderCode" spellcheck="false" aria-label="Generated HTML code" placeholder="Generated project code appears here"></textarea>
      </main>
    </div>`;
  document.body.appendChild(overlay);

  const $ = id => document.getElementById(id);
  let currentHTML = '';

  function escapeText(s) {
    return String(s).replace(/[&<>"']/g, c => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
    }[c]));
  }

  function shell(title, body, script = '') {
    return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeText(title)}</title>
<style>
*{box-sizing:border-box}
body{margin:0;padding:24px;background:#f4f5f7;color:#171717;font:15px system-ui,Arial}
main{max-width:850px;margin:25px auto;background:white;padding:25px;border-radius:18px;box-shadow:0 8px 30px #0001}
h1{margin-top:0}
button{border:0;background:#111;color:white;border-radius:9px;padding:10px 14px;cursor:pointer}
input,textarea,select{padding:11px;border:1px solid #ccc;border-radius:9px;font:inherit;max-width:100%}
.row{display:flex;gap:9px;flex-wrap:wrap;margin:12px 0}
.muted{color:#666}
.item{padding:12px;border:1px solid #ddd;border-radius:10px;margin:8px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.card{padding:18px;background:#f1f2f4;border-radius:12px}
@media(max-width:600px){body{padding:8px}main{margin:8px auto;padding:17px}}
</style>
</head>
<body>
<main>${body}</main>
<script>${script}<\/script>
</body>
</html>`;
  }

  function buildCalculator() {
    return shell('VEX Calculator', `
      <h1>Calculator</h1>
      <input id="display" value="0" readonly style="width:100%;font-size:28px;text-align:right;margin-bottom:12px">
      <div class="grid">
        ${['7','8','9','÷','4','5','6','×','1','2','3','−','0','.','=','+','C'].map(x =>
          `<button data-key="${x}" style="padding:18px;font-size:18px">${x}</button>`
        ).join('')}
      </div>
      <p class="muted">Basic calculator · Runs in your browser</p>
    `, `
      let v='';
      document.querySelectorAll('[data-key]').forEach(b=>b.onclick=()=>{
        let k=b.dataset.key;
        if(k==='C')v='';
        else if(k==='='){
          try{
            let e=v.replace(/×/g,'*').replace(/÷/g,'/').replace(/−/g,'-');
            if(!/^[0-9+*/.() -]+$/.test(e))throw 0;
            v=String(Function('return ('+e+')')());
          }catch(e){v='Error'}
        }else v+=k;
        document.getElementById('display').value=v||'0';
      });
    `);
  }

  function buildTodo() {
    return shell('VEX Todo', `
      <h1>My Tasks</h1>
      <div class="row">
        <input id="task" placeholder="Add a task" style="flex:1">
        <button id="add">Add task</button>
      </div>
      <div id="list"></div>
    `, `
      const input=document.getElementById('task');
      const list=document.getElementById('list');
      function add(){
        let t=input.value.trim();
        if(!t)return;
        let d=document.createElement('div');
        d.className='item';
        let c=document.createElement('input');
        c.type='checkbox';
        let s=document.createElement('span');
        s.textContent=' '+t;
        let x=document.createElement('button');
        x.textContent='Delete';
        x.style.float='right';
        x.onclick=()=>d.remove();
        c.onchange=()=>s.style.textDecoration=c.checked?'line-through':'none';
        d.append(c,s,x);
        list.append(d);
        input.value='';
      }
      document.getElementById('add').onclick=add;
      input.addEventListener('keydown',e=>{if(e.key==='Enter')add()});
    `);
  }

  function buildNotes() {
    return shell('VEX Notes', `
      <h1>Quick Notes</h1>
      <textarea id="note" placeholder="Write your notes..." style="width:100%;min-height:240px"></textarea>
      <p class="muted">Notes are saved in this browser on this device.</p>
      <button id="save">Save notes</button>
      <span id="msg" class="muted"></span>
    `, `
      let n=document.getElementById('note');
      n.value=localStorage.getItem('vex_notes')||'';
      document.getElementById('save').onclick=()=>{
        localStorage.setItem('vex_notes',n.value);
        document.getElementById('msg').textContent=' Saved';
      };
    `);
  }

  function buildQuiz(prompt) {
    let match=prompt.match(/(\d+)\s*questions?/i);
    let count=Math.max(3,Math.min(20,Number(match?.[1]||5)));
    let questions=Array.from({length:count},(_,i)=>({
      q:`Sample question ${i+1}: Which option is correct?`,
      a:['Option A','Option B','Option C','Option D'],
      correct:0
    }));
    return shell('VEX Quiz', `
      <h1>Quiz App</h1>
      <p class="muted">${count} sample questions. Edit the question data in the code to customize.</p>
      <div id="quiz"></div>
      <button id="next">Start quiz</button>
      <p id="score"></p>
    `, `
      const qs=${JSON.stringify(questions)};
      let i=0,score=0;
      function show(){
        let q=qs[i];
        document.getElementById('quiz').innerHTML=
          '<h3>'+q.q+'</h3>'+
          q.a.map((a,j)=>'<div class="item"><label><input type="radio" name="ans" value="'+j+'"> '+a+'</label></div>').join('');
        document.getElementById('next').textContent=i===qs.length-1?'Finish':'Next';
      }
      document.getElementById('next').onclick=()=>{
        if(document.querySelector('input[name=ans]:checked')){
          let s=document.querySelector('input[name=ans]:checked');
          if(Number(s.value)===qs[i].correct)score++;
          i++;
        }else if(i!==0){
          document.getElementById('score').textContent='Choose an answer first.';
          return;
        }
        if(i>=qs.length){
          document.getElementById('quiz').innerHTML='<h2>Quiz complete</h2>';
          document.getElementById('next').style.display='none';
          document.getElementById('score').textContent='Score: '+score+' / '+qs.length;
        }else show();
      };
      show();
    `);
  }

  function buildExpense() {
    return shell('Expense Tracker', `
      <h1>Expense Tracker</h1>
      <div class="row">
        <input id="desc" placeholder="Expense name">
        <input id="amount" type="number" min="0" step="0.01" placeholder="Amount">
        <button id="add">Add</button>
      </div>
      <h2>Total: ₹<span id="total">0.00</span></h2>
      <div id="items"></div>
    `, `
      let rows=[];
      function render(){
        document.getElementById('items').innerHTML=rows.map((r,i)=>
          '<div class="item">'+r.name+' — ₹'+r.amount+
          ' <button data-i="'+i+'" style="float:right">Delete</button></div>'
        ).join('');
        document.getElementById('total').textContent=
          rows.reduce((s,r)=>s+r.amount,0).toFixed(2);
        document.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>{
          rows.splice(Number(b.dataset.i),1);
          render();
        });
      }
      document.getElementById('add').onclick=()=>{
        let name=document.getElementById('desc').value.trim();
        let amount=Number(document.getElementById('amount').value);
        if(!name||!Number.isFinite(amount)||amount<=0)return;
        rows.push({name,amount});
        document.getElementById('desc').value='';
        document.getElementById('amount').value='';
        render();
      };
    `);
  }

  function buildPortfolio() {
    return shell('Portfolio', `
      <nav class="row"><strong>MY PORTFOLIO</strong><span class="muted">Home · About · Projects · Contact</span></nav>
      <section style="padding:45px 0">
        <p class="muted">HELLO, I'M</p>
        <h1 style="font-size:42px">Your Name</h1>
        <h2>Web Developer &amp; Creative Thinker</h2>
        <p class="muted">I build clean, useful digital experiences.</p>
        <button onclick="document.getElementById('contact').scrollIntoView()">Contact me</button>
      </section>
      <h2>About</h2><p>Write a short introduction about yourself here.</p>
      <h2>Projects</h2>
      <div class="grid">
        <div class="card">Project One</div>
        <div class="card">Project Two</div>
        <div class="card">Project Three</div>
      </div>
      <h2 id="contact">Contact</h2><p>Email: hello@example.com</p>
    `);
  }

  function buildLanding() {
    return shell('Landing Page', `
      <nav class="row"><strong>YOUR BRAND</strong><span class="muted">Features · About · Contact</span></nav>
      <section style="text-align:center;padding:55px 5px">
        <h1 style="font-size:42px">Build something amazing</h1>
        <p class="muted">A simple responsive landing page for your idea.</p>
        <button onclick="document.getElementById('features').scrollIntoView()">Explore features</button>
      </section>
      <h2 id="features">Features</h2>
      <div class="grid">
        <div class="card"><h3>Simple</h3><p>Easy to use.</p></div>
        <div class="card"><h3>Fast</h3><p>Lightweight design.</p></div>
        <div class="card"><h3>Responsive</h3><p>Works on mobile and desktop.</p></div>
      </div>
    `);
  }

  function buildGeneric(prompt) {
    return shell('VEX Project', `
      <h1>Project starter</h1>
      <p class="muted">Requested idea:</p>
      <div class="item">${escapeText(prompt)}</div>
      <h2>Project structure</h2>
      <div class="grid">
        <div class="card">Home screen</div>
        <div class="card">Main feature</div>
        <div class="card">Settings</div>
      </div>
      <p>This is a starter layout. The requested custom functionality still needs to be implemented.</p>
    `);
  }

  function generate() {
    let p=$('vexBuilderPrompt').value.trim();
    if(!p){
      $('vexBuilderStatus').textContent='Please describe your project first.';
      return;
    }
    let q=p.toLowerCase();

    if(/calculator|calculate|math app/.test(q)) currentHTML=buildCalculator();
    else if(/quiz|question app|mcq/.test(q)) currentHTML=buildQuiz(p);
    else if(/expense|budget tracker|spending tracker/.test(q)) currentHTML=buildExpense();
    else if(/todo|to-do|task list/.test(q)) currentHTML=buildTodo();
    else if(/notes app|note taking/.test(q)) currentHTML=buildNotes();
    else if(/portfolio|personal website/.test(q)) currentHTML=buildPortfolio();
    else if(/landing page|business website|company website/.test(q)) currentHTML=buildLanding();
    else currentHTML=buildGeneric(p);

    $('vexBuilderCode').value=currentHTML;
    run();
    $('vexBuilderStatus').textContent=
      'Project generated from a built-in template. Preview it, inspect the code, and test its buttons. This is not an AI model-generated arbitrary application.';
  }

  function run() {
    if(!currentHTML) currentHTML=$('vexBuilderCode').value;
    $('vexBuilderFrame').srcdoc=currentHTML;
  }

  function check() {
    let s=$('vexBuilderCode').value||currentHTML;
    let issues=[];
    if(!s.trim())issues.push('No code generated.');
    if(!/<html[\s>]/i.test(s))issues.push('HTML root element not found.');
    if(!/<\/html>/i.test(s))issues.push('Closing HTML tag not found.');
    if(!/<meta[^>]+viewport/i.test(s))issues.push('Mobile viewport meta tag missing.');
    if(!/<style[\s>]/i.test(s))issues.push('No CSS style block found.');
    if(!/<script[\s>]/i.test(s))issues.push('No JavaScript block found.');

    $('vexBuilderStatus').textContent=issues.length
      ? 'Static checks found:\n• '+issues.join('\n• ')
      : 'Basic static checks passed. These checks do not prove that every feature works; test the preview manually.';
  }

  function download(name,blob) {
    let a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download=name;
    a.click();
    setTimeout(()=>URL.revokeObjectURL(a.href),1000);
  }

  function zip() {
    let html=$('vexBuilderCode').value||currentHTML;
    if(!html){
      $('vexBuilderStatus').textContent='Generate a project first.';
      return;
    }
    if(!window.JSZip){
      $('vexBuilderStatus').textContent='ZIP library unavailable. Use Download HTML instead.';
      return;
    }
    let z=new JSZip();
    z.file('index.html',html);
    z.file('README.txt',
      'VEX AI browser project\nOpen index.html in a modern browser.\nThis project has no backend unless separately added.'
    );
    z.generateAsync({type:'blob'})
      .then(b=>download('vex-project.zip',b))
      .catch(e=>$('vexBuilderStatus').textContent='ZIP error: '+e.message);
  }

  function open() {
    overlay.classList.add('open');
    $('vexBuilderPrompt').focus();
  }

  const launch=document.createElement('button');
  launch.id='vexBuilderLaunch';
  launch.textContent='Code Builder';
  launch.onclick=open;

  const top=document.querySelector('.topbar');
  if(top)top.appendChild(launch);
  else document.body.appendChild(launch);

  $('vexBuilderClose').onclick=()=>overlay.classList.remove('open');
  $('vexBuilderGenerate').onclick=generate;
  $('vexBuilderRun').onclick=()=>{
    currentHTML=$('vexBuilderCode').value;
    run();
  };
  $('vexBuilderCheck').onclick=check;
  $('vexBuilderCopy').onclick=()=>{
    navigator.clipboard.writeText($('vexBuilderCode').value)
      .then(()=>$('vexBuilderStatus').textContent='HTML copied.')
      .catch(()=>$('vexBuilderStatus').textContent='Copy failed; select and copy the code manually.');
  };
  $('vexBuilderDownload').onclick=()=>download(
    'vex-project.html',
    new Blob([$('vexBuilderCode').value||currentHTML],{type:'text/html'})
  );
  $('vexBuilderZip').onclick=zip;

  const zipLib=document.createElement('script');
  zipLib.src='https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js';
  zipLib.async=true;
  document.head.appendChild(zipLib);
})();
