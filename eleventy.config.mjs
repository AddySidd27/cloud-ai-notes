import fs from "node:fs";
import path from "node:path";
import markdownItAnchor from "markdown-it-anchor";
import syntaxHighlight from "@11ty/eleventy-plugin-syntaxhighlight";
import topics from "./src/_data/topics.js";
import series from "./src/_data/series.js";

export default function (eleventyConfig) {
  eleventyConfig.addPlugin(syntaxHighlight, { preAttributes: { tabindex: 0 } });
  eleventyConfig.addPassthroughCopy({ "src/css": "css", "src/js": "js", "src/fonts": "fonts", "src/diagrams": "diagrams" });
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });

  // Privacy guard: src/img/avd also holds superseded or unredacted screenshots that stay in the source tree
  // but must not be published. Copy only the files under img/avd that a source page, template, data file or
  // stylesheet actually references, and everything else under src/img (logos, og images, icons) as before.
  // Source files are never touched.
  {
    const walkSrc = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walkSrc(path.join(d, e.name)) : [path.join(d, e.name)]));
    const textExt = new Set([".md", ".njk", ".js", ".mjs", ".json", ".css", ".html", ".yml", ".yaml"]);
    const referenced = new Set();
    for (const f of walkSrc("src")) {
      if (f.startsWith(path.join("src", "img") + path.sep)) continue;
      if (!textExt.has(path.extname(f).toLowerCase())) continue;
      for (const m of fs.readFileSync(f, "utf8").matchAll(/\/img\/avd\/([A-Za-z0-9_.\-]+)/g)) referenced.add(m[1]);
    }
    for (const e of fs.readdirSync(path.join("src", "img"), { withFileTypes: true })) {
      if (e.isDirectory() && e.name === "avd") continue;
      eleventyConfig.addPassthroughCopy({ [`src/img/${e.name}`]: `img/${e.name}` });
    }
    for (const name of referenced) {
      if (fs.existsSync(path.join("src", "img", "avd", name))) eleventyConfig.addPassthroughCopy({ [`src/img/avd/${name}`]: `img/avd/${name}` });
    }
  }


  // Layout stability: add intrinsic width and height to local images that lack them, so the page does not shift while
  // images load. Dimensions are read from the source file (PNG, JPEG or SVG); existing attributes are never overridden.
  {
    const dimCache = new Map();
    const dims = (src) => {
      if (dimCache.has(src)) return dimCache.get(src);
      let out = null;
      try {
        const file = path.join("src", decodeURIComponent(src.split(/[?#]/)[0]));
        const buf = fs.readFileSync(file);
        const ext = path.extname(file).toLowerCase();
        if (ext === ".png" && buf.length > 24) out = [buf.readUInt32BE(16), buf.readUInt32BE(20)];
        else if (ext === ".jpg" || ext === ".jpeg") {
          let i = 2;
          while (i + 9 < buf.length) {
            if (buf[i] !== 0xff) { i++; continue; }
            const m = buf[i + 1];
            if (m >= 0xc0 && m <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(m)) { out = [buf.readUInt16BE(i + 7), buf.readUInt16BE(i + 5)]; break; }
            i += 2 + buf.readUInt16BE(i + 2);
          }
        } else if (ext === ".svg") {
          const s = buf.toString("utf8", 0, 2000);
          const vb = s.match(/viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"/);
          const w = s.match(/<svg[^>]*\swidth="([\d.]+)(?:px)?"/), h = s.match(/<svg[^>]*\sheight="([\d.]+)(?:px)?"/);
          if (w && h) out = [Math.round(+w[1]), Math.round(+h[1])];
          else if (vb) out = [Math.round(+vb[1]), Math.round(+vb[2])];
        }
      } catch {}
      dimCache.set(src, out);
      return out;
    };
    eleventyConfig.addTransform("imageDimensions", function (content) {
      if (!(this.page.outputPath || "").endsWith(".html")) return content;
      return content.replace(/<img\b[^>]*>/g, (tag) => {
        if (/\swidth=/.test(tag) && /\sheight=/.test(tag)) return tag;
        const src = (tag.match(/\ssrc="(\/(?:img|diagrams)\/[^"]+)"/) || [])[1];
        const d = src && dims(src);
        if (!d || !d[0] || !d[1]) return tag;
        const stripped = tag.replace(/\s(?:width|height)="[^"]*"/g, "");
        return stripped.replace(/<img\b/, `<img width="${d[0]}" height="${d[1]}"`);
      });
    });
  }

  eleventyConfig.amendLibrary("md", (md) => md.use(markdownItAnchor, { level: [2], tabIndex: false }));

  // All articles that belong to a series, in reading order. Start Here has no series tag, so it is not listed.
  const seriesTags = series.map((s) => s.tag);
  const articles = (api) =>
    api.getAll().filter((p) => p.data.order > 0 && (p.data.tags || []).some((t) => seriesTags.includes(t)))
      .sort((a, b) => a.data.order - b.data.order);
  eleventyConfig.addCollection("articles", articles);

  const seriesOf = (p) => series.find((s) => (p.data.tags || []).includes(s.tag));
  eleventyConfig.addCollection("liveSeries", (api) =>
    series.map((s) => ({ ...s, posts: articles(api).filter((p) => (p.data.tags || []).includes(s.tag)) })).filter((s) => s.posts.length));
  eleventyConfig.addCollection("liveTopics", (api) =>
    topics.map((t) => ({ ...t, posts: articles(api).filter((p) => seriesOf(p)?.category === t.slug) })).filter((t) => t.posts.length));

  const articleFigures = (html) => String(html).replace(/<p>\s*(<img[^>]*src="([^"]+)"[^>]*>)\s*<\/p>(?:\s*<p>((?:<em>[\s\S]*?<\/em>)|(?:Figure \d+\.[\s\S]*?))<\/p>)?/g, (_, image, src, caption) => {
    const alt = (image.match(/alt="([^"]*)"/) || [])[1] || "Article illustration";
    const compact = src.includes("AVD-Post-01-Components") ? " compact" : "";
    return `<figure class="article-figure${compact}">${image}<figcaption><span class="figure-caption">${caption || (src.startsWith("/diagrams/") ? "" : alt)}</span><span class="figure-zoom">Click the image to enlarge</span></figcaption></figure>`;
  });
  eleventyConfig.addFilter("articleFigures", articleFigures);
  eleventyConfig.addFilter("avdFigures", articleFigures);
  eleventyConfig.addFilter("inSeries", (list, tag) => list.filter((p) => (p.data.tags || []).includes(tag)));
  eleventyConfig.addFilter("seriesOf", (tags) => series.find((s) => (tags || []).includes(s.tag)));
  eleventyConfig.addFilter("topicOf", (ser) => ser && topics.find((t) => t.slug === ser.category));
  const abs = (base, path) => base.replace(/\/$/, "") + path;
  eleventyConfig.addFilter("ldHome", (site) => JSON.stringify({ "@context": "https://schema.org", "@graph": [
    { "@type": "WebSite", "@id": site.url + "/#website", url: site.url + "/", name: site.name, description: site.description, publisher: { "@id": site.url + "/#author" },
      potentialAction: { "@type": "SearchAction", target: site.url + "/search/?q={search_term_string}", "query-input": "required name=search_term_string" } },
    { "@type": "Person", "@id": site.url + "/#author", name: site.author, jobTitle: site.role, url: site.url + "/about/" } ] }));
  eleventyConfig.addFilter("ldPerson", (site) => JSON.stringify({ "@context": "https://schema.org", "@type": "Person", name: site.author, jobTitle: site.role, url: site.url + "/about/", sameAs: [site.linkedin, "https://github.com/AddySidd27"].filter(Boolean) }));
  eleventyConfig.addFilter("ldArticle", (c) => {
    const { site, title, deck, url, img, meta, ser, tp } = c;
    return JSON.stringify({ "@context": "https://schema.org", "@graph": [
      { "@type": "TechArticle", headline: title, description: deck, url, mainEntityOfPage: url, image: img, datePublished: meta.published, dateModified: meta.published,
        keywords: meta.tags.join(", "), inLanguage: "en",
        author: { "@type": "Person", name: site.author, jobTitle: site.role, url: site.url + "/about/" }, publisher: { "@type": "Person", name: site.author },
        isPartOf: { "@type": "CreativeWorkSeries", name: ser.title, url: abs(site.url, "/" + ser.slug + "/") } },
      { "@type": "BreadcrumbList", itemListElement: [
        { "@type": "ListItem", position: 1, name: "Home", item: site.url + "/" },
        { "@type": "ListItem", position: 2, name: tp.name, item: abs(site.url, "/" + tp.slug + "/") },
        { "@type": "ListItem", position: 3, name: ser.name, item: abs(site.url, "/" + ser.slug + "/") },
        { "@type": "ListItem", position: 4, name: title, item: url } ] } ] });
  });
  eleventyConfig.addFilter("neighbors", (list, url) => {
    const i = list.findIndex((p) => p.url === url);
    return { prev: i > 0 ? list[i - 1] : null, next: i >= 0 && i < list.length - 1 ? list[i + 1] : null };
  });
  // Related: other articles sharing the most tags, ties broken by closeness in the series.
  eleventyConfig.addFilter("related", (list, url, meta, n) => {
    const me = list.find((p) => p.url === url); if (!me) return [];
    const mine = (meta[me.data.order] || {}).tags || [];
    return list.filter((p) => p.url !== url).map((p) => ({
      p, score: ((meta[p.data.order] || {}).tags || []).filter((t) => mine.includes(t)).length * 100 - Math.abs(p.data.order - me.data.order),
    })).sort((a, b) => b.score - a.score).slice(0, n).map((x) => x.p);
  });
  eleventyConfig.addFilter("pick", (list, orders) => orders.map((o) => list.find((p) => p.data.order === o)).filter(Boolean));
  eleventyConfig.addFilter("absUrl", (path, base) => base.replace(/\/$/, "") + path);
  eleventyConfig.addFilter("latest", (list, n) => [...list].reverse().slice(0, n));
  // Newest first by publish date, at most `per` articles from one series, so one busy series cannot fill the list.
  eleventyConfig.addFilter("mixLatest", (list, meta, n, per) => {
    const seen = {}; const out = [];
    const day = (p) => (meta[p.data.order] || {}).published || "";
    const sorted = [...list].sort((x, y) => day(y).localeCompare(day(x)) || y.data.order - x.data.order);
    for (const p of sorted) {
      const s = seriesOf(p); const k = s ? s.slug : "none";
      if ((seen[k] || 0) >= per) continue;
      seen[k] = (seen[k] || 0) + 1; out.push(p);
      if (out.length >= n) break;
    }
    return out;
  });
  // First diagram used in an article, for list thumbnails. Empty when the article has no diagram.
  eleventyConfig.addFilter("firstDiagram", (html) => {
    const m = String(html).match(/<img[^>]+src="(\/diagrams\/[^"]+\.svg)"/);
    return m ? m[1] : "";
  });
  eleventyConfig.addFilter("pad", (n) => String(n).padStart(2, "0"));
  eleventyConfig.addFilter("longDate", (d) => new Date(d + "T12:00:00Z").toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" }));
  eleventyConfig.addFilter("toc", (html) =>
    [...String(html).matchAll(/<h2 id="([^"]+)"[^>]*>(.*?)<\/h2>/gs)].map((m) => ({
      id: m[1],
      text: m[2].replace(/<a class="header-anchor".*?<\/a>/gs, "").replace(/<[^>]+>/g, "").trim(),
    })));
  eleventyConfig.addFilter("readingTime", (html) => {
    const words = String(html).replace(/<[^>]+>/g, " ").split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.round(words / 220));
  });
  eleventyConfig.addFilter("clip", (s, n) => {
    s = String(s || ""); return s.length > n ? s.slice(0, n).replace(/\s+\S*$/, "") + "…" : s;
  });

  return {
    dir: { input: "src", output: "_site", includes: "_includes", data: "_data" },
    markdownTemplateEngine: false,
    htmlTemplateEngine: "njk",
  };
}
