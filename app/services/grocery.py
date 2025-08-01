from database import insert_booking

def handle_grocery(command: str):
    insert_booking("grocery", command)
    return {"message": "Grocery slot reserved", "details": command}
