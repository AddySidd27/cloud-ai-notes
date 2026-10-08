export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/css": "css", "src/js": "js", "src/img": "img", "src/fonts": "fonts", "src/diagrams": "diagrams" });
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });
  eleventyConfig.addCollection("alz", (api) =>
    api.getFilteredByTag("alz").sort((a, b) => a.data.order - b.data.order));
  eleventyConfig.addFilter("neighbors", (list, url) => {
    const i = list.findIndex((p) => p.url === url);
    return { prev: i > 0 ? list[i - 1] : null, next: i >= 0 && i < list.length - 1 ? list[i + 1] : null };
  });
  eleventyConfig.addFilter("absUrl", (path, base) => base.replace(/\/$/, "") + path);
  return {
    dir: { input: "src", output: "_site", includes: "_includes", data: "_data" },
    markdownTemplateEngine: false,
    htmlTemplateEngine: "njk",
  };
}
