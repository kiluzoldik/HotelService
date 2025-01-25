import pytest


@pytest.mark.parametrize(
    "email, password",
    [
        ("test1@test1.com", "test1"),
        ("test2@test2.com", "test2"),
        ("test3@test3.com", "test3"),
        ("test4@test4.com", "test4"),
    ],
)
@pytest.mark.order("last")
async def test_flow_auth(email, password, authenticated_client):
    await authenticated_client.post("/auth/logout")
    response_register_user = await authenticated_client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response_register_user.status_code == 200

    response_login_user = await authenticated_client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response_login_user.status_code == 200

    response_auth_me = await authenticated_client.get("/auth/me")
    assert response_auth_me.status_code == 200
    result = response_auth_me.json()
    assert result["email"] == email

    response_logout = await authenticated_client.post("/auth/logout")
    assert response_logout.status_code == 200

    response_auth_me_after_logout = await authenticated_client.get("/auth/me")
    assert response_auth_me_after_logout.status_code == 401
