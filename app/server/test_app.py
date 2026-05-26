import unittest
from unittest.mock import patch, MagicMock
import json
from app import app  # Changed from relative import to absolute import

# filepath: app/server/test_app.py
class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client using Flask's test client
        self.app = app.test_client()
        self.app.testing = True
        # Turn off database initialization for tests
        app.config['TESTING'] = True
        
    def _create_mock_dog(self, dog_id, name, breed):
        """Helper method to create a mock dog with standard attributes"""
        dog = MagicMock(spec=['to_dict', 'id', 'name', 'breed'])
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.to_dict.return_value = {'id': dog_id, 'name': name, 'breed': breed}
        return dog
        
    def _setup_query_mock(self, mock_query, dogs):
        """Helper method to configure the query mock"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.count.return_value = len(dogs)
        mock_query_instance.offset.return_value = mock_query_instance
        mock_query_instance.limit.return_value = mock_query_instance
        mock_query_instance.all.return_value = dogs
        return mock_query_instance

    @patch('app.db.session.query')
    def test_get_dogs_success(self, mock_query):
        """Test successful retrieval of multiple dogs"""
        # Arrange
        dog1 = self._create_mock_dog(1, "Buddy", "Labrador")
        dog2 = self._create_mock_dog(2, "Max", "German Shepherd")
        mock_dogs = [dog1, dog2]
        
        self._setup_query_mock(mock_query, mock_dogs)
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data['dogs']), 2)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['total'], 2)
        
        # Verify first dog
        self.assertEqual(data['dogs'][0]['id'], 1)
        self.assertEqual(data['dogs'][0]['name'], "Buddy")
        self.assertEqual(data['dogs'][0]['breed'], "Labrador")
        
        # Verify second dog
        self.assertEqual(data['dogs'][1]['id'], 2)
        self.assertEqual(data['dogs'][1]['name'], "Max")
        self.assertEqual(data['dogs'][1]['breed'], "German Shepherd")
        
        # Verify query was called
        mock_query.assert_called_once()
        
    @patch('app.db.session.query')
    def test_get_dogs_empty(self, mock_query):
        """Test retrieval when no dogs are available"""
        # Arrange
        self._setup_query_mock(mock_query, [])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['dogs'], [])
        self.assertEqual(data['total'], 0)
        
    @patch('app.db.session.query')
    def test_get_dogs_structure(self, mock_query):
        """Test the response structure for a single dog"""
        # Arrange
        dog = self._create_mock_dog(1, "Buddy", "Labrador")
        self._setup_query_mock(mock_query, [dog])
        
        # Act
        response = self.app.get('/api/dogs')
        
        # Assert
        data = json.loads(response.data)
        self.assertIn('dogs', data)
        self.assertIn('page', data)
        self.assertIn('total', data)
        self.assertIn('total_pages', data)
        self.assertTrue(isinstance(data['dogs'], list))
        self.assertEqual(len(data['dogs']), 1)
        self.assertEqual(set(data['dogs'][0].keys()), {'id', 'name', 'breed'})


    def _create_mock_dog_full(self, dog_id, name, breed, age, description, gender, status):
        """Helper to create a mock dog with full detail attributes"""
        from unittest.mock import PropertyMock
        dog = MagicMock()
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.age = age
        dog.description = description
        dog.gender = gender
        dog.status.name = status
        return dog

    def _setup_name_query_mock(self, mock_query, dog):
        """Helper to configure the query mock for get_dog_by_name (uses .first())"""
        mock_instance = MagicMock()
        mock_query.return_value = mock_instance
        mock_instance.join.return_value = mock_instance
        mock_instance.filter.return_value = mock_instance
        mock_instance.first.return_value = dog
        return mock_instance

    @patch('app.db.session.query')
    def test_get_dog_by_name_success(self, mock_query):
        """Test successful retrieval of a dog by name"""
        mock_dog = self._create_mock_dog_full(1, "Buddy", "Labrador", 3, "Friendly dog", "Male", "AVAILABLE")
        self._setup_name_query_mock(mock_query, mock_dog)

        response = self.app.get('/api/dogs/name/Buddy')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], "Buddy")
        self.assertEqual(data['breed'], "Labrador")
        self.assertEqual(data['age'], 3)
        self.assertEqual(data['gender'], "Male")
        self.assertEqual(data['status'], "AVAILABLE")

    @patch('app.db.session.query')
    def test_get_dog_by_name_not_found(self, mock_query):
        """Test 404 response when dog name does not exist"""
        self._setup_name_query_mock(mock_query, None)

        response = self.app.get('/api/dogs/name/Unknown')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_dog_by_name_too_long(self):
        """Test 400 response when name exceeds 100 characters"""
        long_name = 'A' * 101
        response = self.app.get(f'/api/dogs/name/{long_name}')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    @patch('app.db.session.query')
    def test_get_dog_by_name_case_insensitive(self, mock_query):
        """Test that name lookup is case-insensitive"""
        mock_dog = self._create_mock_dog_full(1, "Buddy", "Labrador", 3, "Friendly dog", "Male", "AVAILABLE")
        self._setup_name_query_mock(mock_query, mock_dog)

        response = self.app.get('/api/dogs/name/buddy')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], "Buddy")


if __name__ == '__main__':
    unittest.main()