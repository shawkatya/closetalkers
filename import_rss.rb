require "jekyll-import"

JekyllImport::Importers::RSS.run({
  "source" => "feed.xml",
  "render_as_post" => true,
  "canonical_link" => true
})