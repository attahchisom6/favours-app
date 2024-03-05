#!/usr/bin/env python3
""""
test the vearer auth class
"""
from models.user import User
from Authentication_microservice.api.v1.auth.bearer_auth import BearerAuth
import jwt
import bcrypt

kwargs = {"first_name": "Okechukwu", "last_name": "Nwanna", "email": "oke@nna.com", "password": "127oke"}

u = User(**kwargs)
u.save()

b = BearerAuth()
print(b.extract_user_from_credentials(None, None))
print(b.extract_user_from_credentials("pas", None))
print(b.extract_user_from_credentials(u.email, "i5"))
print(b.extract_user_from_credentials(u.email, "127oke"))
print(u.is_valid_password("127oke"))
print(u.email)
print(u.password)
# assert u.password == bcrypt.hashpw("127oke".encode("utf-8"), bcrypt.gensalt())

jwt_encoded = jwt.encode(kwargs, key=b.load_from_env_or_file(), algorithm="HS384")
if jwt_encoded:
  print(jwt_encoded)
else:
  print("jwt encode failed")
