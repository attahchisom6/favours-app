#!/usr/bin/env python3
""""
test the vearer auth class
"""
from models.user import User
from Authentication_microservice.api.v1.auth.bearer_auth import BearerAuth
import jwt

kwargs = {first_name: "Okechukwu", last_name: "Nwanna", email: "oke@nna.com", password: "127oke"}

u = User(**kwargs)
u.save()

b = BearerAuth()
print(b.extract_user_from_credentials(None, None))
print(b.extract_user_from_credentials("pas", None))
print(b.extract_user_from_credentials(user.email, "i5"))
print(b.extract_user_from_credentials(user.email, "127oke"))
assert user.password == "127oke"

jwt_encoded = jwt.encode(kwargs, "SECRET_KEY", algorithms=["HS384"])
