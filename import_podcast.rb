require 'rss'
require 'fileutils'
require 'time'

# Configuration
feed_file = 'feed.xml'  # Change this to your RSS feed file path or URL
posts_dir = '_posts'

FileUtils.mkdir_p(posts_dir)

# Parse the feed
File.open(feed_file) do |file|
  feed = RSS::Parser.parse(file)
  
  feed.items.each do |item|
    # Extract date
    date = item.pubDate
    date_str = date.strftime('%Y-%m-%d')
    
    # Create filename from title
    title = item.title.strip
    title_slug = title.gsub(/[^0-9A-Za-z\s-]/, '').gsub(/\s+/, '-').downcase
    filename = "#{posts_dir}/#{date_str}-#{title_slug}.md"
    
    # Skip if file already exists
    if File.exist?(filename)
      puts "Skipping (already exists): #{filename}"
      next
    end
    
    # Extract enclosure data
    enclosure = item.enclosure
    original_url = enclosure.url
    # Extract filename from URL and convert to _assets path
    audio_filename = original_url.split('/').last
    audio_url = "https://shawkatya.github.io/closetalkers/_assets/#{audio_filename}"
    file_size = enclosure.length.to_i
    
    # Extract iTunes data
    duration = item.itunes_duration.content.to_i
    episode_type = item.itunes_episodeType.content
    season = item.itunes_season.content.to_i
    explicit = item.itunes_explicit.content
    
    # Get GUID
    guid = item.guid.content
    
    # Get summary (clean up)
    summary = item.itunes_summary.strip
    
    # Get description content (strip HTML tags)
    description = item.description.gsub(/<[^>]*>/, '').strip
    
    # Write the post file
    File.open(filename, 'w') do |post|
      post.puts "---"
      post.puts "layout: post"
      post.puts "title: \"#{title.gsub('"', '\\"')}\""
      post.puts "date: #{date.strftime('%Y-%m-%d %H:%M:%S %z')}"
      post.puts "podcast:"
      post.puts "  audio_url: \"#{audio_url}\""
      post.puts "  file_size: #{file_size}"
      post.puts "  duration: #{duration}"
      post.puts "  guid: \"#{guid}\""
      post.puts "  season: #{season}"
      post.puts "  episode_type: \"#{episode_type}\""
      post.puts "  explicit: \"#{explicit}\""
      post.puts "  summary: \"#{summary.gsub('"', '\\"')}\""
      post.puts "  # image: \"/assets/episode-cover.png\""
      post.puts "---"
      post.puts description
      post.puts ""
      post.puts "[Listen to the episode](#{audio_url})"
    end
    
    puts "Created: #{filename}"
  end
end

puts "\nImport complete! Files created in #{posts_dir}"
