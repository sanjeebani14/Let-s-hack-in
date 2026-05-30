---
name: InRoad
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#bdc8d1'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#87929a'
  outline-variant: '#3e484f'
  surface-tint: '#7bd0ff'
  primary: '#8ed5ff'
  on-primary: '#00354a'
  primary-container: '#38bdf8'
  on-primary-container: '#004965'
  inverse-primary: '#00668a'
  secondary: '#bdc2ff'
  on-secondary: '#131e8c'
  secondary-container: '#2f3aa3'
  on-secondary-container: '#a8afff'
  tertiary: '#45e3ce'
  on-tertiary: '#003731'
  tertiary-container: '#07c7b2'
  on-tertiary-container: '#004d44'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#c4e7ff'
  primary-fixed-dim: '#7bd0ff'
  on-primary-fixed: '#001e2c'
  on-primary-fixed-variant: '#004c69'
  secondary-fixed: '#e0e0ff'
  secondary-fixed-dim: '#bdc2ff'
  on-secondary-fixed: '#000767'
  on-secondary-fixed-variant: '#2f3aa3'
  tertiary-fixed: '#62fae3'
  tertiary-fixed-dim: '#3cddc7'
  on-tertiary-fixed: '#00201c'
  on-tertiary-fixed-variant: '#005047'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  data-lg:
    fontFamily: Space Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0.02em
  data-sm:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style
The design system is engineered to evoke a sense of "Career Intelligence"—a visionary, high-performance environment where AI-driven insights feel both authoritative and accessible. The aesthetic leans into a **Futuristic Minimalist** style, blending the precision of developer tools with the elegance of premium enterprise software. 

The interface leverages a "Hackathon-ready" energy: it is lean, fast, and dense with information without being cluttered. Key attributes include:
- **High-Fidelity Utility:** A focus on data density and clear information architecture.
- **AI-Native Atmosphere:** Utilizing light-glows and translucency to signal "active" intelligence and background processing.
- **Technical Sophistication:** A blend of deep obsidian surfaces and vibrant, neon-inflected accents that suggest a high-tech, digital-first ecosystem.

## Colors
The palette is optimized for a high-contrast dark mode environment. 

- **Primary (Cyan):** Used for primary actions, focus states, and the core "AI active" identity.
- **Secondary (Violet):** Used for progression metrics, career pathing visualizations, and secondary highlights.
- **Tertiary (Emerald):** Reserved for "Success" states and positive growth indicators.
- **Background Tiers:** The foundation uses `#0F172A` (Midnight), with elevated surfaces using slightly lighter, desaturated variations to create depth through tonal layering rather than pure black.
- **Data Accents:** Use vibrant, high-saturation versions of the primary and secondary colors for charts to ensure legibility against the deep background.

## Typography
The typography strategy employs a dual-font system to separate narrative content from technical data.

1.  **UI & Narrative (Geist/Inter):** Geist is used for headlines to provide a sharp, technical edge. Inter handles the bulk of body copy for maximum readability during long-form career analysis.
2.  **Data & Insights (Space Grotesk):** All numerical scores, percentages, and labels use Space Grotesk. Its geometric construction reinforces the "intelligence" aspect of the dashboard and provides a distinct visual cue that the user is looking at calculated data points.
3.  **Scale:** Use tight tracking on large headlines and increased tracking on small data labels for a modern, architectural feel.

## Layout & Spacing
The layout follows a **Fixed-Fluid Hybrid Grid**. 

- **Sidebar:** A fixed 280px navigation rail that can collapse into a 64px icon-only bar.
- **Main Canvas:** A 12-column fluid grid for dashboard widgets.
- **Widgets:** Should utilize a modular 8px base unit. Gaps between widgets are consistently 24px (md) to maintain a breathable, organized look.
- **Mobile:** Reflows to a single-column stack. Margins reduce to 16px. Top navigation replaces the sidebar.

## Elevation & Depth
Depth in this design system is achieved through **Glassmorphism** and **Luminous Layering** rather than traditional drop shadows.

- **Surface 0:** The base background (#0F172A).
- **Surface 1 (Cards):** Semi-transparent fills (e.g., `rgba(30, 41, 59, 0.5)`) with a 1px border of `rgba(255, 255, 255, 0.1)` and a `backdrop-filter: blur(12px)`.
- **Active Glow:** Interactive elements or AI-suggested items feature a subtle outer glow (Bloom) using the Primary Cyan, with a spread of 15-20px and low opacity (15%).
- **Inner Borders:** Use "Ghost Borders"—thin, 1px strokes that are slightly lighter than the surface color to define boundaries without adding visual weight.

## Shapes
The shape language is "Soft-Technical." We use a conservative corner radius (0.25rem to 0.75rem) to maintain a professional, high-performance tool aesthetic while avoiding the harshness of 0px corners.

- **Standard Elements:** 4px (0.25rem) for inputs and small buttons.
- **Dashboard Cards:** 8px (0.5rem) to provide a distinct container feel.
- **Feature Highlights:** 12px (0.75rem) for large promotional or AI "insight" blocks.
- **Icons:** Use linear, 2px stroke icons with slightly rounded caps to match the UI's geometry.

## Components
- **Buttons:** 
  - *Primary:* Solid Cyan gradient with black text for maximum contrast.
  - *Secondary:* Ghost style with 1px Violet border and subtle hover glow.
- **AI Insights (Chips):** Small, pill-shaped tags using the Secondary Violet color with a 10% opacity background and 100% opacity text.
- **Data Visualization:** Charts should use thick 3px lines for trends. Use "Glow Lines"—SVG paths with a Gaussian blur filter underneath the main stroke to simulate a neon light.
- **Input Fields:** Darker than the card surface, using a 1px "Focus" border in Primary Cyan. Labels should always use the "data-sm" typography style.
- **Progress Rings:** Used for "Career Match" scores. Utilize a dual-stroke method: a dark track and a glowing primary-color indicator.
- **Feedback States:** Micro-interactions (like hovering over a skill card) should trigger a subtle scaling (1.02x) and an increase in the backdrop blur intensity.