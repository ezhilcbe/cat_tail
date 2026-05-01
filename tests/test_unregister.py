from urllib.parse import quote

from src.app import activities


def _unregister_path(activity_name):
    return f"/activities/{quote(activity_name, safe='')}/participants"


def test_unregister_success(client):
    activity_name = "Basketball Team"
    email = "alex@mergington.edu"

    response = client.delete(_unregister_path(activity_name), params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        _unregister_path("Unknown Club"),
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_student_returns_404(client):
    response = client.delete(
        _unregister_path("Chess Club"),
        params={"email": "not.enrolled@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"
