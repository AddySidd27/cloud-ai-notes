import markdownItAnchor from "markdown-it-anchor";
import syntaxHighlight from "@11ty/eleventy-plugin-syntaxhighlight";
import topics from "./src/_data/topics.js";
import series from "./src/_data/series.js";

export default function (eleventyConfig) {
  eleventyConfig.addPlugin(syntaxHighlight, { preAttributes: { tabindex: 0 } });
  eleventyConfig.addPassthroughCopy({ "src/css": "css", "src/js": "js", "src/img": "img", "src/fonts": "fonts", "src/diagrams": "diagrams" });
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });

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

  eleventyConfig.addFilter("seriesOf", (tags) => series.find((s) => (tags || []).includes(s.tag)));
  eleventyConfig.addFilter("topicOf", (ser) => ser && topics.find((t) => t.slug === ser.category));
  const abs = (base, path) => base.replace(/\/$/, "") + path;
  eleventyConfig.addFilter("ldHome", (site) => JSON.stringify({ "@context": "https://schema.org", "@graph": [
    { "@type": "WebSite", "@id": site.url + "/#website", url: site.url + "/", name: site.name, description: site.description, publisher: { "@id": site.url + "/#author" },
      potentialAction: { "@type": "SearchAction", target: site.url + "/search/?q={search_term_string}", "query-input": "required name=search_term_string" } },
    { "@type": "Person", "@id": site.url + "/#author", name: site.author, jobTitle: site.role, url: site.url + "/about/" } ] }));
  eleventyConfig.addFilter("ldPerson", (site) => JSON.stringify({ "@context": "https://schema.org", "@type": "Person", name: site.author, jobTitle: site.role, url: site.url + "/about/" }));
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
