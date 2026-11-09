
/* =====================================================
   VEX AI CODE BUILDER V2
   Browser-only builder | No external AI API or model
   Works with the existing VEX index.html
===================================================== */

(function () {
  "use strict";

  const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

  let building = false;

  // ---------- CODING KNOWLEDGE SEARCH ----------

  async function researchCoding(prompt) {
    const queries = [
      prompt + " web development implementation",
      prompt + " JavaScript HTML CSS documentation",
      "MDN Web Docs JavaScript HTML CSS"
    ];

    const sources = [];
    const seen = new Set();

    for (const query of queries) {
      try {
        const data = await searchWeb(query);
        const results = extractResults(data);

        for (const item of results.slice(0, 5)) {
          if (!item.url || seen.has(item.url)) continue;
          seen.add(item.url);

          let context = null;

          if (item.url.startsWith("http")) {
            context = await getPageContext(item.url);
          }

          sources.push({
            title: item.title || "Coding resource",
            url: item.url,
            description: item.description || "",
            context: context?.summary || context?.content?.slice(0, 1200) || ""
          });

          if (sources.length >= 8) break;
        }
      } catch (error) {
        console.warn("Coding research:", error);
      }

      if (sources.length >= 8) break;
    }

    return sources;
  }

  // ---------- PROJECT GENERATORS ----------

  function makeQuizApp() {
    return {
      name: "Quiz App",
      html: `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quiz App</title>
</head>
<body>
<main class="quiz">
  <header>
    <h1>Knowledge Quiz</h1>
    <p>Test your knowledge.</p>
  </header>
  <div id="progress">Question 1 of 5</div>
  <h2 id="question"></h2>
  <div id="answers"></div>
  <p id="feedback"></p>
  <button id="next" hidden>Next question</button>
  <div id="result" hidden></div>
  <button id="restart" hidden>Restart quiz</button>
</main>
</body>
</html>`,
      css: `
*{box-sizing:border-box}
body{margin:0;background:#101827;color:white;font-family:Arial;min-height:100vh;display:grid;place-items:center;padding:15px}
.quiz{width:min(550px,100%);background:#1d293b;padding:28px;border-radius:18px;box-shadow:0 15px 50px #0006}
header p{color:#aab7c9}
#progress{color:#aab7c9;margin:25px 0 12px}
#answers{display:grid;gap:10px;margin:20px 0}
.answer{background:#34445d;text-align:left;width:100%;border:1px solid #53647d}
.answer:hover{background:#465c7b}
.answer:disabled{opacity:.8}
button{border:0;border-radius:9px;padding:13px;color:white;background:#3978e8;cursor:pointer}
#feedback{min-height:25px}
#result{font-size:22px;margin:20px 0}
`,
      js: `
const questions=[
 {q:"Which language structures a web page?",a:["HTML","Python","SQL","C"],correct:0},
 {q:"Which language styles web pages?",a:["Java","CSS","PHP","C++"],correct:1},
 {q:"Which language adds browser interactivity?",a:["JavaScript","HTML","CSS","XML"],correct:0},
 {q:"Which HTML tag creates a link?",a:["<link>","<a>","<href>","<url>"],correct:1},
 {q:"Which method selects an element by ID?",a:["getElementById","queryAll","findID","selectID"],correct:0}
];
let index=0,score=0,answered=false;
const $=id=>document.getElementById(id);
function render(){
 answered=false;
 $("progress").textContent="Question "+(index+1)+" of "+questions.length;
 $("question").textContent=questions[index].q;
 $("feedback").textContent="";
 $("next").hidden=true;
 $("answers").innerHTML="";
 questions[index].a.forEach((answer,i)=>{
   const b=document.createElement("button");
   b.className="answer";
   b.textContent=answer;
   b.onclick=()=>choose(i,b);
   $("answers").appendChild(b);
 });
}
function choose(i,button){
 if(answered)return;
 answered=true;
 const correct=questions[index].correct;
 if(i===correct){score++;$("feedback").textContent="Correct!";}
 else{$("feedback").textContent="Incorrect. Correct answer: "+questions[index].a[correct];}
 document.querySelectorAll(".answer").forEach((b,j)=>{
   b.disabled=true;
   if(j===correct)b.style.borderColor="#50d890";
 });
 $("next").hidden=false;
}
$("next").onclick=()=>{
 index++;
 if(index>=questions.length){
   $("question").textContent="Quiz completed!";
   $("answers").innerHTML="";
   $("progress").textContent="Finished";
   $("feedback").textContent="";
   $("next").hidden=true;
   $("result").hidden=false;
   $("result").textContent="Your score: "+score+" / "+questions.length;
   $("restart").hidden=false;
 }else render();
};
$("restart").onclick=()=>{
 index=0;score=0;
 $("result").hidden=true;
 $("restart").hidden=true;
 render();
};
render();
`
    };
  }

  function makeExpenseApp() {
    return {
      name: "Expense Tracker",
      html: `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Expense Tracker</title>
</head>
<body>
<main class="container">
 <h1>Expense Tracker</h1>
 <section class="summary">
  <span>Total expenses</span>
  <strong id="total">₹0</strong>
 </section>
 <form id="expenseForm">
  <input id="expenseName" placeholder="Expense name" required>
  <input id="expenseAmount" type="number" min="0.01" step="0.01" placeholder="Amount (₹)" required>
  <button type="submit">Add expense</button>
 </form>
 <h2>History</h2>
 <div id="expenseList"></div>
 <button id="clearAll" class="secondary">Clear all</button>
</main>
</body>
</html>`,
      css: `
*{box-sizing:border-box}
body{margin:0;background:#f2f4f8;font-family:Arial;color:#202938;padding:18px}
.container{max-width:650px;margin:30px auto;background:white;padding:25px;border-radius:17px;box-shadow:0 8px 35px #0001}
.summary{background:#172d4b;color:white;padding:20px;border-radius:12px;display:flex;justify-content:space-between;align-items:center}
.summary strong{font-size:25px}
form{display:grid;gap:10px;margin:20px 0}
input{padding:13px;border:1px solid #ccd3df;border-radius:8px;width:100%}
button{padding:12px;border:0;border-radius:8px;background:#2469dc;color:white;cursor:pointer}
.secondary{background:#555;margin-top:15px}
.expense{display:flex;justify-content:space-between;align-items:center;gap:10px;border-bottom:1px solid #eee;padding:13px 0}
.expense button{background:#b52c39;padding:8px}
`,
      js: `
const $=id=>document.getElementById(id);
let expenses=[];
try{expenses=JSON.parse(localStorage.getItem("vex_expenses")||"[]");if(!Array.isArray(expenses))expenses=[];}catch(e){expenses=[]}
function save(){localStorage.setItem("vex_expenses",JSON.stringify(expenses));render()}
function render(){
 const total=expenses.reduce((sum,x)=>sum+x.amount,0);
 $("total").textContent="₹"+total.toFixed(2);
 $("expenseList").innerHTML="";
 if(!expenses.length){$("expenseList").textContent="No expenses added yet.";return}
 expenses.forEach((item,index)=>{
  const row=document.createElement("div");
  row.className="expense";
  const label=document.createElement("span");
  label.textContent=item.name+" — ₹"+item.amount.toFixed(2);
  const remove=document.createElement("button");
  remove.textContent="Delete";
  remove.onclick=()=>{expenses.splice(index,1);save()};
  row.append(label,remove);
  $("expenseList").appendChild(row);
 });
}
$("expenseForm").addEventListener("submit",e=>{
 e.preventDefault();
 const name=$("expenseName").value.trim();
 const amount=Number($("expenseAmount").value);
 if(!name||!Number.isFinite(amount)||amount<=0)return;
 expenses.push({name,amount});
 $("expenseName").value="";
 $("expenseAmount").value="";
 save();
});
$("clearAll").onclick=()=>{
 if(!confirm("Delete all expenses?"))return;
 expenses=[];save();
};
render();
`
    };
  }

  function makeLandingPage(prompt) {
    const title = prompt
      .replace(/^(please\s+)?(build|create|make)\s+/i, "")
      .slice(0, 65) || "My Website";

    return {
      name: "Landing Page",
      html: `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHTML(title)}</title>
</head>
<body>
<nav><strong>${escapeHTML(title)}</strong><a href="#features">Features</a><a href="#about">About</a><a href="#contact">Contact</a></nav>
<section class="hero">
 <p class="tag">WELCOME</p>
 <h1>${escapeHTML(title)}</h1>
 <p>A clean, responsive website designed to introduce your idea.</p>
 <a class="cta" href="#features">Explore</a>
</section>
<section id="features">
 <h2>Features</h2>
 <div class="grid">
  <article><h3>Simple</h3><p>Easy-to-understand experience.</p></article>
  <article><h3>Responsive</h3><p>Designed for mobile and desktop.</p></article>
  <article><h3>Modern</h3><p>A clean and accessible layout.</p></article>
 </div>
</section>
<section id="about"><h2>About</h2><p>Replace this text with information about your project.</p></section>
<section id="contact"><h2>Contact</h2><p>Add your contact details here.</p></section>
<footer>Made with VEX AI</footer>
</body>
</html>`,
      css: `
*{box-sizing:border-box;scroll-behavior:smooth}
body{margin:0;font-family:Arial,sans-serif;color:#20232a}
nav{display:flex;gap:25px;align-items:center;padding:20px 7%;border-bottom:1px solid #eee;flex-wrap:wrap}
nav strong{margin-right:auto}
nav a{color:#444;text-decoration:none}
.hero{padding:100px 8%;background:#101827;color:white;min-height:430px}
.hero h1{font-size:clamp(38px,8vw,76px);max-width:850px;margin:12px 0}
.hero p{color:#c0cad8;line-height:1.7}
.tag{letter-spacing:3px}
.cta{display:inline-block;margin-top:20px;background:white;color:#111;padding:13px 22px;border-radius:8px;text-decoration:none}
section:not(.hero){padding:55px 8%}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:15px}
article{border:1px solid #ddd;border-radius:12px;padding:20px}
footer{background:#101827;color:white;text-align:center;padding:25px}
@media(max-width:600px){.hero{padding:65px 7%}}
`,
      js: `
document.querySelectorAll('nav a').forEach(a=>{
 a.addEventListener('click',()=>{
  const target=document.querySelector(a.getAttribute('href'));
  if(target)target.scrollIntoView({behavior:'smooth'});
 });
});
`
    };
  }

  function buildProject(prompt) {
    const q = prompt.toLowerCase();

    if (q.includes("calculator") || q.includes("calculate")) {
      return calculatorTemplate();
    }

    if (q.includes("quiz") || q.includes("question game")) {
      return makeQuizApp();
    }

    if (q.includes("expense") || q.includes("budget tracker") || q.includes("spending tracker")) {
      return makeExpenseApp();
    }

    if (q.includes("todo") || q.includes("to-do") || q.includes("task list")) {
      return todoTemplate();
    }

    if (q.includes("note") || q.includes("notepad")) {
      return notesTemplate();
    }

    if (q.includes("portfolio") || q.includes("personal website")) {
      return portfolioTemplate();
    }

    if (q.includes("landing page") || q.includes("business website") ||
        q.includes("website") || q.includes("web page")) {
      return makeLandingPage(prompt);
    }

    return genericTemplate(prompt);
  }

  // ---------- PROJECT QUALITY CHECKS ----------

  function checkProject(project) {
    const checks = [];

    checks.push({
      name: "HTML document structure",
      ok: /<html[\s>]/i.test(project.html) &&
          /<\/html>/i.test(project.html) &&
          /<body[\s>]/i.test(project.html)
    });

    checks.push({
      name: "Viewport configuration",
      ok: /name=["']viewport["']/i.test(project.html)
    });

    checks.push({
      name: "CSS is present",
      ok: project.css.trim().length > 20
    });

    checks.push({
      name: "JavaScript syntax",
      ok: (() => {
        try {
          new Function(project.js);
          return true;
        } catch (e) {
          return false;
        }
      })()
    });

    checks.push({
      name: "JavaScript is present",
      ok: project.js.trim().length > 0
    });

    return checks;
  }

  function checkHTML() {
    const html = projectHTML();

    return {
      ok: /<html[\s>]/i.test(html) &&
          /<body[\s>]/i.test(html) &&
          /<\/body>/i.test(html),
      size: html.length
    };
  }

  // ---------- PROJECT ZIP DOWNLOAD ----------

  function crc32(bytes) {
    let crc = -1;

    for (let i = 0; i < bytes.length; i++) {
      crc ^= bytes[i];

      for (let j = 0; j < 8; j++) {
        crc = (crc >>> 1) ^ (crc & 1 ? 0xEDB88320 : 0);
      }
    }

    return (crc ^ -1) >>> 0;
  }

  function zipFiles(files) {
    const encoder = new TextEncoder();
    const local = [];
    const central = [];
    let offset = 0;

    function u16(n) {
      return [n & 255, (n >>> 8) & 255];
    }

    function u32(n) {
      return [
        n & 255,
        (n >>> 8) & 255,
        (n >>> 16) & 255,
        (n >>> 24) & 255
      ];
    }

    for (const file of files) {
      const name = encoder.encode(file.name);
      const data = encoder.encode(file.data);
      const crc = crc32(data);

      const localHeader = new Uint8Array([
        ...u32(0x04034b50),
        ...u16(20),
        ...u16(0),
        ...u16(0),
        ...u16(0),
        ...u16(0),
        ...u32(crc),
        ...u32(data.length),
        ...u32(data.length),
        ...u16(name.length),
        ...u16(0),
        ...name
      ]);

      local.push(localHeader, data);

      const centralHeader = new Uint8Array([
        ...u32(0x02014b50),
        ...u16(20),
        ...u16(20),
        ...u16(0),
        ...u16(0),
        ...u16(0),
        ...u16(0),
        ...u32(crc),
        ...u32(data.length),
        ...u32(data.length),
        ...u16(name.length),
        ...u16(0),
        ...u16(0),
        ...u16(0),
        ...u16(0),
        ...u32(0),
        ...u32(offset),
        ...name
      ]);

      central.push(centralHeader);
      offset += localHeader.length + data.length;
    }

    const centralSize = central.reduce((sum, x) => sum + x.length, 0);

    const end = new Uint8Array([
      ...u32(0x06054b50),
      ...u16(0),
      ...u16(0),
      ...u16(files.length),
      ...u16(files.length),
      ...u32(centralSize),
      ...u32(offset),
      ...u16(0)
    ]);

    return new Blob([...local, ...central, end], {
      type: "application/zip"
    });
  }

  function downloadZIP() {
    const files = [
      {
        name: "index.html",
        data: projectHTML()
      },
      {
        name: "style.css",
        data: codeFiles["style.css"]
      },
      {
        name: "script.js",
        data: codeFiles["script.js"]
      },
      {
        name: "README.txt",
        data:
          projectName + "\n\n" +
          "Created using VEX AI Code Builder.\n" +
          "Open index.html in a modern browser to run this project.\n" +
          "This browser project does not include a hosted backend."
      }
    ];

    const blob = zipFiles(files);
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");

    a.href = url;
    a.download = (projectName || "VEX_Project")
      .replace(/[^a-z0-9_-]/gi, "_") + ".zip";

    document.body.appendChild(a);
    a.click();
    a.remove();

    setTimeout(() => URL.revokeObjectURL(url), 3000);
  }

  // ---------- IMPROVED ARTIFACT ----------

  function improvedArtifactHTML() {
    return `<div class="app-artifact">
      <div class="artifact-header">
        <div class="artifact-title">▣ ${escapeHTML(projectName)}</div>
        <div class="artifact-actions">
          <button class="artifact-btn primary" onclick="runProject()">▶ Run</button>
          <button class="artifact-btn" onclick="openBuildFullscreen()">⛶ Full screen</button>
          <button class="artifact-btn" onclick="toggleCodeFiles()">View Code</button>
          <button class="artifact-btn" onclick="downloadProject()">↓ HTML</button>
          <button class="artifact-btn" onclick="VEXBuilder.downloadZIP()">↓ Project ZIP</button>
        </div>
      </div>
      <iframe class="preview-frame" id="projectPreview"
        sandbox="allow-scripts allow-forms allow-modals"></iframe>
      <div class="code-files" id="codeFiles">
        <div class="code-file-tabs">
          <button class="code-file-tab active" onclick="showCodeFile('index.html',this)">index.html</button>
          <button class="code-file-tab" onclick="showCodeFile('style.css',this)">style.css</button>
          <button class="code-file-tab" onclick="showCodeFile('script.js',this)">script.js</button>
        </div>
        <pre class="code-source" id="codeSource"></pre>
      </div>
    </div>`;
  }

  function renderImprovedArtifact(target) {
    target.insertAdjacentHTML("beforeend", improvedArtifactHTML());
    runProject();
    showCodeFile("index.html", document.querySelector(".code-file-tab"));
    scrollCode();
  }

  // ---------- RESEARCH DISPLAY ----------

  function researchHTML(sources) {
    if (!sources.length) {
      return "<p>No coding references could be retrieved. The project was created using the built-in builder.</p>";
    }

    return `
      <details style="margin:12px 0;color:#aaa">
        <summary style="cursor:pointer">Coding references researched (${sources.length})</summary>
        ${sources.map(source => `
          <a class="search-card" href="${escapeHTML(source.url)}"
             target="_blank" rel="noopener">
            <strong>${escapeHTML(source.title)}</strong>
            <p>${escapeHTML(source.description || "Open coding reference")}</p>
          </a>
        `).join("")}
      </details>`;
  }

  // ---------- MAIN BUILDER ----------

  async function sendCodeMessageV2() {
    if (building || codeBusy) return;

    const input = $("codeInput");
    const prompt = input.value.trim();

    if (!prompt) return;

    input.value = "";
    addCodeMessage("user", prompt);

    const body = addCodeMessage("assistant", "");
    building = true;
    codeBusy = true;

    body.innerHTML =
      "<p>VEX is researching and preparing your project.</p>" +
      progressHTML();

    try {
      updateProgress(0);

      const sources = await researchCoding(prompt);

      updateProgress(1);
      await sleep(250);

      const project = buildProject(prompt);

      if (!project || !project.html) {
        throw new Error("Project generation failed.");
      }

      updateProgress(2);

      setProject(project);

      const checks = checkProject(project);
      const passed = checks.filter(x => x.ok).length;

      updateProgress(3);
      await sleep(300);

      const htmlCheck = checkHTML();

      body.innerHTML =
        "<p><strong>Project generated.</strong></p>" +
        "<p>VEX searched coding resources, selected a supported project structure and generated these files:</p>" +
        "<p>• index.html<br>• style.css<br>• script.js</p>" +
        "<p><strong>Initial checks: " + passed + "/" + checks.length +
        " passed.</strong></p>" +
        "<div class='progress-box'>" +
        checks.map(check =>
          `<div class="progress-line ${check.ok ? "done" : ""}">
            <span class="progress-dot">${check.ok ? "✓" : "!"}</span>
            ${escapeHTML(check.name)}
            <span style="margin-left:auto">${check.ok ? "Passed" : "Needs attention"}</span>
          </div>`
        ).join("") +
        "</div>" +
        (htmlCheck.ok
          ? "<p>Preview document structure check passed.</p>"
          : "<p>Preview document structure needs attention.</p>") +
        researchHTML(sources) +
        "<p><strong>Preview:</strong> Run the app and try its features. These initial checks are not a guarantee that every feature works.</p>";

      renderImprovedArtifact(body);

    } catch (error) {
      console.error("VEX Builder:", error);

      body.innerHTML =
        "<p><strong>Project creation failed.</strong></p>" +
        "<p>" + escapeHTML(error.message || "Unknown error") + "</p>" +
        "<p>Please try again with a more specific app description.</p>";
    } finally {
      building = false;
      codeBusy = false;
    }
  }

  // ---------- SAFE GLOBAL EXPORT ----------

  window.VEXBuilder = {
    downloadZIP,
    researchCoding,
    checkProject,
    buildProject
  };

  // Replace old template-only builder function.
  window.sendCodeMessage = sendCodeMessageV2;

  // Keep the existing HTML download function available.
  window.downloadProject = function () {
    const content = projectHTML();
    const blob = new Blob([content], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");

    a.href = url;
    a.download = (projectName || "VEX_Project")
      .replace(/[^a-z0-9_-]/gi, "_") + ".html";

    document.body.appendChild(a);
    a.click();
    a.remove();

    setTimeout(() => URL.revokeObjectURL(url), 3000);
  };

})();
