#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================


from flask import Flask, render_template, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import html
import base64

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.auth    import login_required, admin_required
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now
from datetime import *

# Create the app
app = Flask(__name__)

@app.template_filter('b64encode')
def b64encode_filter(data):
    if data is None:
        return ""
    return base64.b64encode(data).decode()

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps



#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def home_past_trips():
    with connect_db() as client:
        # Get all the things from the DB
        sql = """
            SELECT *

            FROM trips
            WHERE date(trips.date) < date('now')
            ORDER BY trips.date DESC
        """
        params=[]
        result = client.execute(sql, params)
        past_trips = result.rows

        # And show them on the page
        return render_template("pages/home.jinja",  past_trips = past_trips)


#-----------------------------------------------------------
# Past trips page route
#-----------------------------------------------------------
@app.get("/past/")
def past_trips():
    with connect_db() as client:
        # Get all past trips
        sql = """
            SELECT trips.*, trip_photos.*
            FROM trips
            LEFT JOIN trip_photos ON trip_photos.trip_id = trips.id
            WHERE date(trips.date) < date('now')
            ORDER BY trips.date DESC;

        """
        result = client.execute(sql)
        past_trips = result.rows 



    return render_template("pages/past.jinja", past_trips=past_trips)


# #-----------------------------------------------------------
# # Things page route - Show all the things, and new thing form
# #-----------------------------------------------------------
# @app.get("/things/")
# def show_all_things():
#     with connect_db() as client:
#         # Get all the things from the DB
#         sql = """
#             SELECT things.id,
#                    things.name,
#                    users.name AS owner

#             FROM things
#             JOIN users ON things.user_id = users.id

#             ORDER BY things.name ASC
#         """
#         params=[]
#         result = client.execute(sql, params)
#         things = result.rows

#         # And show them on the page
#         return render_template("pages/things.jinja", things=things)


# #-----------------------------------------------------------
# # Thing page route - Show details of a single thing
# #-----------------------------------------------------------
# @app.get("/thing/<int:id>")
# def show_one_thing(id):
#     with connect_db() as client:
#         # Get the thing details from the DB, including the owner info
#         sql = """
#             SELECT things.id,
#                    things.name,
#                    things.price,
#                    things.user_id,
#                    users.name AS owner

#             FROM things
#             JOIN users ON things.user_id = users.id

#             WHERE things.id=?
#         """
#         params = [id]
#         result = client.execute(sql, params)

#         # Did we get a result?
#         if result.rows:
#             # yes, so show it on the page
#             thing = result.rows[0]
#             return render_template("pages/thing.jinja", thing=thing)

#         else:
#             # No, so show error
#             return not_found_error()


# #-----------------------------------------------------------
# # Route for adding a thing, using data posted from a form
# # - Restricted to logged in users
# #-----------------------------------------------------------
# @app.post("/add")
# @login_required
# def add_a_thing():
#     # Get the data from the form
#     name  = request.form.get("name")
#     price = request.form.get("price")

#     # Sanitise the text inputs
#     name = html.escape(name)

#     # Get the user id from the session
#     user_id = session["user_id"]

#     with connect_db() as client:
#         # Add the thing to the DB
#         sql = "INSERT INTO things (name, price, user_id) VALUES (?, ?, ?)"
#         params = [name, price, user_id]
#         client.execute(sql, params)

