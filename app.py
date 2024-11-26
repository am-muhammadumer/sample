from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Flask Configuration
app.config['SECRET_KEY'] = 'your_secret_key'  # For flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Create a Model for Contact Messages
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Contact Form Submission Route
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Validate form inputs
        if not name or not email or not message:
            flash('All fields are required!', 'danger')
            return redirect(url_for('home'))

        # Save data to the database
        new_contact = Contact(name=name, email=email, message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('home'))

# Admin Page to View Messages (Example Functionality)
@app.route('/admin/messages')
def view_messages():
    contacts = Contact.query.all()
    return render_template('admin_messages.html', contacts=contacts)



# View message route
@app.route('/admin/messages/view/<int:message_id>')
def view_message(message_id):
    contact = Contact.query.get_or_404(message_id)
    return jsonify({
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'message': contact.message
    })


# Delete message route
@app.route('/admin/messages/delete/<int:message_id>', methods=['GET','POST'])
def delete_message(message_id):
    contact = Contact.query.get_or_404(message_id)
    db.session.delete(contact)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('view_messages'))


#Initialize the Database
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
