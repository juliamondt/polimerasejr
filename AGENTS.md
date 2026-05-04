# Polimerase EJ Website

Multi-page static site (no build system). 

## Key Facts

- **Language**: Portuguese (pt-BR)
- **No build step**: Edit HTML and CSS files directly
- **No npm/node**: No package.json, dependencies to install
- **No test suite**: No automated tests
- **No lint/format**: No code style enforcement
- **Name of the project**: Polímeras EJ

## Development

- Open `index.html` or any subpage in a browser to preview changes
- Use a local HTTP server if needed (recommended for proper CSS/JS loading):
  ```bash
  python3 -m http.server 8000
  ```
## Structure
- `style.css` — Global stylesheet for all pages
- `index.html` — The Home page (Hero, About, Differentials, and Services)
- `portfolio.html` — Portfolio and Cases section
- `blog.html` — Blog section
- `equipe.html` — Team section
- `faq.html` — Frequently Asked Questions
- `contato.html` — Contact form and info
- JS functions (like mobile menu toggle and FAQ accordion) are inline within the `<script>` tags at the bottom of each HTML file.

## Lessons Learned

### JSON Output Limitations

When working with the Write tool via JSON, be aware of output size limits. Long content (especially SVG paths, large CSS files, or extensive HTML) will cause JSON parsing errors.

**Solutions:**
1. Use Python scripts to build files instead of passing content through JSON
2. Avoid inline SVG paths - use text placeholders like `[SVG_ICON]`
3. Write files in chunks or use temporary files
4. Use the `task` tool for complex multi-step operations

## Todo List

- [x] Create style.css by extracting CSS from old-index.html
- [ ] Create index.html (Home page)
- [ ] Create portfolio.html
- [ ] Create blog.html
- [ ] Create equipe.html
- [ ] Create faq.html
- [ ] Create contato.html

## Building the Site

To build the multi-page site, create a Python script `build_site.py` that:
1. Reads old-index.html
2. Extracts CSS and saves to style.css
3. Creates all HTML pages with proper structure
4. Includes global nav, footer, and WhatsApp button on each page
5. Links to style.css in each HTML head

Example approach:
```python
import os

# Read original file
with open('old-index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract sections by finding section IDs
# Build each HTML page with common elements
# Write to respective files
```
