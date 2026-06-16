from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_PATH = OUT_DIR / "chicken-kings-vault-summary.pdf"


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=23,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="Subtle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10,
        textColor=colors.HexColor("#475569"),
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=3,
        spaceBefore=0,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCompact",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=10,
        textColor=colors.HexColor("#111827"),
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletCompact",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.0,
        leading=9.6,
        leftIndent=10,
        firstLineIndent=-6,
        bulletIndent=0,
        spaceAfter=1.5,
        textColor=colors.HexColor("#111827"),
    )
)
styles.add(
    ParagraphStyle(
        name="MetaRight",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#334155"),
    )
)


def bullet(text: str) -> Paragraph:
    return Paragraph(text, styles["BulletCompact"], bulletText="-")


story = []

header = Table(
    [
        [
            Paragraph("Chicken King's Vault", styles["DocTitle"]),
            Paragraph("Repo summary<br/>1 page", styles["MetaRight"]),
        ],
        [
            Paragraph(
                "Static browser game vault with a landing page, searchable catalog, and many individual HTML game wrappers.",
                styles["Subtle"],
            ),
            Paragraph("Evidence date: 2026-04-06", styles["Subtle"]),
        ],
    ],
    colWidths=[5.4 * inch, 1.3 * inch],
)
header.setStyle(
    TableStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]
    )
)
story.append(header)
story.append(Spacer(1, 0.12 * inch))

left_sections = [
    [
        Paragraph("What It Is", styles["Section"]),
        Paragraph(
            "A static website called Chicken King's Vault that presents a curated browser-playable game collection. The repo includes a home page, a full catalog page, and many packaged game pages/assets served directly as static files.",
            styles["BodyCompact"],
        ),
    ],
    [
        Paragraph("Who It's For", styles["Section"]),
        Paragraph(
            "Primary persona: players who want a large, no-install browser game library they can browse and launch quickly from one site.",
            styles["BodyCompact"],
        ),
    ],
    [
        Paragraph("What It Does", styles["Section"]),
        bullet("Shows a branded home page with featured games and a CTA to browse the catalog."),
        bullet("Lists <b>726</b> games in the main catalog UI."),
        bullet("Lets users search titles client-side as they type."),
        bullet("Supports genre filtering across categories like Action, Platformer, RPG, Puzzle, and more."),
        bullet("Supports A-Z and Z-A sorting for visible games."),
        bullet("Displays cover art and links each card to a dedicated HTML game page."),
        bullet("Includes Vercel analytics wiring and AdSense script tags in the top-level pages."),
    ],
]

right_sections = [
    [
        Paragraph("How It Works", styles["Section"]),
        bullet("<b>Entry pages:</b> <code>index.html</code> is the landing page; <code>gamepage.html</code> is the full catalog."),
        bullet("<b>Catalog data:</b> game entries are hardcoded as anchor cards in <code>gamepage.html</code>, each pointing to a game HTML file and thumbnail."),
        bullet("<b>Client logic:</b> inline JavaScript in <code>gamepage.html</code> applies search, filter, count updates, and A-Z/Z-A sorting in the browser."),
        bullet("<b>Game delivery:</b> many standalone HTML pages load local assets and packaged runtimes such as Construct scripts, Unity WebGL builds, and media folders."),
        bullet("<b>Hosting/ops:</b> <code>.vercel/project.json</code> shows the repo is linked to a Vercel project; <code>/_vercel/insights/script.js</code> is referenced for analytics."),
        bullet("<b>Offline:</b> service worker registration helper exists in <code>scripts/register-sw.js</code>, but <b>sw.js not found in repo</b>."),
    ],
    [
        Paragraph("How To Run", styles["Section"]),
        bullet("Open the repo root for the site: <code>chickenkingsvault/chickenkingsvault</code>."),
        bullet("No <code>package.json</code> or build pipeline was found in repo; this appears to be a static site."),
        bullet("Serve the folder with a simple static server, for example: <code>python -m http.server 8000</code>."),
        bullet("Open <code>http://localhost:8000/index.html</code> to start."),
        bullet("Alternative: deploy/preview as a static project on Vercel using the existing project link. Exact Vercel build settings were not found in repo."),
    ],
]

content = Table(
    [[left_sections, right_sections]],
    colWidths=[3.32 * inch, 3.32 * inch],
    hAlign="LEFT",
)
content.setStyle(
    TableStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )
)
story.append(content)
story.append(Spacer(1, 0.08 * inch))
story.append(
    Paragraph(
        "Evidence used: README.md, index.html, gamepage.html, .vercel/project.json, scripts/register-sw.js, scripts/offlineclient.js, and repository file layout.",
        styles["Subtle"],
    )
)

doc = SimpleDocTemplate(
    str(PDF_PATH),
    pagesize=letter,
    leftMargin=0.52 * inch,
    rightMargin=0.52 * inch,
    topMargin=0.48 * inch,
    bottomMargin=0.42 * inch,
)
doc.build(story)

print(PDF_PATH)
