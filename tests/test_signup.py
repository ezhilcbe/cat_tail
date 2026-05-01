from urllib.parse import quote


def _signup_path(activity_name):
    return f"/activities/{quote(activity_name, safe='')}/signup"


def test_signup_success(client):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    response = client.post(_signup_path(activity_name), params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        _signup_path("Unknown Club"),
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    response = client.post(
        _signup_path("Chess Club"),
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
