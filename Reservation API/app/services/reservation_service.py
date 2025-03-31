from app.utils.db_connection import get_db_connection
from app.utils.db_connection import get_db_connection

def manage_reservation_details(operation, user_role, reservationID=None, bookID=None, customerID=None, decision = None, ApproverID = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        params = [operation, user_role, reservationID, bookID, customerID, decision, ApproverID]
        cursor.callproc('ManageReservations', params)
        result = []
        for res in cursor.stored_results():
            result = res.fetchall()
        return result  # Return the entire list, empty or not
    except Exception as e:
        print(f"Error: {e}")
        return {'Message': f'Error processing request: {str(e)}'}
    finally:
        cursor.close()
        conn.close()
