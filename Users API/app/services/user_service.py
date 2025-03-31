from app.utils.db_connection import get_db_connection

def manage_user_details(method, user_role, user_id=None, name=None, dob=None, address=None, email=None, phone_no=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        params = [method, user_role, user_id, name, dob, address, email, phone_no]
        cursor.callproc('ManageUserDetails', params)

        result = []
        for res in cursor.stored_results():
            result = res.fetchall()

        return result
    except Exception as e:
        print(f"Error: {e}")
        return {'Message': 'Error processing request.'}
    finally:
        cursor.close()
        conn.close()
