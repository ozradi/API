# import asyncio

# from permit import Permit, UserInput
# from fastapi import FastAPI, status, HTTPException
# from fastapi.responses import JSONResponse

# app = FastAPI()

# # This line initializes the SDK and connects your python app
# # to the Permit.io PDP container you've set up in the previous step.
# permit = Permit(
#     # in production, you might need to change this url to fit your deployment
#     pdp="http://localhost:7000",
#     # your api key
#     token="eyJhbGciOiJSUzI1NiIsImtpZCI6IjRjYjFhYjYyLWVhZTctNDFmZS04NWMwLTAyZjFlNjMyN2FlZCIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NDAyNTAxNDMsImV4cCI6MTY3MTY5OTc0MywiYXVkIjoiaHR0cHM6Ly9hcGkucGVybWl0LmlvL3YxLyIsImlzcyI6Imh0dHBzOi8vYXV0aC5wZXJtaXQuaW8vIiwic3ViIjoiNzJkNGNjYWVkNTdjNDg4NzljMjU1NjMzZTAwMWNlMmQifQ.ZtSXRmdJYFxxo3i_fD2oAMoZSJLKHdkR15LarvXoC-IYNRlU-EYQnhhzGgBlglJtx0UWAeQzS9EUohzTI-G56n6ZvdvJ3nKD11MedM2TzfN9XSeeQ4ZmMQXp5RXx7Dg8wv3ZVtIT8s095VfkhUJA6yamHcthcOqXZg8bRnnAOwqpytpPlcpKe3q-1skEB0AE7Kqe3q_PevMUPDVqLzKPEAz3VeVcotnQKIcFcj0KfJ8yVDXKapBbOy6zafVaem5dfbK0guwkgw0QJG_U4vrck53s4EYP9_2dCjvT1ao4R3NJeWXmJ6umu2mxrEgLqyg99Yg7x69xhcePHGfozq9GUtx2H_cNYAHRqAkxqPQ5sWbvgVeMfd2heNJNdHDDSa0kA0odT6JwuMF1r2Y_341ja5ysmGyv0rzodYvnXjog_ATjJXssOq5o6J6FM6az1d1ZsuNQ7xilPpAgaQvlSmcv4jCVHtwIcO3aHMNPs0JvgvRJeY2ZHKUIAcmW2-xDjQ5plZ67T5zEWTdYmwpGrfgr_O78M8tXdb3jBcyLVGCf7tYNUMK0nKfbDoORoYy38YKl5eK0c6_t3XLFngTSY8xFIomnFXb6jBS7HwmYhbQgkwqFgaZot_zeOIIbaVwc9X-zeDhl8bb5kTrBoTuX_BEXvuSIswHT5Xwi9yB7ZtCZxaw",
# )

# # This user was defined by you in the previous step and
# # is already assigned with a role in the permission system.
# user = {
#     "id": "7624e4cf3b904febbb2033259300f02c",
#     "firstName": "Oz",
#     "lastName": "Radiano",
#     "email": "ozradiano@gmail.com",
# } # in a real app, you would typically decode the user id from a JWT token

# user2 = {
#     "id": "ozradi",
#     "firstName": "Oz",
#     "lastName": "Rad",
#     "email": "ozradtest@gmail.com",
# } # in a real app, you would typically decode the user id from a JWT token


# @app.get("/")
# async def check_permissions():
#     user = UserInput(user2.id, user2.first_name, user2.last_name, user2.email)
#     permit.write(permit.api.sync_user(user2.customId, user2.first_name, user2.last_name, user2.email))

#     # After we created this user in the previous step, we also synced the user's identifier
#     # to permit.io servers with permit.write(permit.api.syncUser(user)). The user identifier
#     # can be anything (email, db id, etc) but must be unique for each user. Now that the
#     # user is synced, we can use its identifier to check permissions with `permit.check()`.
#     permitted = await permit.check(user["id"], "delete", "document")
#     if not permitted:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
#             "result": f"{user.get('firstName')} {user.get('lastName')} is NOT PERMITTED to delete document!"
#         })

#     return JSONResponse(status_code=status.HTTP_200_OK, content={
#         "result": f"{user.get('firstName')} {user.get('lastName')} is PERMITTED to delete document!"
#     })
