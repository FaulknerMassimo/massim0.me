function formatDate(iso) {
  const d = new Date(iso + "T00:00:00");
  const opts = { year: "numeric", month: "short", day: "numeric" };
  return d.toLocaleDateString("en-US", opts);
}

function renderPostList(posts, container, showCategory = true) {
  container.innerHTML = "";
  if (posts.length === 0) {
    container.innerHTML = '<li class="post-item"><p style="color:var(--subtle)">No posts yet.</p></li>';
    return;
  }
  posts
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .forEach(post => {
      const li = document.createElement("li");
      li.className = "post-item";

      const categoryTag = showCategory
        ? `<span class="category-tag">${post.category}</span>`
        : "";

      li.innerHTML = `
        <div class="post-meta">
          <span>${formatDate(post.date)}</span>
          ${categoryTag}
        </div>
        <h3><a href="${getPostURL(post)}">${post.title}</a></h3>
        <p class="excerpt">${post.excerpt}</p>
      `;
      container.appendChild(li);
    });
}

function getPostURL(post) {
  const depth = getDepth();
  const prefix = depth === 0 ? "./" : "../".repeat(depth);
  return `${prefix}posts/${post.category}/${post.id}.html`;
}

function getDepth() {
  const path = window.location.pathname;
  const segments = path.replace(/\/[^/]*$/, "").split("/").filter(Boolean);
  const rootMarker = document.documentElement.dataset.root;
  if (rootMarker !== undefined) return parseInt(rootMarker, 10);
  return 0;
}

document.addEventListener("DOMContentLoaded", () => {
  const current = window.location.pathname.split("/").filter(Boolean);
  document.querySelectorAll("nav a").forEach(link => {
    const href = link.getAttribute("href").replace(/^\.\/|^\.\.\//g, "");
    if (current.some(seg => href.includes(seg))) {
      link.classList.add("active");
    }
  });
});
