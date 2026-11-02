import os
import xml.etree.ElementTree as ET
import html
import base64

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
AVATAR_PATH = os.path.join(ASSETS_DIR, "avatar.png")

os.makedirs(ASSETS_DIR, exist_ok=True)

def escape_xml(s):
    return html.escape(s, quote=True)

# ==========================================
# 1. BUILD HERO.SVG
# ==========================================
def build_hero():
    print("[1/3] Generating assets/hero.svg...")
    if os.path.exists(AVATAR_PATH):
        with open(AVATAR_PATH, "rb") as f:
            avatar_b64 = base64.b64encode(f.read()).decode("utf-8")
    else:
        avatar_b64 = ""

    CHAR_W = 11.2
    WIDTH = 1120
    HEIGHT = 770

    def gen_typing_chars(text, start_x, y, start_time, char_delay=0.035, color="#f1f5f9", bold=False, class_name="m a"):
        elements = []
        current_time = start_time
        weight_attr = ' font-weight="700"' if bold else ''
        for i, ch in enumerate(text):
            x = start_x + (i * CHAR_W)
            escaped_ch = escape_xml(ch)
            if ch == ' ':
                current_time += char_delay * 0.7
                continue
            elem = f'<text x="{x:.1f}" y="{y}" class="{class_name}" fill="{color}"{weight_attr} style="animation-delay:{current_time:.2f}s">{escaped_ch}</text>'
            elements.append(elem)
            current_time += char_delay
        return "".join(elements), current_time

    def gen_prompt(y, delay, user="root@egnake", path="~#"):
        full_str = f"{user}:{path} "
        total_w = len(full_str) * CHAR_W
        svg = f'''  <g class="a" style="animation-delay:{delay:.2f}s">
    <text y="{y}" class="m"><tspan x="56.0" fill="#ff2a5f" font-weight="700">{escape_xml(user)}</tspan><tspan fill="#64748b">:</tspan><tspan fill="#38bdf8">{escape_xml(path)}</tspan><tspan fill="#f1f5f9"> </tspan></text>
  </g>'''
        end_x = 56.0 + total_w
        return svg, end_x

    svg_lines = []
    svg_lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Ege Parlak (egnake) - Red Teamer, Exploit Developer &amp; Autonomous AI Systems">
  <defs>
    <radialGradient id="glow" cx="80%" cy="5%" r="60%">
      <stop offset="0%" stop-color="#ff2a5f" stop-opacity="0.12"/>
      <stop offset="50%" stop-color="#730c20" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#0b0c10" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#ffffff" stroke-opacity="0.015" stroke-width="1"/>
    </pattern>
    <clipPath id="win"><rect width="{WIDTH}" height="{HEIGHT}" rx="16"/></clipPath>
    <clipPath id="av"><rect x="56" y="120" width="240" height="240" rx="14"/></clipPath>
    <linearGradient id="sepGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff2a5f" stop-opacity="0.85"/>
      <stop offset="60%" stop-color="#ff2a5f" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ff2a5f" stop-opacity="0"/>
    </linearGradient>

    <style>
      .m {{ font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'SFMono-Regular', Consolas, Menlo, monospace; font-size: 16px; white-space: pre; }}
      .s {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .a {{ opacity: 0; animation: show 0.01s linear forwards; }}
      @keyframes show {{ to {{ opacity: 1; }} }}
      .blink {{ animation: blink 1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style>
  </defs>

  <g clip-path="url(#win)">
    <rect width="{WIDTH}" height="{HEIGHT}" fill="#0b0c11"/>
    <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#glow)"/>
    <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grid)"/>

    <rect width="{WIDTH}" height="48" fill="#11131a"/>
    <rect y="48" width="{WIDTH}" height="1" fill="#1c202d"/>

    <circle cx="28" cy="24" r="6.5" fill="#ff5f56"/>
    <circle cx="50" cy="24" r="6.5" fill="#febc2e"/>
    <circle cx="72" cy="24" r="6.5" fill="#28c840"/>

    <text x="{WIDTH / 2}" y="29" text-anchor="middle" class="s" font-size="13" font-weight="500" fill="#7d8699">root@egnake: ~ (zsh)</text>
    <text x="{WIDTH - 30}" y="29" text-anchor="end" class="m" font-size="12.5" fill="#505869">github.com/egnake</text>
''')

    # Command 1
    p1_svg, p1_end = gen_prompt(88, 0.30)
    svg_lines.append(p1_svg)
    t1_svg, t1_end = gen_typing_chars("neofetch --operator egnake", p1_end, 88, 0.50, char_delay=0.032)
    svg_lines.append(f'  <g>{t1_svg}</g>')

    neofetch_time = 1.40
    avatar_svg = f'''  <!-- Neofetch Avatar -->
  <g class="a" style="animation-delay:{neofetch_time:.2f}s">
    <rect x="55" y="119" width="242" height="242" rx="15" fill="none" stroke="#ff2a5f" stroke-opacity="0.25"/>
    <image x="56" y="120" width="240" height="240" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"
      href="data:image/jpeg;base64,{avatar_b64}"/>
    <rect x="56" y="120" width="240" height="240" rx="14" fill="none" stroke="#ffffff" stroke-opacity="0.10"/>
  </g>'''
    svg_lines.append(avatar_svg)

    specs_data = [
        ("Operator", "Ege Parlak (egnake)", "#ffffff", True),
        ("Role", "Red Teamer · Exploit Dev · Security AI", "#f1f5f9", False),
        ("Expertise", "Autonomous Bug Bounty · OPSEC Hardening · Sızma Testleri", "#f1f5f9", False),
        ("Flagships", "Burpnake · anon · OffSploit", "#38bdf8", True),
        ("Arsenal", "Python · Bash · Dart/Flutter · Next.js · C/C++ · Docker", "#f1f5f9", False),
        ("Homelab", "Ubuntu Core + CasaOS (Docker) · Kali Linux · Tor Net", "#f1f5f9", False),
        ("Contact", "egcaem000@gmail.com · LinkedIn: ege-parlak", "#94a3b8", False)
    ]

    specs_svg = [f'''  <!-- Neofetch Info Specs -->
  <g class="a" style="animation-delay:{neofetch_time + 0.08:.2f}s">
    <text x="325" y="138" class="m" font-size="18" font-weight="700"><tspan fill="#ff2a5f">root</tspan><tspan fill="#f1f5f9">@</tspan><tspan fill="#ff2a5f">egnake</tspan></text>
    <rect x="325" y="148" width="380" height="1.5" fill="url(#sepGrad)"/>
  </g>''']

    for idx, (label, val, val_color, is_bold) in enumerate(specs_data):
        row_y = 176 + (idx * 25)
        delay_row = neofetch_time + 0.14 + (idx * 0.05)
        bold_attr = ' font-weight="700"' if is_bold else ''
        specs_svg.append(f'''  <g class="a" style="animation-delay:{delay_row:.2f}s">
    <text x="325" y="{row_y}" class="m" fill="#ff2a5f" font-weight="700">{label}</text>
    <text x="430" y="{row_y}" class="m" fill="{val_color}"{bold_attr}>{val}</text>
  </g>''')

    swatches = ["#0b0c11", "#330810", "#5c0a1a", "#8a0f26", "#bd1434", "#ff2a5f", "#ff6b8b", "#38bdf8", "#00e599", "#f1f5f9"]
    swatch_rects = []
    for si, sc in enumerate(swatches):
        sx = 325 + (si * 40)
        swatch_rects.append(f'<rect x="{sx}" y="360" width="34" height="18" rx="3.5" fill="{sc}" stroke="#1e2433" stroke-width="1"/>')

    specs_svg.append(f'''  <g class="a" style="animation-delay:{neofetch_time + 0.55:.2f}s">
    {''.join(swatch_rects)}
  </g>''')
    svg_lines.append("\n".join(specs_svg))

    # Command 2
    cmd2_time = neofetch_time + 0.80
    p2_svg, p2_end = gen_prompt(422, cmd2_time)
    svg_lines.append(p2_svg)
    t2_svg, t2_end = gen_typing_chars("cat mission.md", p2_end, 422, cmd2_time + 0.15, char_delay=0.035)
    svg_lines.append(f'  <g>{t2_svg}</g>')

    out2_time = t2_end + 0.12
    svg_lines.append(f'''  <g class="a" style="animation-delay:{out2_time:.2f}s">
    <text x="56" y="452" class="m"><tspan fill="#ff2a5f" font-weight="700">❯ </tspan><tspan fill="#f1f5f9">"Güvenliği hem protokol hem kod seviyesinde ele alıyor; sistemleri kırarak açıklarını, otonom araçlar inşa ederek sınırlarını keşfediyorum."</tspan></text>
  </g>
  <g class="a" style="animation-delay:{out2_time + 0.14:.2f}s">
    <text x="56" y="476" class="m"><tspan fill="#ff2a5f" font-weight="700">❯ </tspan><tspan fill="#8c97a8">"Engineering autonomous offensive AI, OPSEC hardening toolkits, and weaponized exploit frameworks."</tspan></text>
  </g>''')

    # Command 3
    cmd3_time = out2_time + 0.38
    p3_svg, p3_end = gen_prompt(516, cmd3_time)
    svg_lines.append(p3_svg)
    t3_svg, t3_end = gen_typing_chars("egnake-sec --flagships", p3_end, 516, cmd3_time + 0.15, char_delay=0.030)
    svg_lines.append(f'  <g>{t3_svg}</g>')

    out3_time = t3_end + 0.12
    projects = [
        ("┌─", "[Burpnake]", "Autonomous AI Bug Bounty", "HTTP Traffic Intercept · DOM Recon · Vulnerability Chaining & Auto-PoC"),
        ("├─", "[anon]    ", "Advanced Linux OPSEC Toolkit", "Transparent Tor Routing · RAM Wiping · MAC Spoofing · Anti-MITM"),
        ("└─", "[OffSploit]", "AI Exploit Intelligence Engine", "Ollama / Local RAG · Zafiyet Eşleştirme · Otonom PoC Asistanı")
    ]

    for pi, (tree, p_name, p_role, p_tech) in enumerate(projects):
        row_y = 546 + (pi * 24)
        p_delay = out3_time + (pi * 0.09)
        svg_lines.append(f'''  <g class="a" style="animation-delay:{p_delay:.2f}s">
    <text x="56" y="{row_y}" class="m"><tspan fill="#475569">{tree} </tspan><tspan fill="#ff2a5f" font-weight="700">{escape_xml(p_name):<11}</tspan><tspan fill="#475569"> :: </tspan><tspan fill="#f1f5f9">{escape_xml(p_role):<30}</tspan><tspan fill="#525d70"> → </tspan><tspan fill="#8c97a8">{escape_xml(p_tech)}</tspan></text>
  </g>''')

    # Command 4
    cmd4_time = out3_time + 0.42
    p4_svg, p4_end = gen_prompt(646, cmd4_time)
    svg_lines.append(p4_svg)
    t4_svg, t4_end = gen_typing_chars("init-handshake --target contact", p4_end, 646, cmd4_time + 0.15, char_delay=0.030)
    svg_lines.append(f'  <g>{t4_svg}</g>')

    out4_time = t4_end + 0.12
    svg_lines.append(f'''  <g class="a" style="animation-delay:{out4_time:.2f}s">
    <text x="56" y="674" class="m"><tspan fill="#00e599">[✓]</tspan><tspan fill="#00e599"> Handshake ACK. </tspan><tspan fill="#f1f5f9">Açık kaynak araçlar, siber güvenlik araştırmaları ve iş birlikleri için bir mesaj uzağınızdayım.</tspan></text>
  </g>''')

    # Final prompt
    final_time = out4_time + 0.28
    p_fin_svg, p_fin_end = gen_prompt(714, final_time)
    svg_lines.append(p_fin_svg)

    svg_lines.append(f'''  <g class="a" style="animation-delay:{final_time + 0.08:.2f}s">
    <rect x="{p_fin_end:.1f}" y="698" width="9.5" height="19" fill="#ff2a5f" class="blink"/>
  </g>''')

    svg_lines.append(f'''
    <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.06"/>
    <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="16" fill="none" stroke="#ff2a5f" stroke-opacity="0.18"/>
  </g>
</svg>''')

    hero_path = os.path.join(ASSETS_DIR, "hero.svg")
    with open(hero_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    ET.parse(hero_path)
    print("  -> assets/hero.svg created and validated.")


# ==========================================
# 2. BUILD ACTION BUTTONS
# ==========================================
def build_buttons():
    print("[2/3] Generating action buttons in assets/...")
    buttons = {
        "btn-github.svg": {
            "title": "GitHub Projeleri",
            "icon": '''<g transform="translate(24, 18) scale(1.0)">
              <path fill="#ff2a5f" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
            </g>''',
            "primary": True
        },
        "btn-linkedin.svg": {
            "title": "LinkedIn",
            "icon": '''<g transform="translate(26, 18) scale(1.0)">
              <path fill="#0a66c2" d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.64c-.9 0-1.63.73-1.63 1.63s.73 1.63 1.63 1.63 1.63-.73 1.63-1.63-.73-1.63-1.63-1.63z"/>
            </g>''',
            "primary": False
        },
        "btn-mail.svg": {
            "title": "E-Posta İletişim",
            "icon": '''<g transform="translate(25, 18) scale(1.0)">
              <rect x="2" y="4" width="20" height="16" rx="3" fill="none" stroke="#ff2a5f" stroke-width="2"/>
              <path d="M3 6l9 7 9-7" fill="none" stroke="#ff2a5f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </g>''',
            "primary": False
        }
    }

    for fname, cfg in buttons.items():
        title = cfg["title"]
        icon = cfg["icon"]
        is_primary = cfg["primary"]
        bg_fill = "#140a0f" if is_primary else "#0c0e15"
        border_color = "#ff2a5f" if is_primary else "#202636"
        border_width = "1.8" if is_primary else "1.2"
        text_color = "#ffffff" if is_primary else "#e2e8f0"
        arrow_color = "#ff2a5f" if is_primary else "#94a3b8"

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="250" height="60" viewBox="0 0 250 60" role="img" aria-label="{title}">
  <defs>
    <style>
      .btn-bg {{ transition: all 0.25s ease; }}
      svg:hover .btn-bg {{ stroke: #ff2a5f; fill: #171b26; }}
      .btn-text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; font-size: 16px; font-weight: 600; }}
    </style>
  </defs>
  <rect class="btn-bg" x="1.5" y="1.5" width="247" height="57" rx="14" fill="{bg_fill}" stroke="{border_color}" stroke-width="{border_width}"/>
  {icon}
  <text x="66" y="36" class="btn-text" fill="{text_color}">{title}</text>
  <text x="224" y="36" text-anchor="end" class="btn-text" font-size="18" fill="{arrow_color}" fill-opacity="0.85">↗</text>
