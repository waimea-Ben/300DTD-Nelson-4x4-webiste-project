# Nelson 4X4 Club

by Ben Martin  

---

## Project Description  

This project is a fully functional website for the **Nelson 4X4 Club**, built to provide club members with information, trip management, and media sharing. The site supports both public visitors and registered members, with additional admin functionality for club organisers.  

### Key Features  

- User-friendly **homepage** with information about the club and upcoming events  
- **Member system** with login, profiles, and role-based permissions (admin/member)  
- **Trip management** – create, edit, and view upcoming and past 4X4 trips  
- **Photo gallery** – upload and manage trip photos with credits  
- **Search and filtering** – quickly find trips, members, or past events  
- **Admin dashboard** – manage members, trips, photos, and site settings  
- **Responsive design** for mobile, tablet, and desktop use  
- **Secure database integration** with permissions for different roles  

---

## Project Links  

- [GitHub repo for the project](https://github.com/waimea-Ben/300DTD-Nelson-4x4-webiste-project)  
- [Documentation](https://waimea-ben.github.io/300DTD-Nelson-4x4-webiste-project/)  
- [Live web app](https://three00dtd-nelson-4x4-webiste-project.onrender.com) 

---

## Project Files  

- Program source code can be found in the [app](app/) folder  
- Project documentation is in the [docs](docs/) folder, including:  
  - [Project requirements](docs/0-requirements.md)  
  - Development sprints:  
    - [Sprint 1](docs/1-sprint-1-prototype.md) - Development of a prototype  
    - [Sprint 2](docs/2-sprint-2-mvp.md) - Development of a minimum viable product (MVP)  
    - [Sprint 3](docs/3-sprint-3-refinement.md) - Final refinements  
  - [Final review](docs/4-review.md)  
  - [Setup guide](docs/setup.md) - Project and hosting setup  

---

## Project Details  

This is a digital media and database project for **NCEA Level 3**, assessed against standards [91902](docs/as91902.pdf) and [91903](docs/as91903.pdf).  

The project is a web app that uses [Flask](https://flask.palletsprojects.com) for the server back-end, connecting to a **SQLite** (development) and **Turso** (production) database. The final deployment of the app is on [Render](https://render.com/).  

The app uses [Jinja2](https://jinja.palletsprojects.com/templates/) templating for structuring pages and data, and [PicoCSS](https://picocss.com/) as the base for styling, with custom CSS for refinement.  

### Complex Database Techniques  

- Structured data with multiple related tables (trips, members, photos, site settings)  
- Implemented **CRUD operations** (create, read, update, delete) across all core tables  
- Used **SQL joins** to combine trips, leaders, and photos in custom views  
- Implemented **role-based permissions** (admin vs member vs public)  
- Dynamic linking between the database and front-end templates  

### Complex Digital Media (Web) Techniques  

- Responsive design for desktop and mobile  
- Interactive photo gallery with upload and delete functions  
- Integration of original assets (club logo, media styling)  
- Dynamic content loading using **htmx** for seamless updates  
- Automated deployment to Render with database syncing  
- Secure login and session handling  
- Customised, user-friendly UI following industry conventions  
