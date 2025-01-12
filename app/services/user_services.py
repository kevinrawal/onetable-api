
async def get_user_from_db(user_id: int) -> dict:
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "2a4fD@example.com",
        "role": "admin",
        "status": "active",
        "password": "$2b$12$DU/OQ2htBvEa5BpugTE01OQMoVC/evOlnS00mcTB2fCdjIra2YIoO",
    }
