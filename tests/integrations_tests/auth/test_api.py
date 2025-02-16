import pytest


@pytest.mark.parametrize(
    "email, password",
    [
        ("example0@mail.ru", "Test_0123456789"),
        ("example1@mail.ru", "Test_1123456789"),
        ("example2@mail.ru", "Test_2123456789"),
        ("example3@mail.ru", "Test_3123456789"),
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
