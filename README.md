# Music Streaming Website Application

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation Guide](#installation-guide)
6. [Usage](#usage)
7. [API Reference](#api-reference)
8. [Data Models](#data-models)
9. [Security Considerations](#security-considerations)
10. [Performance Optimization](#performance-optimization)

## Introduction

This is a music streaming website application developed using the Flask framework. Users can register accounts, create personal playlists, search for and play music from YouTube. The application aims to provide a simple yet feature-rich music playback platform.

## Features

- User authentication system (register, login, logout)
- YouTube music search and playback
- Personal playlist management
- Music addition and removal functionality
- User music quantity limit management

## Tech Stack

- Backend: Python 3.x, Flask
- Database: SQLite (via SQLAlchemy ORM)
- Frontend: HTML, JavaScript (assumed, not shown in provided code)
- External Libraries: yt-dlp (for YouTube audio extraction)
- Authentication: Flask-Login

## Project Structure
project_root  
│  
├── website  
│   ├── init.py     				# App initialization and configuration  
│   ├── auth.py         			# Authentication-related routes and functions  
│   ├── models.py       			# Database model definitions  
│   ├── views.py        			# Main view routes  
│   ├── templates/      			# HTML templates  
│   └── static/         			# CSS templates 
│ 	 
├── main.py             			# Application entry point  
└── instances/database.db           # SQLite database file (auto-generated)  
## Installation Guide

1. Clone the repository:
git clone https://github.com/Thirvin/DBMS_FINAL.git
cd DBMS_FINAL
2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
3. Install dependencies:
## Usage

1. Run the application:
python main.py
2. Access `http://localhost:5000` in your browser

3. Register a new account or log in with an existing one

4. Use the search function to find music, create playlists, and enjoy the music!

## API Reference

### Authentication

- POST `/login`: User login
- GET `/logout`: User logout
- POST `/sigh-up`: User registration

### Music

- POST `/search_url`: Search music by YouTube URL
- POST `/search_id`: Search music by music ID
- GET `/play/<path:index>`: Play specific music

### Playlist

- POST `/creat_playlist`: Create a new playlist
- POST `/add_music_to_playlist`: Add music to a playlist
- POST `/remove_music_from_playlist`: Remove music from a playlist
- POST `/get_all_list`: Get all playlists of a user
- POST `/remove_playlist`: Delete a playlist

### User Management

- POST `/increase_limit`: Increase user's music limit

## Data Models

### User
- id: Integer, primary key
- email: String, unique
- password: String (stored encrypted)
- first_name: String
- last_name: String
- membership: String
- limit: Integer

### Music
- id: String, primary key
- M_title: String
- audio_url: String
- thumbnail_url: String
- artist: String
- original_url: String

### Playlist
- P_id: Integer, primary key
- P_type: String
- P_title: String
- P_size: Integer
- is_private: Boolean
- UID: Integer, foreign key (User)

### InWhichPlaylist
- M_id: Integer, foreign key (Music)
- P_id: Integer, foreign key (Playlist)
- UID: Integer, foreign key (User)

## Security Considerations

- Use of Werkzeug's generate_password_hash and check_password_hash functions for password encryption and verification
- Utilization of Flask-Login for managing user sessions, ensuring secure authentication
- User authentication for sensitive operations (e.g., adding/removing music)

## Performance Optimization

- Use of SQLAlchemy ORM for efficient database queries
- Implementation of music URL caching to reduce requests to YouTube

