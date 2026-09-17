// Optional browser smoke test. Requires Playwright and its Chromium runtime.
// Uses a synthetic temporary course, a loopback server, and no provider calls.
const assert = require('node:assert/strict');
const {mkdtempSync, rmSync, writeFileSync, unlinkSync} = require('node:fs');
const {tmpdir} = require('node:os');
const path = require('node:path');
const {execFileSync, spawn} = require('node:child_process');
const {chromium} = require('playwright');

async function main() {
  const project = mkdtempSync(path.join(tmpdir(), 'cadence-progress-smoke-'));
  const python = process.env.CADENCE_TEST_PYTHON || 'python3';
  const script = path.resolve(__dirname, '../skills/cadence/scripts/progress.py');
  const command = (...args) => execFileSync(python, [script, ...args, '--project', project], {encoding:'utf8'});
  let server, browser;
  try {
    command('init', '--title', 'Synthetic progress test', '--demo');
    command('catalog', '--catalog-file', path.resolve(__dirname, 'fixtures/artifact-catalog.md'));
    command('phase', '--phase', 'analysis', '--status', 'working', '--note', 'Checking the learner profile');
    command('agent', '--id', 'sequential-test', '--role', 'Subject expert', '--execution', 'sequential', '--status', 'working');
    writeFileSync(path.join(project, 'review.md'), 'Synthetic review only.');
    command('artifact', '--path', 'review.md', '--status', 'draft');
    server = spawn(python, [script, 'serve', '--project', project], {stdio:['ignore','pipe','pipe']});
    const url = await new Promise((resolve, reject) => {
      let output = '';
      const timer = setTimeout(() => reject(new Error('Viewer did not start')), 10000);
      server.on('error', reject);
      server.on('exit', code => { clearTimeout(timer); reject(new Error(`Viewer exited ${code}`)); });
      server.stdout.on('data', chunk => {
        output += chunk.toString();
        if (output.includes('\n')) {
          clearTimeout(timer);
          resolve(JSON.parse(output.split('\n')[0]).url);
        }
      });
    });
    browser = await chromium.launch({headless:true, channel:process.env.CADENCE_TEST_BROWSER_CHANNEL || undefined});
    const page = await browser.newPage({viewport:{width:820,height:1000}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(url);
    await page.getByText('Checking the learner profile', {exact:true}).first().waitFor();
    const logo = page.getByRole('img', {name:'Project Cadence'});
    await logo.waitFor();
    assert(await logo.evaluate(image => image.complete && image.naturalWidth > 0));
    assert.equal(await page.locator('#phases li').count(), 5);
    assert.match(await page.locator('#agents').innerText(), /Sequential check/);
    assert.match(await page.locator('#artifacts').innerText(), /Draft saved/);
    assert.equal(await page.locator('.phase-sections').count(), 3);
    const analysis = page.locator('.phase-sections[data-phase="analysis"]');
    assert.equal(await analysis.getAttribute('open'), '');
    writeFileSync(path.join(project, 'analysis.md'), 'Synthetic analysis section with saved findings.');
    command('section', '--phase', 'analysis', '--id', 'analysis.1.1', '--status', 'complete', '--path', 'analysis.md', '--note', 'Synthetic findings checked');
    const completed = page.locator('[data-section-id="analysis.1.1"]');
    await page.locator('[data-section-id="analysis.1.1"][data-status="complete"]').waitFor();
    assert.match(await completed.innerText(), /✓/);
    assert.match(await analysis.locator('summary').innerText(), /1 \/ 4/);
    command('section', '--phase', 'development', '--id', 'development.2.1', '--status', 'skipped', '--note', 'Outside this synthetic test scope');
    const skipped = page.locator('[data-section-id="development.2.1"]');
    await page.locator('[data-section-id="development.2.1"][data-status="skipped"]').waitFor({state:'attached'});
    assert(!/✓/.test(await skipped.textContent()));
    await analysis.locator('summary').focus();
    await page.keyboard.press('Enter');
    assert.equal(await analysis.getAttribute('open'), null);
    command('activity', '--note', 'Checking persisted disclosure state');
    await page.waitForFunction(() => document.getElementById('note').textContent === 'Checking persisted disclosure state');
    assert.equal(await analysis.getAttribute('open'), null);
    await analysis.locator('summary').click();
    unlinkSync(path.join(project, 'analysis.md'));
    await page.locator('[data-section-id="analysis.1.1"][data-status="missing"]').waitFor();
    assert(!/✓/.test(await completed.innerText()));
    command('phase', '--phase', 'analysis', '--status', 'waiting', '--note', 'Choose the target learners');
    await page.waitForFunction(() => document.getElementById('note').textContent === 'Choose the target learners');
    assert.equal(await page.locator('#run-status').innerText(), 'Waiting for you');
    command('activity', '--note', '<img src=x onerror=alert(1)>');
    await page.waitForFunction(() => document.getElementById('note').textContent.includes('<img'));
    assert.equal(await page.locator('#note img').count(), 0);
    command('activity', '--note', 'Checking a long curriculum title and its supporting documents');
    await page.waitForFunction(() => document.getElementById('note').textContent.startsWith('Checking a long'));
    await page.locator('#evidence summary').focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#evidence').getAttribute('open'), '');
    for (const width of [820, 580, 375, 320]) {
      await page.setViewportSize({width,height:1100});
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Overflow at ${width}px`);
      const boxes = await page.locator('.phase').evaluateAll(nodes => nodes.map(node => {
        const r = node.getBoundingClientRect(); return {left:r.left,right:r.right,top:r.top,bottom:r.bottom};
      }));
      for (let i=1; i<boxes.length; i++) {
        const a=boxes[i-1], b=boxes[i];
        assert(a.right <= b.left+1 || a.bottom <= b.top+1, `Overlapping phases at ${width}px`);
      }
    }
    await page.emulateMedia({colorScheme:'dark'});
    assert.equal(errors.length, 0, errors.join('\n'));
    server.kill();
    await page.waitForFunction(() => document.getElementById('connection').textContent.startsWith('Disconnected'), null, {timeout:10000});
    assert.match(await page.locator('#note').innerText(), /Checking a long/);
    console.log('Browser checks passed: subsection checkmarks, skipped and missing evidence, disclosure state, live updates, waiting states, safe text, keyboard, 320–820px layouts, dark mode, and disconnect preservation.');
  } finally {
    if (browser) await browser.close();
    if (server && server.exitCode === null) server.kill();
    rmSync(project, {recursive:true,force:true});
  }
}
main().catch(error => { console.error(error); process.exitCode=1; });
