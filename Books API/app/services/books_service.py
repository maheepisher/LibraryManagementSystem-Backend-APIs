from app.utils.db_connection import get_db_connection

def manage_books_details(method, user_role, book_id=None, BookName=None, Genre=None, Author=None,PublishDate = None, BookDescription = None, isCommunityBook = False, customerID = None, adminID = None, decision = None, requestDate = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Parameters for the stored procedure
        params = [method, user_role, book_id, BookName, Genre, Author, PublishDate, BookDescription, isCommunityBook, customerID, adminID, decision, requestDate]
        cursor.callproc('ManageBooks', params)

        # Fetch results from the stored procedure
        result = []
        for res in cursor.stored_results():
            result = res.fetchall()

        return result  # Return the array of books directly
    except Exception as e:
        print(f"Error: {e}")
        return {'Message': f'Error processing request: {str(e)}'}
    finally:
        cursor.close()
        conn.close()