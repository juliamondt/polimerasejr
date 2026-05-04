#!/usr/bin/env python3
"""
build_site.py - Refactor single-page site into multi-page static site for Polímeras EJ
"""

import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
OLD_INDEX = BASE_DIR / "old-index.html"
OUTPUT_DIR = BASE_DIR

# Section selectors
SECTIONS = [
    ("index.html", ["#home", ".services-strip", "#sobre", "#diferenciais", "#servicos"]),
    ("sobre.html", ["#sobre"]),
    ("servicos.html", ["#servicos"]),
    ("portfolio.html", ["#portfolio"]),
    ("blog.html", ["#blog"]),
    ("equipe.html", ["#equipe"]),
    ("faq.html", ["#faq"]),
    ("contato.html", ["#contato"]),
]

# Common elements to extract
NAV_LINKS = [
    ("#sobre", "Sobre"),
    ("#servicos", "Serviços"),
    ("#portfolio", "Portfólio"),
    ("#blog", "Blog"),
    ("#equipe", "Equipe"),
    ("#faq", "FAQ"),
    ("#contato", "Contato"),
]

def extract_css():
    """Extract CSS from old-index.html and save to style.css"""
    with open(OLD_INDEX, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract CSS between <style> tags
    match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if match:
        css_content = match.group(1)
        with open(OUTPUT_DIR / "style.css", "w", encoding="utf-8") as f:
            f.write(css_content)
        print("✓ Extracted CSS to style.css")

def extract_common_elements(content):
    """Extract common HTML elements from the source file"""
    return {
        "head": extract_head(content),
        "nav": extract_nav(content),
        "mobile_menu": extract_mobile_menu(content),
        "wpp_float": extract_wpp_float(content),
        "footer": extract_footer(content),
        "scripts": extract_scripts(content),
    }

def extract_head(content):
    """Extract and update head element"""
    match = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if match:
        head = match.group(1)
        # Replace inline style with link to style.css
        head = re.sub(r'<style>.*?</style>', '', head, flags=re.DOTALL)
        # Add link to style.css after fonts
        head = re.sub(
            r'(<link href="https://fonts\.googleapis\.com/css2[^>]*>)',
            r'\1\n<link rel="stylesheet" href="style.css">',
            head
        )
        # Update title from "Polímeras EJ" to "Polimerase EJ"
        head = re.sub(r'Polímeras EJ', 'Polimerase EJ', head)
        return f"<head>\n{head}\n</head>"
    return "<head></head>"

def extract_nav(content):
    """Extract nav and update links to point to HTML files"""
    match = re.search(r'<nav[^>]*>(.*?)</nav>', content, re.DOTALL)
    if match:
        nav = match.group(1)
        # Update logo link to index.html FIRST (before loop)
        nav = re.sub(r'href="#home"', 'href="index.html"', nav)
        # Update nav links
        for old_href, label in NAV_LINKS:
            nav = re.sub(
                rf'href="{old_href}"',
                rf'href="{old_href[1:]}.html"',
                nav
            )
        # Update nav-cta
        nav = re.sub(r'href="#contato"', 'href="contato.html"', nav)
        # Update logo text to "Polimerase <span>EJ</span>"
        nav = re.sub(r'Polímeras <span>EJ</span>', 'Polimerase <span style="color:#252423;font-size:12px">EJ</span>', nav)
        return f'<nav id="navbar">\n{nav}\n</nav>'
    return ''

def extract_mobile_menu(content):
    """Extract mobile menu and update links"""
    match = re.search(r'<div class="mobile-menu"[^>]*>(.*?)</div>', content, re.DOTALL)
    if match:
        menu = match.group(1)
        # Update mobile menu links
        for old_href, label in NAV_LINKS:
            menu = re.sub(
                rf'href="{old_href}"',
                rf'href="{old_href[1:]}.html"',
                menu
            )
        # Update mobile CTA
        menu = re.sub(r'href="#contato"', 'href="contato.html"', menu)
        # Update logo text to "Polimerase <span>EJ</span>"
        menu = re.sub(r'Polímeras <span>EJ</span>', 'Polimerase <span style="color:#252423;font-size:12px">EJ</span>', menu)
        return f'<div class="mobile-menu" id="mobileMenu">\n{menu}\n</div>'
    return ''

def extract_wpp_float(content):
    """Extract floating WhatsApp button"""
    match = re.search(r'<a href="https://wa\.me/[^"]*" class="wpp-float"[^>]*>(.*?)</a>', content, re.DOTALL)
    if match:
        # Update text to "Polimerase <span>EJ</span>"
        updated_text = match.group(1).replace('Polímeras <span>EJ</span>', 'Polimerase <span style="color:#252423;font-size:12px">EJ</span>')
        # Update href and text to "Polimerase EJ" (handle both plain and percent-encoded)
        updated_href = match.group(0).replace('Polímeras EJ', 'Polimerase EJ').replace('Polímeras%20EJ', 'Polimerase%20EJ')
        return f'<a href="https://wa.me/5541998630132?text=Olá!%20Gostaria%20de%20solicitar%20uma%20proposta%20da%20Polimerase%20EJ." class="wpp-float" target="_blank" aria-label="WhatsApp">\n{updated_text}\n</a>'
    return ''

def extract_footer(content):
    """Extract footer element"""
    match = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL)
    if match:
        footer = match.group(1)
        # Update footer navigation links
        for old_href, label in NAV_LINKS:
            footer = re.sub(
                rf'href="{old_href}"',
                rf'href="{old_href[1:]}.html"',
                footer
            )
        # Update footer text to "Polimerase EJ"
        footer = re.sub(r'Polímeras EJ', 'Polimerase EJ', footer)
        return f'<footer>\n{footer}\n</footer>'
    return ''

