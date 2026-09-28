const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.site-nav');

navToggle?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
});

document.querySelectorAll('.site-nav a').forEach(link => {
  link.addEventListener('click', () => {
    nav.classList.remove('open');
    navToggle?.setAttribute('aria-expanded', 'false');
  });
});

document.getElementById('year').textContent = new Date().getFullYear();

const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

const sections = [...document.querySelectorAll('main section[id]')];
const navLinks = [...document.querySelectorAll('.site-nav a')];
const sectionObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    navLinks.forEach(link => {
      link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`);
    });
  });
}, { rootMargin: '-35% 0px -55% 0px' });
sections.forEach(section => sectionObserver.observe(section));

const projectData = JSON.parse(document.getElementById('project-data').textContent);

function expandProjectYear(hash) {
  const target = document.getElementById(hash.replace(/^#/, ''));
  const year = target?.closest('details.project-year');
  if (year) year.open = true;
}

document.querySelectorAll('.project-year-nav a').forEach(link => {
  link.addEventListener('click', () => expandProjectYear(link.hash));
});
window.addEventListener('hashchange', () => expandProjectYear(location.hash));
expandProjectYear(location.hash);

document.querySelector('.project-year-controls').hidden = false;
document.querySelectorAll('[data-project-years]').forEach(button => {
  button.addEventListener('click', () => {
    const open = button.dataset.projectYears === 'expand';
    document.querySelectorAll('details.project-year').forEach(year => { year.open = open; });
  });
});

const dialog = document.getElementById('project-dialog');
const dialogContent = document.getElementById('dialog-content');

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[char]);
}

function renderMedia(asset) {
  const src = escapeHtml(asset.src);
  const caption = escapeHtml(asset.caption);
  const poster = asset.poster ? ` poster="${escapeHtml(asset.poster)}"` : '';
  const content = asset.type === 'video'
    ? `<video controls preload="metadata" playsinline${poster} aria-label="${caption}" src="${src}"></video><p><a class="media-download" href="${src}">Open video file</a> &middot; <a class="media-download" href="${src}" download>Download video</a></p>`
    : `<a href="${src}" target="_blank" rel="noopener noreferrer" aria-label="Open full image: ${caption}"><img src="${src}" alt="${caption}" loading="lazy" decoding="async" /></a><a class="media-download" href="${src}" download>Download image</a>`;
  return `<figure>${content}<figcaption>${caption}</figcaption></figure>`;
}

function renderProject(project) {
  const gallery = project.media;
  dialogContent.innerHTML = `
    <div class="dialog-inner">
      <p class="eyebrow">Project Case Study</p>
      <h2 id="project-dialog-title">${escapeHtml(project.title)}</h2>
      <p class="company">${project.year} · ${escapeHtml(project.context)}</p>
      ${project.award ? `<p class="award">${escapeHtml(project.award)}</p>` : ''}
      <div class="dialog-section">
        <h3>Objective</h3>
        <p>${escapeHtml(project.objective)}</p>
      </div>
      <div class="dialog-section">
        <h3>Key Constraints / Challenges</h3>
        <ul>${project.challenges.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
      </div>
      <div class="dialog-section">
        <h3>Engineering Contribution</h3>
        <p>${escapeHtml(project.contribution)}</p>
      </div>
      ${project.outcome ? `<div class="dialog-section"><h3>Outcome and Testing</h3><p>${escapeHtml(project.outcome)}</p></div>` : ''}
      ${project.iterations?.length ? `<div class="dialog-section"><h3>Design Evolution</h3>${project.iterations.map(step => `<h4>${escapeHtml(step.title)}</h4><p><strong>Before:</strong> ${escapeHtml(step.before)}</p><p><strong>After:</strong> ${escapeHtml(step.after)}</p>`).join('')}</div>` : ''}
      ${project.external_links?.length ? `<div class="dialog-section"><h3>Interactive CAD</h3>${project.external_links.map(link => `<p><a class="text-link" href="${escapeHtml(link.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(link.label)}</a></p><p>${escapeHtml(link.description)}</p>`).join('')}</div>` : ''}
      ${project.supporting_page ? `<div class="dialog-section"><h3>Supporting files</h3><p><a class="text-link" href="${escapeHtml(encodeURI(project.supporting_page))}">Browse supporting files</a></p></div>` : ''}
      ${project.documents?.length ? `<div class="dialog-section"><h3>Project Documentation</h3><ul>${project.documents.map(document => `<li><a class="text-link" href="${escapeHtml(encodeURI(document.src))}" target="_blank" rel="noopener noreferrer">${escapeHtml(document.label)}</a></li>`).join('')}</ul></div>` : ''}
      ${gallery.length ? `<div class="dialog-section"><h3>Build Photos &amp; Demonstrations</h3><div class="dialog-gallery">${gallery.map(renderMedia).join('')}</div></div>` : ''}
    </div>`;
}

document.querySelectorAll('.project-open').forEach(button => {
  button.addEventListener('click', () => {
    const project = projectData[button.dataset.project];
    if (!project) return;
    renderProject(project);
    dialog.showModal();
    dialog.scrollTop = 0;
  });
});

document.querySelector('.dialog-close')?.addEventListener('click', () => dialog.close());
dialog?.addEventListener('close', () => {
  if (dialog.open) return;
  dialog.querySelectorAll('video').forEach(video => video.pause());
});

dialog?.addEventListener('click', event => {
  if (event.target !== dialog) return;
  const rect = dialog.getBoundingClientRect();
  const inside = event.clientX >= rect.left && event.clientX <= rect.right && event.clientY >= rect.top && event.clientY <= rect.bottom;
  if (!inside) dialog.close();
});
