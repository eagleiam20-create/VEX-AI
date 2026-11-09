
(() => {
  "use strict";

  if (window.__VEX_BUILDER_LOADED__) return;

  function initVEXBuilder() {
    if (window.__VEX_BUILDER_LOADED__) return;
    window.__VEX_BUILDER_LOADED__ = true;

    const css = `
    #vexBuilderLaunch {
      position:relative;
      z-index:20;
      margin-left:auto;
      background:#fff;
      color:#000;
      border:0;
      border-radius:12px;
      padding:10px 16px;
      font-size:13px;
      font-weight:800;
      cursor:pointer;
    }

    #vexBuilderOverlay {
      position:fixed;
      inset:0;
      z-index:99999;
      display:none;
      flex-direction:column;
      background:#000;
      color:#fff;
      font-family:Arial,sans-serif;
    }

    #vexBuilderOverlay.open {display:flex}

    #vexBuilderHead {
      min-height:58px;
      padding:10px 16px;
      display:flex;
      align-items:center;
      gap:12px;
      border-bottom:1px solid #292929;
      background:#050505;
    }

    #vexBuilderHead strong {
      font-size:15px;
      letter-spacing:1px;
    }

    #vexBuilderHead button,
    #vexBuilderActions button {
      background:#111;
      color:#fff;
      border:1px solid #333;
      border-radius:9px;
      padding:10px 13px;
      cursor:pointer;
    }

    #vexBuilderHead button:hover,
    #vexBuilderActions button:hover {
      background:#252525;
    }

    #vexBuilderBody {
      display:grid;
      grid-template-columns:310px minmax(0,1fr);
      flex:1;
      min-height:0;
    }

    #vexBuilderSide {
      padding:18px;
      overflow-y:auto;
      border-right:1px solid #292929;
      background:#050505;
    }

    #vexBuilderSide h2 {
      font-size:20px;
      margin:0 0 8px;
    }

    #vexBuilderSide p {
      color:#999;
      font-size:12px;
      line-height:1.7;
    }

    #vexBuilderSide label {
      display:block;
      font-size:12px;
      color:#bbb;
      margin:16px 0 7px;
    }

    #vexBuilderPrompt {
      width:100%;
      min-height:145px;
      resize:vertical;
      padding:12px;
      box-sizing:border-box;
      background:#101010;
      color:white;
      border:1px solid #333;
      border-radius:10px;
      outline:none;
      font:13px/1.6 Arial;
    }

    #vexBuilderPrompt:focus {
      border-color:#888;
    }

    #vexBuilderGenerate {
      width:100%;
      margin-top:12px;
      padding:13px;
      background:#fff;
      color:#000;
      border:0;
      border-radius:10px;
      font-weight:800;
      cursor:pointer;
    }

    #vexBuilderTemplates {
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:8px;
      margin-top:15px;
    }

    #vexBuilderTemplates button {
      background:#101010;
      color:#ddd;
      border:1px solid #303030;
      padding:10px 5px;
      border-radius:9px;
      font-size:11px;
      cursor:pointer;
    }

    #vexBuilderStatus {
      margin-top:15px;
      padding:12px;
      background:#101010;
      border:1px solid #292929;
      border-radius:9px;
      color:#aaa;
      font-size:12px;
      line-height:1.7;
      white-space:pre-wrap;
      overflow-wrap:anywhere;
    }

    #vexBuilderPreview {
      display:flex;
      flex-direction:column;
      min-width:0;
      min-height:0;
      padding:12px;
      gap:10px;
      background:#000;
    }

    #vexBuilderActions {
      display:flex;
      flex-wrap:wrap;
      gap:7px;
    }

    #vexBuilderFrame {
      width:100%;
      flex:1;
      min-height:220px;
      background:white;
      border:1px solid #333;
      border-radius:10px;
    }

    #vexBuilderCode {
      width:100%;
      height:190px;
      box-sizing:border-box;
      resize:vertical;
      background:#080808;
      color:#ddd;
      border:1px solid #333;
      border-radius:10px;
      padding:12px;
      outline:none;
      font:12px/1.5 Consolas,monospace;
    }

    #vexBuilderCode:focus {border-color:#888}

    @media(max-width:760px) {
      #vexBuilderHead span {display:none!important}
      #vexBuilderBody {
        grid-template-columns:1fr;
        grid-template-rows:auto minmax(0,1fr);
      }
      #vexBuilderSide {
        border-right:0;
        border-bottom:1px solid #292929;
        max-height:38vh;
        padding:13px;
      }
      #vexBuilderSide h2 {font-size:17px}
      #vexBuilderPrompt {min-height:85px}
      #vexBuilderPreview {padding:8px}
      #vexBuilderFrame {min-height:180px}
      #vexBuilderCode {height:140px}
      #vexBuilderActions button {
        padding:8px 9px;
        font-size:11px;
      }
    }`;

    const style = document.createElement("style");
    style.id = "vexBuilderStyles";
    style.textContent = css;
    document.head.appendChild(style);

    const overlay = document.createElement("section");
    overlay.id = "vexBuilderOverlay";

    overlay.innerHTML = `
      <header id="vexBuilderHead">
        <strong>VEX AI / CODE BUILDER</strong>
        <span style="color:#777;font-size:11px">
          Project Studio
        </span>
        <span style="flex:1"></span>
        <button id="vexBuilderClose">Close ×</button>
      </header>

      <div id="vexBuilderBody">

        <aside id="vexBuilderSide">
          <h2>Create your project</h2>
          <p>
            Describe the app or website you want to build.
            Generate a starter project and test it in the preview.
          </p>

          <label for="vexBuilderPrompt">PROJECT DESCRIPTION</label>

          <textarea id="vexBuilderPrompt"
            placeholder="Example: Make a modern todo app with add, delete, complete tasks and save them automatically."></textarea>

          <button id="vexBuilderGenerate">
            Generate project
          </button>

          <label>QUICK TEMPLATES</label>

          <div id="vexBuilderTemplates">
            <button data-template="calculator">Calculator</button>
            <button data-template="todo">Todo App</button>
            <button data-template="notes">Notes App</button>
            <button data-template="quiz">Quiz App</button>
            <button data-template="expense">Expense Tracker</button>
            <button data-template="portfolio">Portfolio</button>
            <button data-template="landing">Website</button>
            <button data-template="dashboard">Dashboard</button>
          </div>

          <div id="vexBuilderStatus">
            Ready. Describe a project or select a template.
          </div>
        </aside>

        <main id="vexBuilderPreview">

          <div id="vexBuilderActions">
            <button id="vexBuilderRun">▶ Run</button>
            <button id="vexBuilderCheck">Check</button>
            <button id="vexBuilderCopy">Copy</button>
            <button id="vexBuilderDownload">Download HTML</button>
            <button id="vexBuilderZip">Download ZIP</button>
            <button id="vexBuilderReset">Reset</button>
          </div>

          <iframe
            id="vexBuilderFrame"
            title="VEX project preview"
            sandbox="allow-scripts allow-forms">
          </iframe>

          <textarea
            id="vexBuilderCode"
            spellcheck="false"
            placeholder="Your project code will appear here...">
          </textarea>

        </main>
      </div>
    `;

    document.body.appendChild(overlay);

    const $ = id => document.getElementById(id);

    let currentHTML = "";
    let projectName = "vex-project";

    function status(message) {
      $("vexBuilderStatus").textContent = message;
    }

    function escapeHTML(value) {
      return String(value).replace(/[&<>"']/g, c => ({
        "&":"&amp;",
        "<":"&lt;",
        ">":"&gt;",
        '"':"&quot;",
        "'":"&#39;"
      })[c]);
    }

    function shell(title, body, script = "") {
      return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHTML(title)}</title>
<style>
*{box-sizing:border-box}
body{
 margin:0;
 padding:20px;
 background:#f4f5f7;
 color:#171717;
 font:15px Arial,sans-serif
}
main{
 max-width:900px;
 margin:20px auto;
 background:white;
 padding:24px;
 border-radius:16px;
 box-shadow:0 5px 25px #0001
}
h1{margin-top:0}
button{
 background:#171717;
 color:white;
 border:0;
 padding:10px 15px;
 border-radius:8px;
 cursor:pointer
}
button:hover{opacity:.8}
input,textarea,select{
 max-width:100%;
 padding:11px;
 border:1px solid #ccc;
 border-radius:8px;
 font:inherit
}
input[type=checkbox],input[type=radio]{max-width:none}
.row{
 display:flex;
 flex-wrap:wrap;
 gap:9px;
 margin:12px 0
}
.row input{flex:1;min-width:120px}
.muted{color:#777}
.item{
 padding:12px;
 border:1px solid #ddd;
 border-radius:9px;
 margin:9px 0;
 overflow-wrap:anywhere
}
.grid{
 display:grid;
 grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
 gap:12px
}
.card{
 padding:18px;
 background:#f1f2f5;
 border-radius:12px
}
.stat{
 font-size:27px;
 font-weight:bold;
 margin:8px 0
}
@media(max-width:600px){
 body{padding:7px}
 main{padding:16px;margin:5px auto}
}
</style>
</head>
<body>
<main>
${body}
</main>
<script>${script}<\/script>
</body>
</html>`;
    }

    function calculator() {
      return shell("VEX Calculator", `
        <h1>Calculator</h1>
        <input id="display" value="0" readonly
          style="width:100%;font-size:28px;text-align:right;margin-bottom:12px">
        <div class="grid" id="keys">
          ${["7","8","9","÷","4","5","6","×","1","2","3","−","0",".","=","+","C"].map(k =>
            `<button data-key="${k}" style="padding:19px;font-size:18px">${k}</button>`
          ).join("")}
        </div>
        <p class="muted">Basic calculator</p>
      `, `
        let expression = "";
        const display = document.getElementById("display");

        document.getElementById("keys").addEventListener("click",e=>{
          const button=e.target.closest("[data-key]");
          if(!button)return;
          const key=button.dataset.key;

          if(key==="C"){
            expression="";
          } else if(key==="="){
            try{
              const safe=expression
                .replace(/×/g,"*")
                .replace(/÷/g,"/")
                .replace(/−/g,"-");

              if(!safe || !/^[0-9+*/.() -]+$/.test(safe))
                throw Error("Invalid expression");

              const result=Function('"use strict";return ('+safe+')')();

              if(!Number.isFinite(result))throw Error("Invalid result");
              expression=String(Number(result.toFixed(10)));
            }catch{
              expression="";
              display.value="Error";
              return;
            }
          }else{
            expression+=key;
          }

          display.value=expression||"0";
        });
      `);
    }

    function todo() {
      return shell("VEX Todo", `
        <h1>My Tasks</h1>
        <p class="muted">Tasks are saved automatically on this device.</p>
        <div class="row">
          <input id="task" placeholder="Write a task">
          <button id="add">Add task</button>
        </div>
        <div id="list"></div>
        <p id="count" class="muted"></p>
      `, `
        const input=document.getElementById("task");
        const list=document.getElementById("list");
        const KEY="vex_builder_todo";
        let tasks=[];

        try{tasks=JSON.parse(localStorage.getItem(KEY)||"[]")}catch{}

        function save(){
          try{localStorage.setItem(KEY,JSON.stringify(tasks))}catch{}
        }

        function render(){
          list.replaceChildren();

          tasks.forEach((task,index)=>{
            const row=document.createElement("div");
            row.className="item";

            const check=document.createElement("input");
            check.type="checkbox";
            check.checked=task.done;
            check.onchange=()=>{
              tasks[index].done=check.checked;
              save();
              render();
            };

            const text=document.createElement("span");
            text.textContent=" "+task.text;
            text.style.textDecoration=task.done?"line-through":"none";

            const del=document.createElement("button");
            del.textContent="Delete";
            del.style.float="right";
            del.onclick=()=>{
              tasks.splice(index,1);
              save();
              render();
            };

            row.append(check,text,del);
            list.append(row);
          });

          document.getElementById("count").textContent=
            tasks.filter(t=>t.done).length+" completed / "+tasks.length+" total";
        }

        function add(){
          const text=input.value.trim();
          if(!text)return;
          tasks.push({text,done:false});
          input.value="";
          save();
          render();
        }

        document.getElementById("add").onclick=add;
        input.addEventListener("keydown",e=>{
          if(e.key==="Enter")add();
        });

        render();
      `);
    }

    function notes() {
      return shell("VEX Notes", `
        <h1>My Notes</h1>
        <textarea id="note" placeholder="Write something..."
          style="width:100%;min-height:260px"></textarea>
        <div class="row">
          <button id="save">Save notes</button>
          <button id="clear">Clear</button>
        </div>
        <p id="message" class="muted">Your notes stay in this browser.</p>
      `, `
        const note=document.getElementById("note");
        const KEY="vex_builder_notes";

        try{note.value=localStorage.getItem(KEY)||""}catch{}

        document.getElementById("save").onclick=()=>{
          try{
            localStorage.setItem(KEY,note.value);
            document.getElementById("message").textContent="Saved successfully.";
          }catch{
            document.getElementById("message").textContent="Could not save notes.";
          }
        };

        document.getElementById("clear").onclick=()=>{
          if(!confirm("Clear all notes?"))return;
          note.value="";
          localStorage.removeItem(KEY);
          document.getElementById("message").textContent="Notes cleared.";
        };
      `);
    }

    function expense() {
      return shell("VEX Expense Tracker", `
        <h1>Expense Tracker</h1>
        <p class="muted">Track your spending.</p>
        <div class="row">
          <input id="name" placeholder="Expense name">
          <input id="amount" type="number" min="0" step="0.01" placeholder="Amount">
          <button id="add">Add</button>
        </div>
        <div class="card">
          <div class="muted">TOTAL EXPENSE</div>
          <div class="stat">₹<span id="total">0.00</span></div>
        </div>
        <h3>Transactions</h3>
        <div id="items"></div>
      `, `
        const KEY="vex_builder_expenses";
        let rows=[];
        try{rows=JSON.parse(localStorage.getItem(KEY)||"[]")}catch{}

        function save(){
          try{localStorage.setItem(KEY,JSON.stringify(rows))}catch{}
        }

        function render(){
          const box=document.getElementById("items");
          box.replaceChildren();

          rows.forEach((r,i)=>{
            const item=document.createElement("div");
            item.className="item";

            const label=document.createElement("span");
            label.textContent=r.name+" — ₹"+Number(r.amount).toFixed(2);

            const del=document.createElement("button");
            del.textContent="Delete";
            del.style.float="right";
            del.onclick=()=>{
              rows.splice(i,1);
              save();
              render();
            };

            item.append(label,del);
            box.append(item);
          });

          document.getElementById("total").textContent=
            rows.reduce((sum,r)=>sum+Number(r.amount),0).toFixed(2);
        }

        document.getElementById("add").onclick=()=>{
          const name=document.getElementById("name").value.trim();
          const amount=Number(document.getElementById("amount").value);

          if(!name||!Number.isFinite(amount)||amount<=0){
            alert("Enter a name and valid amount.");
            return;
          }

          rows.push({name,amount});
          document.getElementById("name").value="";
          document.getElementById("amount").value="";
          save();
          render();
        };

        render();
      `);
    }

    function quiz() {
      return shell("VEX Quiz", `
        <h1>General Knowledge Quiz</h1>
        <p id="progress" class="muted"></p>
        <div id="question"></div>
        <div id="options"></div>
        <button id="next">Start quiz</button>
        <h3 id="result"></h3>
      `, `
        const questions=[
          {q:"Which planet is known as the Red Planet?",a:["Earth","Mars","Venus","Jupiter"],c:1},
          {q:"How many days are in a week?",a:["5","6","7","8"],c:2},
          {q:"Which is the largest ocean?",a:["Atlantic","Indian","Arctic","Pacific"],c:3},
          {q:"What is 12 × 5?",a:["50","60","70","80"],c:1},
          {q:"Which language runs in a web browser?",a:["JavaScript","Python only","C only","SQL"],c:0}
        ];

        let index=-1,score=0,selected=null;

        function show(){
          const q=questions[index];
          document.getElementById("progress").textContent=
            "Question "+(index+1)+" of "+questions.length;

          document.getElementById("question").textContent=q.q;
          const options=document.getElementById("options");
          options.replaceChildren();
          selected=null;

          q.a.forEach((answer,i)=>{
            const label=document.createElement("label");
            label.className="item";
            label.style.display="block";

            const radio=document.createElement("input");
            radio.type="radio";
            radio.name="answer";
            radio.value=i;
            radio.onchange=()=>selected=i;

            label.append(radio,document.createTextNode(" "+answer));
            options.append(label);
          });

          document.getElementById("next").textContent=
            index===questions.length-1?"Finish":"Next";
        }

        document.getElementById("next").onclick=()=>{
          if(index===-1){
            index=0;
            show();
            return;
          }

          if(selected===null){
            alert("Choose an answer first.");
            return;
          }

          if(selected===questions[index].c)score++;
          index++;

          if(index>=questions.length){
            document.getElementById("question").textContent="Quiz completed!";
            document.getElementById("options").replaceChildren();
            document.getElementById("progress").textContent="Finished";
            document.getElementById("next").style.display="none";
            document.getElementById("result").textContent=
              "Your score: "+score+" / "+questions.length;
          }else show();
        };
      `);
    }

    function portfolio() {
      return shell("My Portfolio", `
        <nav class="row">
          <strong>MY PORTFOLIO</strong>
          <span class="muted">Home · About · Projects · Contact</span>
        </nav>
        <section style="padding:45px 5px">
          <p class="muted">HELLO, I'M</p>
          <h1 style="font-size:40px">Your Name</h1>
          <h2>Developer & Creative Thinker</h2>
          <p class="muted">I build useful digital experiences.</p>
          <button onclick="document.getElementById('contact').scrollIntoView()">Contact me</button>
        </section>
        <h2>About me</h2>
        <p>Write your introduction here.</p>
        <h2>My projects</h2>
        <div class="grid">
          <div class="card">Project One</div>
          <div class="card">Project Two</div>
          <div class="card">Project Three</div>
        </div>
        <h2 id="contact">Contact</h2>
        <p>Email: hello@example.com</p>
      `);
    }

    function landing() {
      return shell("Website", `
        <nav class="row">
          <strong>YOUR BRAND</strong>
          <span class="muted">Home · Features · Contact</span>
        </nav>
        <section style="text-align:center;padding:55px 5px">
          <h1 style="font-size:40px">Build Something Amazing</h1>
          <p class="muted">A responsive website for your idea.</p>
          <button onclick="document.getElementById('features').scrollIntoView()">Explore</button>
        </section>
        <h2 id="features">Features</h2>
        <div class="grid">
          <div class="card"><h3>Simple</h3><p>Easy to use.</p></div>
          <div class="card"><h3>Fast</h3><p>Lightweight design.</p></div>
          <div class="card"><h3>Responsive</h3><p>Mobile friendly.</p></div>
        </div>
        <h2>Contact</h2>
        <p>contact@example.com</p>
      `);
    }

    function dashboard() {
      return shell("VEX Dashboard", `
        <h1>Dashboard</h1>
        <p class="muted">Your project overview</p>
        <div class="grid">
          <div class="card">
            <div class="muted">Visitors</div>
            <div class="stat">1,250</div>
          </div>
          <div class="card">
            <div class="muted">Orders</div>
            <div class="stat">86</div>
          </div>
          <div class="card">
            <div class="muted">Revenue</div>
            <div class="stat">₹24,500</div>
          </div>
        </div>
        <h2>Recent activity</h2>
        <div class="item">Project created</div>
        <div class="item">Dashboard updated</div>
        <div class="item">Welcome to VEX Builder</div>
      `);
    }

    const builders = {
      calculator,
      todo,
      notes,
      expense,
      quiz,
      portfolio,
      landing,
      dashboard
    };

    function createProject(type, prompt = "") {
      if (!builders[type]) {
        status("Unknown template.");
        return;
      }

      currentHTML = builders[type]();
      projectName = "vex-" + type;

      $("vexBuilderCode").value = currentHTML;
      runPreview();

      status(
        "Project created: " + type +
        "\\n\\nPreview is ready. You can edit the HTML code below, run it again, and download it."
      );
    }

    function detectTemplate(prompt) {
      const p = prompt.toLowerCase();

      if (/calculator|calculate|math app/.test(p)) return "calculator";
      if (/todo|to-do|task list|task manager/.test(p)) return "todo";
      if (/notes app|note taking|notepad/.test(p)) return "notes";
      if (/expense|budget tracker|spending tracker/.test(p)) return "expense";
      if (/quiz|mcq|question app/.test(p)) return "quiz";
      if (/portfolio|personal website|resume website/.test(p)) return "portfolio";
      if (/landing page|business website|company website/.test(p)) return "landing";
      if (/dashboard|admin panel|analytics panel/.test(p)) return "dashboard";

      return null;
    }

    function generate() {
      const prompt = $("vexBuilderPrompt").value.trim();

      if (!prompt) {
        status("Please describe your project first.");
        return;
      }

      const type = detectTemplate(prompt);

      if (type) {
        createProject(type);
      } else {
        currentHTML = shell(
          "VEX Project Starter",
          `
            <h1>Project Starter</h1>
            <p class="muted">Your requested project idea:</p>
            <div class="item">${escapeHTML(prompt)}</div>
            <h2>Starter structure</h2>
            <div class="grid">
              <div class="card">Home screen</div>
              <div class="card">Main feature</div>
              <div class="card">Settings</div>
            </div>
            <p>
              This is a starter layout. Custom features still need to be implemented.
            </p>
          `
        );

        projectName = "vex-project";
        $("vexBuilderCode").value = currentHTML;
        runPreview();

        status(
          "Created a basic project starter. This idea does not match a built-in functional template yet."
        );
      }
    }

    function runPreview() {
      const code = $("vexBuilderCode").value.trim();

      if (!code) {
        status("There is no code to preview.");
        return;
      }

      currentHTML = code;
      $("vexBuilderFrame").srcdoc = code;
      status("Preview updated.");
    }

    function checkCode() {
      const code = $("vexBuilderCode").value;
      const issues = [];

      if (!code.trim()) issues.push("No code found.");
      if (!/<html[\s>]/i.test(code)) issues.push("HTML root missing.");
      if (!/<\/html>/i.test(code)) issues.push("Closing HTML tag missing.");
      if (!/<body[\s>]/i.test(code)) issues.push("Body tag missing.");
      if (!/<meta[^>]+viewport/i.test(code)) issues.push("Mobile viewport missing.");

      if (issues.length) {
        status("Code checks found:\\n• " + issues.join("\\n• "));
      } else {
        status(
          "Basic HTML checks passed.\\n\\nThese checks do not guarantee that every feature works. Test the preview manually."
        );
      }
    }

    async function copyCode() {
      const code = $("vexBuilderCode").value;

      if (!code) {
        status("Generate a project first.");
        return;
      }

      try {
        await navigator.clipboard.writeText(code);
        status("Code copied successfully.");
      } catch {
        $("vexBuilderCode").focus();
        $("vexBuilderCode").select();

        try {
          document.execCommand("copy");
          status("Code copied.");
        } catch {
          status("Copy unavailable. Select the code and copy manually.");
        }
      }
    }

    function downloadFile(name, content, type) {
      const blob = new Blob([content], {type});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");

      a.href = url;
      a.download = name;
      document.body.appendChild(a);
      a.click();
      a.remove();

      setTimeout(() => URL.revokeObjectURL(url), 1500);
    }

    function downloadHTML() {
      const code = $("vexBuilderCode").value;

      if (!code) {
        status("Generate a project first.");
        return;
      }

      downloadFile(projectName + ".html", code, "text/html;charset=utf-8");
      status("HTML download started.");
    }

    async function downloadZIP() {
      const code = $("vexBuilderCode").value;

      if (!code) {
        status("Generate a project first.");
        return;
      }

      status("Preparing ZIP file...");

      try {
        if (!window.JSZip) {
          await new Promise((resolve, reject) => {
            const existing = document.querySelector(
              'script[data-vex-jszip="true"]'
            );

            if (existing) {
              if (window.JSZip) return resolve();
              existing.addEventListener("load", resolve, {once:true});
              existing.addEventListener("error", reject, {once:true});
              return;
            }

            const script = document.createElement("script");
            script.src =
              "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js";
            script.dataset.vexJszip = "true";
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
          });
        }

        if (!window.JSZip) throw Error("ZIP library did not load.");

        const zip = new JSZip();

        zip.file("index.html", code);
        zip.file(
          "README.txt",
          "VEX AI Project\\n\\nOpen index.html in a modern browser.\\nThis is a browser-only project unless you add a backend."
        );

        const blob = await zip.generateAsync({type:"blob"});

        downloadFile("vex-project.zip", blob, "application/zip");
        status("ZIP download started.");
      } catch (error) {
        status("ZIP error: " + error.message + "\\nTry Download HTML instead.");
      }
    }

    function openBuilder() {
      overlay.classList.add("open");
      document.body.style.overflow = "hidden";
      $("vexBuilderPrompt").focus();
    }

    function closeBuilder() {
      overlay.classList.remove("open");
      document.body.style.overflow = "";
    }

    const launch = document.createElement("button");
    launch.id = "vexBuilderLaunch";
    launch.textContent = "Code Builder";
    launch.addEventListener("click", openBuilder);

    const topbar = document.querySelector(".topbar");

    if (topbar) {
      topbar.appendChild(launch);
    } else {
      launch.style.position = "fixed";
      launch.style.top = "12px";
      launch.style.right = "12px";
      document.body.appendChild(launch);
    }

    $("vexBuilderClose").onclick = closeBuilder;
    $("vexBuilderGenerate").onclick = generate;
    $("vexBuilderRun").onclick = runPreview;
    $("vexBuilderCheck").onclick = checkCode;
    $("vexBuilderCopy").onclick = copyCode;
    $("vexBuilderDownload").onclick = downloadHTML;
    $("vexBuilderZip").onclick = downloadZIP;

    $("vexBuilderReset").onclick = () => {
      $("vexBuilderCode").value = "";
      $("vexBuilderFrame").srcdoc = "";
      currentHTML = "";
      status("Builder reset. Create a new project.");
    };

    $("vexBuilderTemplates").addEventListener("click", e => {
      const button = e.target.closest("[data-template]");
      if (!button) return;
      createProject(button.dataset.template);
    });

    $("vexBuilderCode").addEventListener("input", () => {
      status("Code edited. Press Run to update the preview.");
    });

    $("vexBuilderPrompt").addEventListener("keydown", e => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") generate();
    });

    window.addEventListener("keydown", e => {
      if (e.key === "Escape" && overlay.classList.contains("open")) {
        closeBuilder();
      }
    });

    console.log("VEX Code Builder loaded successfully.");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initVEXBuilder, {once:true});
  } else {
    initVEXBuilder();
  }
})();