#         # Go back to the home page
#         flash(f"Thing '{name}' added", "success")
#         return redirect("/things")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
# - Restricted to logged in users
#-----------------------------------------------------------
@app.get("/members/<int:id>/delete")
@admin_required
def delete_a_member(id):

    with connect_db() as client:
        # Delete the member from the DB
        sql = "DELETE FROM members WHERE id=?"
        params = [id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Member Deleted", "success")
        return redirect("/admin/members")


#-----------------------------------------------------------
    
@app.get("/members/<int:member_id>/edit")
@admin_required
def edit_member(member_id):
    with connect_db() as client:
        # Get the member details from the DB
        sql = "SELECT * FROM members WHERE id=?"
        params = [member_id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            member = result.rows[0]
            return render_template("components/member_form.jinja", member=member)

        else:
            # No, so show error
            return not_found_error()


#-----------------------------------------------------------
    
@app.put("/members/<int:member_id>/edit")
@admin_required
def update_member(member_id):
    with connect_db() as client:
        # Get data from the form
        name = request.form.get("name")
        new_password = request.form.get("password_hash")  # leave blank to keep existing
        email = request.form.get("email")
        number = request.form.get("number")
        vehicle = request.form.get("vehicle")
        admin = 1 if request.form.get("admin") == "true" else 0

        # Fetch the current member
        sql_current = "SELECT * FROM members WHERE id = ?"
        result = client.execute(sql_current, [member_id])
        if not result.rows:
            return not_found_error()

        member_data = result.rows[0]

        # Decide which password hash to use
        if new_password.strip():
            password_hash = generate_password_hash(new_password)
        else:
            password_hash = member_data["password_hash"]

        # Update the member
        sql_update = """
            UPDATE members
            SET name = ?, 
                password_hash = ?, 
                email = ?, 
                number = ?, 
                vehicle = ?, 
                admin = ?
            WHERE id = ?
        """
        params_update = [
            name,
            password_hash,
            email,
            number,
            vehicle,
            admin,
            member_id
        ]
        client.execute(sql_update, params_update)

        # Fetch the updated member
        sql_select = "SELECT * FROM members WHERE id = ?"
        result = client.execute(sql_select, [member_id])

        if result.rows:
            updated_member = result.rows[0]
            return render_template("components/member_details.jinja", member=updated_member)
        else:
            return not_found_error()

#-----------------------------------------------------------
# TRIP EDIT ROUTES
@app.get("/trips/<int:trip_id>/edit")
@admin_required
def edit_trip(trip_id):
    with connect_db() as client:
        # Get the member details from the DB
        sql = "SELECT * FROM trips WHERE id=?"
        params = [trip_id]
        result = client.execute(sql, params)

        sql_members = "SELECT id, name FROM members ORDER BY name"
        members_result = client.execute(sql_members)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            trips = result.rows[0]
            return render_template("components/admin_trip_form.jinja", trips=trips, members=members_result)

        else:
            # No, so show error
            return not_found_error()       


@app.put("/trips/<int:trip_id>/edit")
@admin_required
def update_trips(trip_id):
    with connect_db() as client:
        # ------------------ Handle form submission ------------------
        if request.form:
            # Get data from the form
            name = request.form.get("name")
            location = request.form.get("location")
            date = request.form.get("date")
            leader = request.form.get("leader")  # this will be the member ID
            grade = request.form.get("difficulty")
            summary = request.form.get("summary")

            # Update the trip in the database
            sql_update = """
                UPDATE trips
                SET name = ?, 
                    location = ?, 
                    date = ?, 
                    leader = ?, 
                    grade = ?, 
                    summary = ?
                WHERE id = ?
            """
            params_update = [name, location, date, leader, grade, summary, trip_id]
            client.execute(sql_update, params_update)

        # ------------------ Fetch trip and members for the form ------------------
        sql_trip = """
            SELECT trips.*, members.name AS leader_name
            FROM trips
            LEFT JOIN members ON trips.leader = members.id
            WHERE trips.id = ?
        """
        trip_result = client.execute(sql_trip, [trip_id])

        sql_members = "SELECT id, name FROM members ORDER BY name"
        members_result = client.execute(sql_members)

        if trip_result.rows:
            trip = trip_result.rows[0]
            members = members_result.rows
            return render_template(
                "components/admin_trip_details.jinja",
                trips=trip,
                members=members
            )
        else:
            return not_found_error()

#-----------------------------------------------------------
#trip delete route
        
@app.get("/trips/<int:trip_id>/delete")
@admin_required
def delete_a_trip(trip_id):
    with connect_db() as client:
        # Delete the trip from the DB
        sql = "DELETE FROM trips WHERE id=?"
        params = [trip_id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Trip Deleted", "success")
        return redirect("/admin/trips")



#-----------------------------------------------------------
# User login form route
#-----------------------------------------------------------
@app.get("/login")
def login_form():
    return render_template("pages/login.jinja")


#-----------------------------------------------------------
# Route for adding a user when registration form submitted
#-----------------------------------------------------------
@app.post("/add-user")
@admin_required
def add_user():
    # Get the data from the form
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    with connect_db() as client:
        # Attempt to find an existing record for that user
        sql = "SELECT * FROM users WHERE username = ?"
        params = [username]
        result = client.execute(sql, params)

        # No existing record found, so safe to add the user
        if not result.rows:
            # Sanitise the name
            name = html.escape(name)

            # Salt and hash the password
            hash = generate_password_hash(password)

            # Add the user to the users table
            sql = "INSERT INTO users (name, username, password_hash) VALUES (?, ?, ?)"
            params = [name, username, hash]
            client.execute(sql, params)

            # And let them know it was successful and they can login
            flash("Registration successful", "success")
            return redirect("/login")

        # Found an existing record, so prompt to try again
        flash("Username already exists. Try again...", "error")
        return redirect("/register")


#-----------------------------------------------------------
# Route for processing a user login
#-----------------------------------------------------------

@app.post("/login-user")
def login_member():
    # Get the login form data
    email = request.form.get("email")
    password = request.form.get("password")

    with connect_db() as client:
        # Attempt to find the member by email
        sql = "SELECT * FROM members WHERE email = ?"
        params = [email]
        result = client.execute(sql, params)

        if result.rows:
            member = result.rows[0]
            stored_hash = member["password_hash"]

            # Check the password against the stored hash
            if check_password_hash(stored_hash, password):
                # Save info in the session
                session["member_id"]   = member["id"]
                session["member_name"] = member["name"]
                session["logged_in"]   = True
                session["is_admin"] = int(member["admin"]) == 1


                flash("Login successful", "success")
                return redirect("/")

        # Either member not found, or password incorrect
        flash("Invalid credentials", "error")
        return redirect("/login")



#-----------------------------------------------------------
# Route for processing a user logout
#-----------------------------------------------------------
@app.get("/logout")
def logout():
    # Clear the details from the session
    session.pop("member_id", None)
    session.pop("member_name", None)
    session.pop("is_admin", None)
    session.pop("logged_in", None)

    # And head back to the home page
    flash("Logged out successfully", "success")
    return redirect("/")

#-----------------------------------------------------------
# admin page route
#-----------------------------------------------------------
@app.get("/admin/settings")
@admin_required
def admin_settings():
    return render_template("pages/admin_settings.jinja")
#-----------------------------------------------------------
@app.get("/admin/trips")
@app.get("/admin")
@admin_required
def search_admin_trips():
    search_text = request.args.get("q", "")  # get search term or empty string
    search_param = f"%{search_text}%"

    with connect_db() as client:
        # Past trips
        sql_past = """
        SELECT trips.*, members.name as leader_name
        FROM trips
        LEFT JOIN members ON trips.leader = members.id
        WHERE (
                  trips.name LIKE ?
                  OR trips.location LIKE ?
              )
          AND date(trips.date) < date('now')
        ORDER BY trips.date DESC
        """
        past_trips = client.execute(sql_past, [search_param, search_param]).rows

        # Future trips
        sql_future = """
        SELECT trips.*, members.name as leader_name
        FROM trips
        LEFT JOIN members ON trips.leader = members.id
        WHERE (
                  trips.name LIKE ?
                  OR trips.location LIKE ?
              )
          AND date(trips.date) >= date('now')
        ORDER BY trips.date ASC
        """
        future_trips = client.execute(sql_future, [search_param, search_param]).rows
        

        # Check if we found anything
        no_results = not (past_trips or future_trips)
        
        

        return render_template(
            "pages/admin_trips.jinja",
            past_trips=past_trips,
            future_trips=future_trips,
            search_text=search_text,
            no_results=no_results
        )


       
#-----------------------------------------------------------
@app.get("/admin/members")
@admin_required
def admin_members():
    search_text = request.args.get("q", "")  # get search term or empty string
    with connect_db() as client:
        sql = """
            SELECT *
            FROM members
            WHERE id != 5
              AND (
                  name LIKE ?
                  OR email LIKE ?
              )
            ORDER BY name ASC
        """
        search_param = f"%{search_text}%"
        params = [search_param, search_param]
        result = client.execute(sql, params)

        if result.rows:
            members = result.rows
            return render_template("pages/admin_members.jinja", members=members, search_text=search_text, no_results=False)
        else:
            # No results found — pass a flag to template or return a custom message
            return render_template("pages/admin_members.jinja", members=[], search_text=search_text, no_results=True)


       

# #-----------------------------------------------------------
@app.get("/upcoming/")
@login_required
def upcoming_trips():
    member_id = session["member_id"]
    with connect_db() as client:
        # Get all upcoming trips
        sql = """
            SELECT *
                             
            FROM trips
            
            WHERE date(trips.date) >= date('now')
            ORDER BY trips.date ASC
        """
        params = []
        upcoming_result = client.execute(sql, params)
        upcoming_trips = upcoming_result.rows

        # Get trips the current user has already joined
        joined_sql = "SELECT trip_id FROM coming WHERE user_id = ?"
        joined_params = [member_id]
        joined_result = client.execute(joined_sql, joined_params)
        joined_trip_ids = [row["trip_id"] for row in joined_result.rows]

    return render_template(
        "pages/upcoming.jinja",
        upcoming_trips=upcoming_trips,
        joined_trip_ids=joined_trip_ids
    )



#-----------------------------------------------------------
#join trip route
@app.get("/trip/<int:trip_id>")
@login_required
def get_trip_details(trip_id):
    with connect_db() as client:
        # Get trip with leader name
        sql = """
        SELECT trips.*, members.name as leader_name
        FROM trips
        LEFT JOIN members ON trips.leader = members.id
        WHERE trips.id=?
        """
        trip_result = client.execute(sql, [trip_id])
        trip = trip_result.rows[0] if trip_result.rows else None


        # Get attendees
        sql = """
        SELECT members.name, members.vehicle
        FROM coming
        JOIN members ON coming.user_id = members.id
        WHERE coming.trip_id = ?
        ORDER BY members.name ASC
        """
        attendees_result = client.execute(sql, [trip_id])
        attendees = attendees_result.rows if attendees_result.rows else []

    return render_template(
        "components/trip_details.jinja",
        trip=trip,
        attendees=attendees
    )


#-----------------------------------------------------------
#join trip route
@app.post("/join-trip/<int:trip_id>")
@login_required
def join_trip(trip_id):
    member_id = session["member_id"]
    with connect_db() as client:
        # Avoid duplicate joins
        check = client.execute("SELECT * FROM coming WHERE user_id=? AND trip_id=?", [member_id, trip_id])
        if not check.rows:
            client.execute("INSERT INTO coming (user_id, trip_id) VALUES (?, ?)", [member_id, trip_id])
    flash("You joined the trip!", "success")
    return redirect("/upcoming/")

#-----------------------------------------------------------
#leave trip route
@app.post("/unjoin-trip/<int:trip_id>")
@login_required
def unjoin_trip(trip_id):
    member_id = session["member_id"]
    with connect_db() as client:
        # Remove the user from the coming table
        client.execute(
            "DELETE FROM coming WHERE user_id = ? AND trip_id = ?",
            [member_id, trip_id]
        )
    flash("You left the trip.", "info")
    return redirect("/upcoming/")


#-----------------------------------------------------------
#add photos route
#-----------------------------------------------------------
@app.get("/trips/<int:trip_id>/add-photos")
@admin_required
def show_add_photo_form(trip_id):
    with connect_db() as client:
        result = client.execute("SELECT * FROM trips WHERE id = ?", [trip_id])
        trip = result[0] if result else None
    return render_template("components/admin_trip_photo_form.jinja", trips=trip)


@app.post("/trips/<int:trip_id>/add-photos")
@admin_required
def add_photos(trip_id):
    file = request.files.get("photo")
    credits = request.form.get("credits")

    if not file:
        return "<div style='color:red;'>No file selected</div>"

    image_data = file.read()
    image_type = file.mimetype

    with connect_db() as client:
        client.execute(
            "INSERT INTO trip_photos (trip_id, credits, image_data, image_type) VALUES (?, ?, ?, ?)",
            [trip_id, credits, image_data, image_type]
        )

        # fetch updated trip and photos
        trip_result = client.execute("SELECT * FROM trips WHERE id = ?", [trip_id])
        trip = trip_result[0] if trip_result else None

        photos = client.execute("SELECT * FROM trip_photos WHERE trip_id = ?", [trip_id])

    return render_template("components/admin_trip_details.jinja", trips=trip, photos=photos)

