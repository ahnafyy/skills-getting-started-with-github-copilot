from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirects_to_static_index():
    response = client.get("/", allow_redirects=False)
    assert response.status_code == 307 or response.status_code == 302
    assert response.headers["location"].endswith("/static/index.html")

def test_get_activities_returns_all_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Check that the email is now in the participants list
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"