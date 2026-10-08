import markdownItAnchor from "markdown-it-anchor";
import topics from "./src/_data/topics.js";

export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/css": "css", "src/js": "js", "src/img": "img", "src/fonts": "fonts", "src/diagrams": "diagrams" });
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });

  eleventyConfig.amendLibrary("md", (md) => md.use(markdownItAnchor, { level: [2], tabIndex: false }));

  // One collection per topic, posts sorted by order. Start Here (order 0) has no tag so it is never listed.
  for (const t of topics) {
    eleventyConfig.addCollection("topic_" + t.tag, (api) =>
      api.getFilteredByTag(t.tag).sort((a, b) => a.data.order - b.data.order));
  }

  eleventyConfig.addFilter("neighbors", (list, url) => {
    const i = list.findIndex((p) => p.url === url);
    return { prev: i > 0 ? list[i - 1] : null, next: i >= 0 && i < list.length - 1 ? list[i + 1] : null };
  });
  eleventyConfig.addFilter("absUrl", (path, base) => base.replace(/\/$/, "") + path);
  eleventyConfig.addFilter("topicByTag", (list, tags) => list.find((t) => (tags || []).includes(t.tag)));
  eleventyConfig.addFilter("latest", (list, n) => [...list].reverse().slice(0, n));
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
