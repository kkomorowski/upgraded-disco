"""Tests for the Mergington High School Activities API"""

import pytest
from fastapi.testclient import TestClient


class TestActivitiesAPI:
    """Test suite for activities API endpoints"""

    def test_root_redirect(self, client: TestClient):
        """Test root endpoint redirects to static index"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        # The redirect response should serve the HTML file

    def test_get_activities(self, client: TestClient):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()

        # Check that we get a dictionary of activities
        assert isinstance(data, dict)
        assert len(data) > 0

        # Check structure of first activity
        first_activity = next(iter(data.values()))
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for field in required_fields:
            assert field in first_activity

        assert isinstance(first_activity["participants"], list)

    def test_signup_successful(self, client: TestClient):
        """Test successful signup for an activity"""
        # First get current participants
        response = client.get("/activities")
        activities = response.json()
        soccer_team = activities["Soccer Team"]
        initial_count = len(soccer_team["participants"])

        # Sign up a new student
        new_email = "test@mergington.edu"
        response = client.post(
            "/activities/Soccer%20Team/signup",
            params={"email": new_email}
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert new_email in data["message"]
        assert "Soccer Team" in data["message"]

        # Verify the participant was added
        response = client.get("/activities")
        activities = response.json()
        soccer_team = activities["Soccer Team"]
        assert len(soccer_team["participants"]) == initial_count + 1
        assert new_email in soccer_team["participants"]

    def test_signup_activity_not_found(self, client: TestClient):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/NonExistentActivity/signup",
            params={"email": "test@mergington.edu"}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_already_registered(self, client: TestClient):
        """Test signup when student is already registered"""
        # Get an existing participant
        response = client.get("/activities")
        activities = response.json()
        existing_email = activities["Soccer Team"]["participants"][0]

        # Try to sign up again
        response = client.post(
            "/activities/Soccer%20Team/signup",
            params={"email": existing_email}
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_unregister_successful(self, client: TestClient):
        """Test successful unregister from an activity"""
        # First get current participants
        response = client.get("/activities")
        activities = response.json()
        soccer_team = activities["Soccer Team"]
        initial_count = len(soccer_team["participants"])
        email_to_remove = soccer_team["participants"][0]

        # Unregister the student
        response = client.delete(
            f"/activities/Soccer%20Team/participants/{email_to_remove}"
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email_to_remove in data["message"]
        assert "Soccer Team" in data["message"]

        # Verify the participant was removed
        response = client.get("/activities")
        activities = response.json()
        soccer_team = activities["Soccer Team"]
        assert len(soccer_team["participants"]) == initial_count - 1
        assert email_to_remove not in soccer_team["participants"]

    def test_unregister_activity_not_found(self, client: TestClient):
        """Test unregister from non-existent activity"""
        response = client.delete(
            "/activities/NonExistentActivity/participants/test@mergington.edu"
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_not_registered(self, client: TestClient):
        """Test unregister when student is not registered"""
        response = client.delete(
            "/activities/Soccer%20Team/participants/nonexistent@mergington.edu"
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"]