source "https://rubygems.org"

# Use the github-pages gem to match GitHub Pages' environment
gem "github-pages", group: :jekyll_plugins

# Common Jekyll plugins (included with github-pages but listed for clarity)
group :jekyll_plugins do
  gem "jekyll-feed"          # Generates an Atom feed of your posts
  gem "jekyll-seo-tag"       # Adds SEO metadata tags
  gem "jekyll-sitemap"       # Generates a sitemap.xml
end

# Windows and JRuby compatibility (optional, but helpful)
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