</svg>'''
        p = os.path.join(ASSETS_DIR, fname)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg)
        ET.parse(p)
        print(f"  -> assets/{fname} created and validated.")


# ==========================================
# 3. BUILD REPO CARDS
# ==========================================
def build_cards():
    print("[3/3] Generating repository cards in assets/...")
    def create_card(filename, title, tag, desc, chips, accent_color, icon_svg):
        width = 540
        height = 200
        chips_svg = []
        chip_x = 28
        for c in chips:
            c_w = len(c) * 7.5 + 18
            chips_svg.append(f'''<g transform="translate({chip_x}, 152)">
              <rect width="{c_w}" height="24" rx="6" fill="#141824" stroke="#252d40" stroke-width="1"/>
              <text x="{c_w/2}" y="16" text-anchor="middle" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="600" fill="#94a3b8">{c}</text>
            </g>''')
            chip_x += c_w + 8

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{title}: {tag}">
  <defs>
    <radialGradient id="cardGlow_{title}" cx="10%" cy="10%" r="80%">
      <stop offset="0%" stop-color="{accent_color}" stop-opacity="0.12"/>
      <stop offset="60%" stop-color="{accent_color}" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#090a0f" stop-opacity="0"/>
    </radialGradient>
    <style>
      .card-bg {{ transition: all 0.25s ease; }}
      svg:hover .card-bg {{ stroke: {accent_color}; stroke-opacity: 0.6; fill: #10131d; }}
      .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 20px; font-weight: 700; fill: #ffffff; }}
      .tag {{ font-family: 'JetBrains Mono', Consolas, monospace; font-size: 11px; font-weight: 700; fill: {accent_color}; letter-spacing: 0.8px; }}
      .desc {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 13.5px; fill: #94a3b8; line-height: 1.4; }}
      .action {{ font-family: 'JetBrains Mono', Consolas, monospace; font-size: 12px; font-weight: 600; fill: {accent_color}; }}
    </style>
  </defs>

  <rect class="card-bg" x="1.5" y="1.5" width="{width - 3}" height="{height - 3}" rx="16" fill="#0c0e15" stroke="#1f2536" stroke-width="1.5"/>
  <rect x="1.5" y="1.5" width="{width - 3}" height="{height - 3}" rx="16" fill="url(#cardGlow_{title})"/>

  <g transform="translate(28, 24)">
    <rect width="44" height="44" rx="10" fill="#141824" stroke="#252d40" stroke-width="1"/>
    {icon_svg}
  </g>

  <text x="84" y="38" class="tag">{tag}</text>
  <text x="84" y="60" class="title">{title}</text>

  <g transform="translate({width - 45}, 28)">
    <circle cx="12" cy="12" r="14" fill="#141824" stroke="#252d40" stroke-width="1"/>
    <text x="12" y="17" text-anchor="middle" class="action" font-size="14">↗</text>
  </g>

  <text x="28" y="98" class="desc">{desc[0]}</text>
  <text x="28" y="120" class="desc">{desc[1]}</text>

  {''.join(chips_svg)}
</svg>'''
        p = os.path.join(ASSETS_DIR, filename)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg)
        ET.parse(p)
        print(f"  -> assets/{filename} created and validated.")

    burpnake_icon = '''<g transform="translate(10, 10)">
  <path fill="#ff2a5f" d="M12 2a4 4 0 0 0-4 4v1H6a2 2 0 0 0-2 2v2a2 2 0 0 0 1.15 1.82A6 6 0 0 0 5 15.5V17a3 3 0 0 0 3 3h8a3 3 0 0 0 3-3v-1.5a6 6 0 0 0-.15-2.68A2 2 0 0 0 20 11V9a2 2 0 0 0-2-2h-2V6a4 4 0 0 0-4-4zm-2 5V6a2 2 0 1 1 4 0v1h-4zm-4 4h2v2H6v-2zm12 0h2v2h-2v-2zm-9 4h6a4 4 0 0 1-6 0z"/>
</g>'''

    create_card(
        "card-burpnake.svg",
        "BurpNake",
        "AUTONOMOUS AI BUG BOUNTY PLATFORM",
        [
            "Intercepts HTTP traffic, performs deep DOM recon &amp; chains vulnerabilities.",
            "Generates verified weaponized PoC exploits entirely on its own using AI."
        ],
        ["Python 3.12+", "FastAPI", "Playwright", "Auto-PoC", "AI Recon"],
        "#ff2a5f",
        burpnake_icon
    )

    anon_icon = '''<g transform="translate(10, 10)">
  <path fill="#38bdf8" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
</g>'''

    create_card(
        "card-anon.svg",
        "ANON",
        "ADVANCED LINUX OPSEC &amp; PRIVACY SUITE",
        [
            "All-in-one operational security &amp; anti-forensics toolkit for Linux and WSL.",
            "Transparent Tor routing, MAC spoofing, RAM wiping &amp; anti-MITM defenses."
        ],
        ["Bash", "Tor Network", "Anti-Forensics", "MAC Spoof", "Iptables"],
        "#38bdf8",
        anon_icon
    )

if __name__ == "__main__":
    print("=== Rebuilding All Assets for egnake/egnake ===")
    build_hero()
    build_buttons()
    build_cards()
    print("=== All Assets Successfully Generated & Validated ===")