def extract_scripts(content):
    """Extract scripts at end of document"""
    match = re.search(r'<script>(.*?)</script></body>', content, re.DOTALL)
    if match:
        return f'<script>\n{match.group(1)}\n</script>\n</body>'
    return ''

def extract_section(content, section_id):
    """Extract a specific section by ID using string find"""
    # Find the opening tag
    start = content.find(f'<section id="{section_id}">')
    if start == -1:
        return ''
    
    # Find the closing tag
    end = content.find('</section>', start)
    if end == -1:
        return ''
    
    # Extract content (skip opening tag and closing tag)
    # end points to the start of '</section>', so we use end to exclude it
    section_content = content[start+18:end]  # 18 = len('<section id="home">')
    # Update name from "Polímeras EJ" to "Polimerase EJ"
    section_content = section_content.replace('Polímeras EJ', 'Polimerase EJ')
    # Also handle percent-encoded URLs (Polímeras%20EJ -> Polimerase%20EJ)
    section_content = section_content.replace('Polímeras%20EJ', 'Polimerase%20EJ')
    return f'<section id="{section_id}">\n{section_content}\n</section>'

def extract_services_strip(content):
    """Extract services strip div"""
    match = re.search(r'<div class="services-strip"[^>]*>(.*?)</div>', content, re.DOTALL)
    if match:
        # Update name to "Polimerase <span>EJ</span>"
        content = match.group(1).replace('Polímeras <span>EJ</span>', 'Polimerase <span style="color:#252423;font-size:12px">EJ</span>')
        return f'<div class="services-strip">\n{content}\n</div>'
    return ''

def build_page(filename, sections_to_include, common_elements, content):
    """Build a complete HTML page with sections and common elements"""
    
    # Start with head
    html = common_elements["head"] + "\n<body>\n\n"
    
    # Add common elements
    html += common_elements["nav"] + "\n"
    html += common_elements["mobile_menu"] + "\n"
    html += "\n"
    
    # Add requested sections (use original content)
    for section_id in sections_to_include:
        # Strip # for section lookup
        lookup_id = section_id[1:] if section_id.startswith("#") else section_id
        html += extract_section(content, lookup_id)
    
    # Add footer and scripts
    html += "\n" + common_elements["wpp_float"] + "\n\n"
    html += common_elements["footer"] + "\n\n"
    html += common_elements["scripts"] + "\n"
    
    return html

