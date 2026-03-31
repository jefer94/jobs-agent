// Custom sb2nov-colorized theme with indigo/violet/cyan/rose palette
// Based on rendercv sb2nov theme with custom colors and frame

#let sb2nov-colorized-theme = (
  // Color palette: indigo, violet, cyan, rose
  primary-color: rgb("4f46e5"),    // indigo-600
  secondary-color: rgb("7c3aed"),   // violet-600
  accent-color: rgb("0891b2"),     // cyan-600
  highlight-color: rgb("e11d48"),   // rose-600
  text-color: rgb("1f2937"),        // gray-800
  light-gray: rgb("9ca3af"),        // gray-400

  // Page setup with frame - reduced margins for more content
  page: (
    paper: "a4",
    margin: (top: 1.2cm, bottom: 1.2cm, left: 1.5cm, right: 1.5cm),
  ),

  // Frame decoration
  frame: (
    enabled: true,
    stroke: 1.5pt + rgb("4f46e5"),  // indigo border
    radius: 0pt,
    inset: 0.5cm,
  ),

  // Layout - single column
  layout: (
    columns: 1,
    section-spacing: 0.8em,
    entry-spacing: 0.6em,
  ),

  // Header styling - creative font, reduced size
  header: (
    name: (
      font: "Playfair Display",      // Creative serif font
      size: 20pt,                   // Reduced from 24pt
      weight: "bold",
      color: rgb("4f46e5"),          // indigo
    ),
    subtitle: (
      font: "Inter",
      size: 10pt,
      weight: "regular",
      color: rgb("7c3aed"),          // violet
    ),
  ),

  // Contact info with icons - added Medium
  contact: (
    font: "Inter",
    size: 9pt,
    color: rgb("0891b2"),            // cyan
    use-icons: true,
    icon-color: rgb("4f46e5"),       // indigo
    separator: " · ",
    networks: ("linkedin", "github", "medium", "website"),  // Added medium
  ),

  // Section headers
  section: (
    font: "Inter",
    size: 11pt,
    weight: "bold",
    color: rgb("e11d48"),            // rose
    underline: true,
    underline-color: rgb("4f46e5"),  // indigo
    underline-thickness: 1pt,
  ),

  // Experience entries - compact date + location format like "07/2025 – actualidad | Colombia"
  experience: (
    company-font: "Inter",
    company-size: 10pt,
    company-weight: "bold",
    company-color: rgb("4f46e5"),    // indigo

    position-font: "Inter",
    position-size: 9pt,
    position-weight: "regular",
    position-color: rgb("7c3aed"), // violet

    // Compact inline date format
    date-format: "MM/YYYY",
    date-location-separator: " | ",
    show-location-inline: true,
    date-color: rgb("0891b2"),       // cyan
    date-size: 9pt,

    location-color: rgb("9ca3af"),   // gray
    location-size: 8pt,
  ),

  // Skills - single column layout
  skills: (
    category-font: "Inter",
    category-size: 9pt,
    category-weight: "bold",
    category-color: rgb("7c3aed"),   // violet

    details-color: rgb("1f2937"),    // gray-800
    details-size: 9pt,
    layout: "inline",                // Single line per category, not columns
  ),

  // Education - inline format (institution + degree on same line)
  education: (
    inline: true,                    // Institution and degree on one line
    show-dates: true,
    date-format: "YYYY",

    institution-font: "Inter",
    institution-size: 10pt,
    institution-weight: "bold",
    institution-color: rgb("4f46e5"), // indigo

    degree-font: "Inter",
    degree-size: 9pt,
    degree-weight: "regular",
    degree-color: rgb("7c3aed"),     // violet

    date-color: rgb("0891b2"),       // cyan
    date-size: 9pt,
  ),

  // Links
  links: (
    color: rgb("0891b2"),            // cyan
    underline: false,
  ),

  // Profile section - conditional display
  profile: (
    default: "auto",                 // 'auto', 'always', 'never'
    max-content-length: 800,         // Approximate character limit
  ),
)

// Export the theme
#let use-theme = sb2nov-colorized-theme
