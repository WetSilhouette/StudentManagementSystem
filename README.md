# Student Management System

A desktop application built with PyQt6 for managing student records in a school database.

## Features

- **Add Students**: Insert new student records with name, course, and mobile number
- **Edit Students**: Update existing student information
- **Delete Students**: Remove student records from the database
- **Search Students**: Find students by name
- **Interactive Table**: View all student records in a sortable table
- **User-Friendly Interface**: Menu bar, toolbar, and status bar for easy navigation

## Requirements

- Python 3.x
- PyQt6
- SQLite3 (included with Python)

### Main Features

#### Adding a Student
- Click **File → Add Student** or use the toolbar button
- Enter the student's name, select a course, and provide a mobile number
- Click **OK** to save

#### Editing a Student
- Click on a student record in the table
- Click the **Edit Record** button in the status bar
- Modify the information and click **OK**

#### Deleting a Student
- Click on a student record in the table
- Click the **Delete Record** button in the status bar
- Confirm the deletion

#### Searching for a Student
- Click **Edit → Search Student** or use the toolbar button
- Enter the student's name
- Click **Search** to highlight matching records

## Available Courses

- Math
- Physics
- Chemistry
- Biology
- Computer Science
- English
- History
- Astronomy

## Project Structure

```
StudentManagementSystem/
├── main.py          # Main application file
├── database.db      # SQLite database (created at runtime)
├── icons/           # Icon files for toolbar (optional)
│   ├── add.png
│   └── search.png
└── README.md        # This file
```

## Database Schema

The application uses a SQLite database with the following schema:

| Column | Type    | Description                    |
|--------|---------|--------------------------------|
| id     | INTEGER | Primary key (auto-increment)   |
| name   | TEXT    | Student's name                 |
| course | TEXT    | Enrolled course                |
| mobile | TEXT    | Contact phone number           |

