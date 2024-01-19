from datetime import date
from http import HTTPStatus

import pytest
from faker import Faker

fake = Faker()


def generate_fake_data():
    sex = fake.random.choice(["male", "female"])
    name = fake.first_name_male() if sex == "male" else fake.first_name_female()
    date_of_birth = fake.date_between_dates(
        date_start=date(1900, 1, 1), date_end=date.today()
    )
    date_of_death = fake.random.choice(
        [None, fake.date_between_dates(date_of_birth, date_end=date.today())]
    )
    return name, sex, date_of_birth, date_of_death


@pytest.fixture(scope="function")
def one_pet():
    name, sex, date_of_birth, date_of_death = generate_fake_data()
    test_data = {
        "name": name,
        "kind": "test_kind",
        "sex": sex,
        "date_of_birth": str(date_of_birth),
        "date_of_death": str(date_of_death) if date_of_death else None,
    }
    return test_data


@pytest.fixture(scope="function")
def create_one_pet(pet_repo, one_pet):
    return pet_repo.create_one(**one_pet)


@pytest.fixture(scope="function")
def create_ten_pets(pet_repo):
    list_of_pets = []
    for i in range(0, 10):
        name, sex, date_of_birth, date_of_death = generate_fake_data()
        pet = {
            "name": name,
            "kind": "test_kind",
            "sex": sex,
            "date_of_birth": str(date_of_birth),
            "date_of_death": str(date_of_death) if date_of_death else None,
        }
        pet = pet_repo.create_one(**pet)
        list_of_pets.append(pet)
    return list_of_pets


def test_get_one(create_one_pet, client, one_pet):
    response = client.get(f"/pet/{create_one_pet.id}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    for key, val in one_pet.items():
        assert data[key] == val


def test_get_one_not_exist(client):
    response = client.get("/pet/1")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_filter_age(create_ten_pets, client, pet_repo):
    assert pet_repo.all()
    first_filter_parametr = "age__gt"
    first_filter_value = 5
    second_filter_parametr = "age__lt"
    second_filter_value = 30
    response = client.get(
        f"pet/?limit={len(create_ten_pets)}&offset=0&{first_filter_parametr}={first_filter_value}&{second_filter_parametr}={second_filter_value}"
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()["result"]
    for i in data:
        assert second_filter_value > i["age"] > first_filter_value

    filtred_created_ten_pets = [
        x for x in create_ten_pets if second_filter_value > x.age > first_filter_value
    ]
    assert len(filtred_created_ten_pets) == len(data)
