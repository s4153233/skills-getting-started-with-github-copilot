import pytest

class TestActivityEndpoints:
    """Integration tests for activity endpoints"""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test fetching all activities returns expected list"""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        for activity in expected_activities:
            assert activity in activities
    
    def test_activity_structure_contains_required_fields(self, client):
        """Test that each activity has all required fields"""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Activity {activity_name} missing {field}"

class TestSignup:
    """Tests for signup functionality"""
    
    def test_signup_new_student_succeeds(self, client, sample_email, sample_activity):
        """Test that a new student can successfully sign up for an activity"""
        # Arrange
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[sample_activity]["participants"]
        initial_count = len(initial_participants)
        
        # Act
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert sample_email in response.json()["message"]
        
        # Verify participant was added
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[sample_activity]["participants"]
        assert len(updated_participants) == initial_count + 1
        assert sample_email in updated_participants
    
    def test_signup_duplicate_student_is_rejected(self, client, sample_email, sample_activity):
        """Test that a student cannot sign up twice for the same activity"""
        # Arrange
        client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )
        
        # Act
        duplicate_response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert
        assert duplicate_response.status_code == 400
        assert "already signed up" in duplicate_response.json()["detail"]
    
    def test_signup_to_nonexistent_activity_fails(self, client, sample_email):
        """Test that signup for a non-existent activity returns 404"""
        # Arrange
        nonexistent_activity = "Fake Club That Doesnt Exist"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

class TestUnregister:
    """Tests for participant removal functionality"""
    
    def test_unregister_removes_participant_successfully(self, client, sample_email, sample_activity):
        """Test that a participant can be successfully removed from an activity"""
        # Arrange
        client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )
        pre_unregister = client.get("/activities").json()[sample_activity]["participants"]
        initial_count = len(pre_unregister)
        
        # Act
        response = client.delete(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert sample_email in response.json()["message"]
        
        # Verify participant was removed
        post_unregister = client.get("/activities").json()[sample_activity]["participants"]
        assert len(post_unregister) == initial_count - 1
        assert sample_email not in post_unregister
    
    def test_unregister_nonparticipant_fails(self, client, sample_email, sample_activity):
        """Test that unregistering a non-participant returns error"""
        # Arrange
        non_participant_email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{sample_activity}/unregister",
            params={"email": non_participant_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client, sample_email):
        """Test that unregister for non-existent activity returns 404"""
        # Arrange
        nonexistent_activity = "Fake Club"
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": sample_email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