def build_index_page(content, common_elements):
    """Build index.html with specific sections"""
    html = common_elements["head"] + "\n<body>\n\n"
    html += common_elements["nav"] + "\n"
    html += common_elements["mobile_menu"] + "\n"
    html += "\n"
    
    # Add sections in order
    sections = ["#home", ".services-strip", "#sobre", "#diferenciais", "#servicos"]
    
    for section_id in sections:
        # Strip # for section lookup
        lookup_id = section_id[1:] if section_id.startswith("#") else section_id
        html += extract_section(content, lookup_id)
        html += "\n"
    
    # Add footer, wpp, scripts
    html += "\n" + common_elements["wpp_float"] + "\n\n"
    html += common_elements["footer"] + "\n\n"
    html += common_elements["scripts"] + "\n"
    
    return html

def main():
    """Main function to build all pages"""
    print("=" * 60)
    print("Polimerase EJ - Multi-page Site Builder")
    print("=" * 60)
    
    # Read source file
    print("\nReading old-index.html...")
    with open(OLD_INDEX, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract common elements
    print("Extracting common elements...")
    common = extract_common_elements(content)
    
    # Extract CSS
    extract_css()
    
    # Build and write each page
    print("\nBuilding HTML pages...")
    
    # Build index.html
    print("  - Building index.html...")
    index_html = build_index_page(content, common)
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("    ✓ index.html created")
    
    # Build sobre.html
    print("  - Building sobre.html...")
    sobre_html = build_page("sobre.html", ["#sobre"], common, content)
    with open(OUTPUT_DIR / "sobre.html", "w", encoding="utf-8") as f:
        f.write(sobre_html)
    print("    ✓ sobre.html created")
    
    # Build servicos.html
    print("  - Building servicos.html...")
    servicos_html = build_page("servicos.html", ["#servicos"], common, content)
    with open(OUTPUT_DIR / "servicos.html", "w", encoding="utf-8") as f:
        f.write(servicos_html)
    print("    ✓ servicos.html created")
    
    # Build portfolio.html
    print("  - Building portfolio.html...")
    portfolio_html = build_page("portfolio.html", ["#portfolio"], common, content)
    with open(OUTPUT_DIR / "portfolio.html", "w", encoding="utf-8") as f:
        f.write(portfolio_html)
    print("    ✓ portfolio.html created")
    
    # Build blog.html
    print("  - Building blog.html...")
    blog_html = build_page("blog.html", ["#blog"], common, content)
    with open(OUTPUT_DIR / "blog.html", "w", encoding="utf-8") as f:
        f.write(blog_html)
    print("    ✓ blog.html created")
    
    # Build equipe.html
    print("  - Building equipe.html...")
    equipe_html = build_page("equipe.html", ["#equipe"], common, content)
    with open(OUTPUT_DIR / "equipe.html", "w", encoding="utf-8") as f:
        f.write(equipe_html)
    print("    ✓ equipe.html created")
    
    # Build faq.html
    print("  - Building faq.html...")
    faq_html = build_page("faq.html", ["#faq"], common, content)
    with open(OUTPUT_DIR / "faq.html", "w", encoding="utf-8") as f:
        f.write(faq_html)
    print("    ✓ faq.html created")
    
    # Build contato.html
    print("  - Building contato.html...")
    contato_html = build_page("contato.html", ["#contato"], common, content)
    with open(OUTPUT_DIR / "contato.html", "w", encoding="utf-8") as f:
        f.write(contato_html)
    print("    ✓ contato.html created")
    
    print("\n" + "=" * 60)
    print("✓ Site building complete!")
    print("=" * 60)
    print("\nCreated files:")
    print("  - style.css")
    print("  - index.html")
    print("  - portfolio.html")
    print("  - blog.html")
    print("  - equipe.html")
    print("  - faq.html")
    print("  - contato.html")

if __name__ == "__main__":
    main()
