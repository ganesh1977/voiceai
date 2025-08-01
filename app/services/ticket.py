from database import insert_booking

def handle_ticket(command: str):
    insert_booking("ticket", command)
    return {"message": "Ticket booked", "details": command}
