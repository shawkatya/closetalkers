# Jekyll Podcast RSS Feed Setup

This setup creates a podcast-compliant RSS feed for your Jekyll blog on GitHub Pages.

## Setup Instructions

### 1. Add the RSS feed template

Copy `podcast.xml` to the root of your Jekyll site. This file will be accessible at `https://yourusername.github.io/podcast.xml`

### 2. Configure your `_config.yml`

Add the podcast configuration section to your `_config.yml` file. Customize all the values:

- **title**: Your podcast name
- **author**: Your name or podcast host names
- **description**: Full description (up to 4000 characters)
- **summary**: Shorter version for podcast apps
- **owner_email**: Email for podcast ownership verification
- **image**: Path to your podcast artwork (must be 1400x1400 to 3000x3000 pixels, JPEG or PNG)
- **categories**: Choose appropriate iTunes categories

### 3. Create podcast episodes

For each podcast episode, create a blog post in your `_posts` directory with the following front matter:

```yaml
---
layout: post
title: "Episode Title"
date: YYYY-MM-DD HH:MM:SS TIMEZONE
podcast:
  audio_url: "https://your-audio-hosting.com/episode.mp3"
  file_size: 12345678  # in bytes
  duration: 1234  # in seconds
  guid: "unique-identifier"
  season: 1
  episode: 1
  episode_type: "full"
  explicit: "no"
  summary: "Brief episode description"
---

Episode show notes go here...
```

### 4. Host your audio files

Your audio files need to be hosted somewhere accessible via HTTPS. Options include:

- **GitHub Releases**: Upload MP3 files to GitHub releases
- **Archive.org**: Free hosting for media files
- **Amazon S3**: Affordable cloud storage
- **Dedicated podcast hosts**: Libsyn, Buzzsprout, etc.

⚠️ **Note**: Don't commit large audio files directly to your GitHub repository. Use Git LFS or external hosting.

### 5. Required podcast episode fields

Each episode post MUST include in the `podcast:` section:

- `audio_url`: Full URL to the MP3 file
- `file_size`: File size in bytes (use `ls -l filename.mp3` to get this)
- `duration`: Episode length in seconds (use `ffprobe` or media info tools)
- `guid`: Unique identifier (use a UUID generator or create your own system)

### 6. Submit to podcast directories

Once your feed is live, you can submit it to:

- **Apple Podcasts**: https://podcastsconnect.apple.com/
- **Spotify**: https://podcasters.spotify.com/
- **Google Podcasts**: https://podcastsmanager.google.com/
- **Podcast Index**: https://podcastindex.org/

Use the feed URL: `https://yourusername.github.io/podcast.xml`

## Helpful Tips

### Getting file size in bytes

**On Mac/Linux:**
```bash
ls -l episode.mp3
```

**On Windows PowerShell:**
```powershell
(Get-Item episode.mp3).length
```

### Getting duration in seconds

**Using ffprobe (part of ffmpeg):**
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 episode.mp3
```

**Or use an online tool like**: https://ezgif.com/video-to-gif

### Generating GUIDs

**Online UUID generator**: https://www.uuidgenerator.net/

**Or use a consistent format**:
```
your-podcast-s01e01
your-podcast-s01e02
```

### Validating your feed

Before submitting to directories, validate your feed:

- **Cast Feed Validator**: https://castfeedvalidator.com/
- **Podbase**: https://podba.se/validate/

## Troubleshooting

**Feed not updating?**
- GitHub Pages can take a few minutes to rebuild
- Clear your browser cache
- Check that the post date isn't in the future

**Episodes not showing?**
- Ensure `podcast:` front matter is present
- Check that `audio_url` is accessible (try opening in browser)
- Verify file_size and duration are numbers, not strings

**Feed validation errors?**
- Make sure image is 1400x1400 minimum
- Check that all required fields are present
- Ensure audio URLs use HTTPS (not HTTP)
