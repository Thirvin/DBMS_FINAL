# Music Streaming API Documentation

## Overview
This document provides a comprehensive overview of the available API endpoints for the music streaming service. Each endpoint is described with its respective method, description, request parameters, and responses.

## Table of Contents
1. [Login](#1-login)
2. [Logout](#2-logout)
3. [Sign Up](#3-sign-up)
4. [Search URL](#4-search-url)
5. [Search by ID](#5-search-by-id)
6. [Play Playlist](#6-play-playlist)
7. [Create Playlist](#7-create-playlist)
8. [Add Music to Playlist](#8-add-music-to-playlist)
9. [Remove Music from Playlist](#9-remove-music-from-playlist)
10. [Test](#10-test)
11. [Get All Playlists](#11-get-all-playlists)

## 1. Login
- **Endpoint:** `/login`
- **Methods:** GET, POST
- **Description:** Allows users to log in.
- **Request:**
  - **POST Parameters:**
    - `email`: User's email address.
    - `password`: User's password.
- **Responses:**
  - On success: Redirects to the home page and flashes a success message.
  - On failure: Flashes an error message and reloads the login page.
- **Template:** `login.html`

## 2. Logout
- **Endpoint:** `/logout`
- **Methods:** GET
- **Description:** Logs out the current user.
- **Responses:** Renders the logout page.
- **Template:** `logout.html`

## 3. Sign Up
- **Endpoint:** `/sigh-up`
- **Methods:** GET, POST
- **Description:** Allows new users to register.
- **Request:**
  - **POST Parameters:**
    - `email`: User's email address.
    - `firstName`: User's first name.
    - `password1`: User's password.
    - `password2`: User's password confirmation.
- **Responses:**
  - On success: Redirects to the home page and flashes a success message.
  - On failure: Flashes an error message and reloads the sign-up page.
- **Template:** `sigh-up.html`

## 4. Search URL
- **Endpoint:** `/search_url`
- **Methods:** POST
- **Description:** Searches for a YouTube URL and retrieves audio information.
- **Request:**
  - **POST Parameters:**
    - `search_query`: YouTube URL to search.
- **Responses:**
  - On success: Returns a JSON object with audio details.
  - Example response:
    ```json
    {
      "status": "success",
      "audio_url": "audio_url",
      "id": "id",
      "thumbnail_url": "thumbnail_url",
      "artist": "artist",
      "title": "title"
    }
    ```

## 5. Search by ID
- **Endpoint:** `/search_id`
- **Methods:** POST
- **Description:** Searches for a music entry by its ID and retrieves audio information.
- **Request:**
  - **POST Parameters:**
    - `search_query`: JSON object containing the music ID.
- **Responses:**
  - On success: Returns a JSON object with audio details.
  - On failure: Returns a JSON object with an error status.
  - Example response:
    ```json
    {
      "status": "success",
      "audio_url": "audio_url",
      "title": "title"
    }
    ```

## 6. Play Playlist
- **Endpoint:** `/play/<path:index>`
- **Methods:** GET
- **Description:** Retrieves and plays a playlist by its ID.
- **Parameters:**
  - `index`: Playlist ID.
- **Responses:** Renders the play page with playlist data.
- **Template:** `play.html`

## 7. Create Playlist
- **Endpoint:** `/creat_playlist`
- **Methods:** POST
- **Description:** Creates a new playlist for the current user.
- **Request:**
  - **POST Parameters:**
    - `name`: Name of the playlist.
    - `type`: Type of the playlist.
- **Responses:**
  - On success: Returns a JSON object with success status and playlist ID.
  - On failure: Returns a JSON object with an error status.

## 8. Add Music to Playlist
- **Endpoint:** `/add_music_to_playlist`
- **Methods:** POST
- **Description:** Adds a music entry to a playlist.
- **Request:**
  - **POST Parameters:**
    - `playlist_id`: ID of the playlist.
    - `music_id`: ID of the music.
- **Responses:**
  - On success: Returns a JSON object with success status.
  - On failure: Returns a JSON object with an error status and reason.

## 9. Remove Music from Playlist
- **Endpoint:** `/remove_music_from_playlist`
- **Methods:** POST
- **Description:** Removes a music entry from a playlist.
- **Request:**
  - **POST Parameters:**
    - `music_id`: ID of the music.
    - `playlist_id`: ID of the playlist.
- **Responses:**
  - On success: Returns a JSON object with success status.
  - On failure: Returns a JSON object with an error status.

## 10. Test
- **Endpoint:** `/test`
- **Methods:** GET
- **Description:** Test endpoint for rendering a test page.
- **Responses:** Renders the test page.
- **Template:** `test.html`

## 11. Get All Playlists
- **Endpoint:** `/get_all_list`
- **Methods:** POST
- **Description:** Retrieves all playlists for the current user.
- **Responses:**
  - On success: Returns a JSON object with a list of playlists.
  - On failure: Returns a JSON object with an error status.
  - Example response:
    ```json
    {
      "datas": [
        {
          "id": "playlist_id",
          "title": "playlist_title"
        }
      ]
    }
    ```

