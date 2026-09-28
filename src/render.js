// Render the animated scenes to video frames.
//   node src/render.js <lang> preview <t1,t2,...>   -> PNG stills in build/<lang>/preview
//   node src/render.js <lang> video [workers]       -> build/<lang>/video.mp4 (silent)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const FPS = 30;
// headless_shell renders noticeably faster; fall back to Playwright's default
const CHROME = ['/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',
  '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'].find(p => fs.existsSync(p));
const FFMPEG = require('child_process').execSync(
  'python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"').toString().trim();

const [lang, mode, arg] = process.argv.slice(2);
const timeline = JSON.parse(fs.readFileSync(`${ROOT}/build/${lang}/timeline.json`, 'utf8'));

function icons() {
  const set = require(`${ROOT}/node_modules/@iconify-json/fluent-emoji-flat/icons.json`);
  const src = fs.readFileSync(`${ROOT}/src/player.html`, 'utf8') + JSON.stringify(timeline);
  const out = {};
  for (const [name, ic] of Object.entries(set.icons)) {
    if (!src.includes(`"${name}"`) && !src.includes(`'${name}'`)) continue;
    const w = ic.width || set.width || 32, h = ic.height || set.height || 32;
    out[name] = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}">${ic.body}</svg>`;
  }
  return out;
}

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(ROOT, 'src/player.html'));
  await page.evaluate(([tl, ic]) => window.setup(tl, ic), [timeline, icons()]);
  return page;
}

async function renderRange(browser, f0, f1, out) {
  const page = await openPage(browser);
  const cdp = await page.context().newCDPSession(page);
  const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS),
    '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
    '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = f0; f < f1; f++) {
    await page.evaluate(t => window.render(t), f / FPS);
    const { data } = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 93, optimizeForSpeed: true });
    const buf = Buffer.from(data, 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 900 === 0) console.log(`${lang} ${out.split('/').pop()} ${f - f0}/${f1 - f0}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await page.close();
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME });
  const dir = `${ROOT}/build/${lang}`;
  if (mode === 'preview') {
    fs.mkdirSync(`${dir}/preview`, { recursive: true });
    const page = await openPage(browser);
    for (const t of arg.split(',').map(Number)) {
      await page.evaluate(t => window.render(t), t);
      await page.screenshot({ path: `${dir}/preview/t${String(t).padStart(6, '0')}.png` });
    }
  } else {
    const workers = +(arg || 4);
    const total = Math.ceil(timeline.total * FPS);
    const per = Math.ceil(total / workers);
    const parts = [];
    await Promise.all(Array.from({ length: workers }, (_, i) => {
      const out = `${dir}/part${i}.mp4`; parts.push(out);
      return renderRange(browser, i * per, Math.min(total, (i + 1) * per), out);
    }));
    fs.writeFileSync(`${dir}/parts.txt`, parts.map(p => `file '${p}'`).join('\n'));
    await new Promise(r => spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
      '-i', `${dir}/parts.txt`, '-c', 'copy', `${dir}/video.mp4`], { stdio: 'inherit' }).on('close', r));
    console.log('done', `${dir}/video.mp4`);
  }
  await browser.close();
})();
