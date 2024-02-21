# Web Reservation System
### Video Demo:  <https://youtu.be/FsdNpunNayk>
## Description:

### Overview
This project presents a web-based reservation system, integrated into a concept artist's website. It's designed to provide an intuitive and efficient way for users to view and book art classes. The website also showcases the artist's portfolio and provides information about the studio, making it a comprehensive platform for both art enthusiasts and potential students.

The concept artist's credit goes to Peiyao Wang, and I appreciate her for letting me use her art pieces as my display for the gallery page.

## Features
### User Authentication
**Register:** New users can sign up by providing their username, password, and personal details. The system ensures that usernames are unique and passwords are securely stored.
**Login/Logout:** Users can log in to access personalized features like making and managing reservations. A logout option is also provided for security.

### Class Schedule Viewing
**Dynamic Schedule Display:** The website displays a schedule of available art classes, categorized by days and types (adults or kids classes). This schedule is dynamically generated from the SQLite database.

### Reservation Management System
**Making Reservations:** Logged-in users can make reservations for classes. The system captures essential details like class choice, user's name, and contact information.
**Managing Reservations:** Users can view their current reservations and have the option to cancel them if needed.

### Artist's Portfolio
**Gallery:** A dedicated section showcases the artist's work, giving visitors a glimpse into the style and quality of art they can expect or learn.

### Additional Information
**About Page:** This page provides background information about the artist and the studio, enriching the visitor's understanding and connection with the artist.
**Contact Page:** Users can find contact details and additional information on how to reach out to the studio, along with its business hours from Monday to Sunday.

## Technical Details
### Technology Stack
**Frontend:** HTML, CSS (Bootstrap for styling), Jinja2 for templating.
**Backend:** Python (Flask framework), SQLite for the database.
**Security:** User authentication, session management, and password hashing.

### Database Schema
**Users:** Stores user credentials and personal information.
**Classes:** Contains details of the art classes, including name, schedule, and type.
**Reservations:** Records the reservations made by users, linking to the users and classes tables.
**Foreign Keys:** Those are made to enable cross-referencing by the functions in app.py. e.g. displays current reservations in the management system based on user login session.

### Directory Structure
**/templates:** Contains HTML templates for different pages of the website.
**/static:** Stores static files like CSS, JavaScript, and images.
**app.py:** The main Flask application file.
**helpers.py:** Includes utility functions used across the application.
**reservation.db:** The SQLite database file.

## Setup and Installation
### Requirements
- Python 3
- Flask
- SQLite
- Jinja

### Running the Application

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install dependencies: pip install -r requirements.txt.
4. Run the Flask application: flask run.
5. Access the website via localhost.

*Sorry, there's no .exe available for this one.*

## Usage
### User Registration and Login
- Access the registration form via the 'Register' link on the homepage.
- Please do not use your normal passwords for the site as we do not regularly maintain it nor do we actively do penetration testing.
- After registration, log in using the 'Login' link.

### Making a Reservation
- Logged-in users can view the class schedule under the 'Make a Reservation' section.
- Select a desired class time and fill in the reservation details.
- Submit the form to confirm the reservation, you will see the "success" box flash at the top of the webpage.

### Managing Reservations
- View and manage your reservations under the 'Manage Reservation' section.
- Use the 'Cancel' option to cancel any existing reservation.
- Note that the system does not account for the capacity of the classes at the moment, but can be easily added in the backend once operational.

## Support
There's no current support system setup, use at your own risk and please avoid using passwords that you share with other accounts.

## Future and Beyond
Similar systems can be easily implemented to your own website and I am currently working on a shop page with integrated payment system, so it can be a full-feature webapp for my personal website. The stylesheet will be a work in progress as well, as I will update the aesthetics of the webpage using custom typeface.

## License
This project is licensed under the MIT License. Please see the license file for more detail.
