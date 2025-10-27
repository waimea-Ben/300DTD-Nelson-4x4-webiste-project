# Project Review

## Addressing Relevant Implications

### User Experience and Accessibility

During the project, I focused on making the website easy to navigate and accessible for all users. This included:  
- Clear navigation bars with consistent tab highlights for Admin pages.  
- Overlay popups for trip details so users can view maps without leaving the page.  
- Form validation on all member and trip forms to prevent errors.  
- Use of ARIA roles for buttons and links, improving accessibility for screen readers.  

### Data Management and Security

To protect user data and maintain integrity:  
- Passwords are stored as hashed values and never exposed in plain text.  
- Admin-only sections are restricted based on session information (`is_admin`).  
- Forms use POST/PUT methods to ensure sensitive data (like passwords) is not exposed in URLs.  
- HTMX is used for updating sections dynamically without exposing unnecessary backend data.  

### Dynamic Interactivity

The project required live updates without full page reloads:  
- HTMX was integrated for editing members, trips, and photos inline.  
- Join/Leave trip functionality updates dynamically using forms within table rows.  
- Overlay maps and trip info load asynchronously to improve responsiveness.  
- Leaflet maps show meeting points and trip destinations, giving interactive visualization.  

### Maintainability and Modularity

To make the system easy to maintain and expand:  
- Reusable components (`member_details.jinja`, `admin_trip_details.jinja`) were created.  
- Templates extend a base layout for consistent styling.  
- CSS classes and IDs are descriptive and structured to separate layout from functionality.  
- Debug component shows request and session data, helping with troubleshooting during development.  

### Visual Design and Branding

The project focused on professional and readable presentation:  
- PicoCSS provided a clean, minimal design while allowing color customization.  
- Consistent use of headings, buttons, and tables across pages.  
- Photos and trip information are displayed with credits and responsive layouts.  
- Icons and imagery improve usability and convey meaning (e.g., meeting point and trip destination icons).  

---

## Overall Review

The project successfully delivered a functional, interactive, and visually coherent website for the Nelson 4WD Club.  

**What went well:**  
- Dynamic HTMX components and interactive maps worked reliably.  
- Clear separation of concerns in templates, CSS, and JS improved maintainability.  
- Forms and search functionality allow easy management of trips and members.  

**What didn’t go so well:**  
- Some map geocoding delays were noticed due to Nominatim API response times.  
- Initial layout adjustments required multiple iterations to ensure mobile responsiveness.  

**Impact of testing/trialling:**  
- Iterative testing of forms, overlays, and HTMX interactions helped identify bugs early.  
- Trialing maps and trip joins ensured accurate geocoding and correct session handling.  

**What would you do differently:**  
- Implement caching for map geocoding to reduce API calls and speed up overlays.  
- Enhance mobile layout for tables and images to improve small-screen usa
