import unittest
from flask_testing import TestCase
import unittest
from flask_testing import TestCase
from website import create_app, db
from website.models import User, Music, Playlist, InWhichPlaylist
from werkzeug.security import generate_password_hash

class TestAPI(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user
        self.user = User(email='test@example.com', password=generate_password_hash('password', method='pbkdf2:sha256'), first_name='Test', membership='Normal', limit=5)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_login(self):
        response = self.login('test@example.com', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully', response.data)

    def test_logout(self):
        self.login('test@example.com', 'password')
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'logout', response.data)

    def test_sign_up(self):
        response = self.client.post('/sigh-up', data=dict(
            email='newuser@example.com',
            firstName='New',
            password1='newpassword',
            password2='newpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully', response.data)

    def test_search_url(self):
        self.login('test@example.com', 'password')
        response = self.client.post('/search_url', data=dict(
            search_query='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('audio_url', response.json)
        self.assertEqual(response.json['status'], 'success')

    def test_search_id(self):
        self.login('test@example.com', 'password')
        response = self.client.post('/search_url', data=dict(
            search_query='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        ))

        response = self.client.post('/search_id', data=dict(
            search_query='{"id": "dQw4w9WgXcQ"}'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('audio_url', response.json)
        self.assertEqual(response.json['status'], 'success')

    def test_create_playlist(self):
        self.login('test@example.com', 'password')
        response = self.client.post('/creat_playlist', data=dict(
            name='My Playlist',
            type='Public'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['status'], 'success')

    def test_add_music_to_playlist(self):
        self.login('test@example.com', 'password')
        playlist = Playlist(P_title='My Playlist', P_type='Public', UID=self.user.id)
        db.session.add(playlist)
        db.session.commit()

        music = Music(id='dQw4w9WgXcQ', M_title='Never Gonna Give You Up', audio_url='https://example.com/audio', thumbnail_url='https://example.com/thumbnail', artist='Rick Astley', original_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        db.session.add(music)
        db.session.commit()

        response = self.client.post('/add_music_to_playlist', data=dict(
            playlist_id=playlist.P_id,
            music_id=music.id
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

    def test_remove_music_from_playlist(self):
        self.login('test@example.com', 'password')
        playlist = Playlist(P_title='My Playlist', P_type='Public', UID=self.user.id)
        db.session.add(playlist)
        db.session.commit()

        music = Music(id='dQw4w9WgXcQ', M_title='Never Gonna Give You Up', audio_url='https://example.com/audio', thumbnail_url='https://example.com/thumbnail', artist='Rick Astley', original_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        db.session.add(music)
        db.session.commit()

        in_playlist = InWhichPlaylist(M_id=music.id, P_id=playlist.P_id, UID=self.user.id)
        db.session.add(in_playlist)
        db.session.commit()

        response = self.client.post('/remove_music_from_playlist', data=dict(
            playlist_id=playlist.P_id,
            music_id=music.id
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

    def test_get_all_list(self):
        self.login('test@example.com', 'password')
        playlist = Playlist(P_title='My Playlist', P_type='Public', UID=self.user.id)
        db.session.add(playlist)
        db.session.commit()

        response = self.client.post('/get_all_list')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertTrue(len(response.json['datas']) > 0)

    def test_increase_limit(self):
        self.login('test@example.com', 'password')
        response = self.client.post('/increase_limit', data=dict(
            increase_amount=5
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        self.assertEqual(response.json['new_limit'], 10)

if __name__ == '__main__':
    unittest.main()

