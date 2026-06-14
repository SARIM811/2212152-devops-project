STUDENT = {
    "reg_no": "TEST-001",
    "name": "Test Student",
    "semester": 8,
    "section": "B",
}


def test_create_student(client):
    response = client.post("/students", json=STUDENT)
    assert response.status_code == 201
    data = response.json()
    assert data["reg_no"] == STUDENT["reg_no"]
    assert data["name"] == STUDENT["name"]


def test_list_students(client):
    client.post("/students", json=STUDENT)
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["reg_no"] == STUDENT["reg_no"]


def test_get_student_by_reg_no(client):
    client.post("/students", json=STUDENT)
    response = client.get(f"/students/{STUDENT['reg_no']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == STUDENT["name"]


def test_get_student_not_found(client):
    response = client.get("/students/NONEXISTENT")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_duplicate_reg_no_returns_409(client):
    client.post("/students", json={**STUDENT, "reg_no": "TEST-DUP"})
    response = client.post("/students", json={**STUDENT, "reg_no": "TEST-DUP"})
    assert response.status_code == 409
