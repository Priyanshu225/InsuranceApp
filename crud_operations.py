import psycopg2
from psycopg2 import Error
from policyholder import Policyholder
from policy import Policy
from claim import Claim
from typing import Optional
from psycopg2.extras import DictCursor

# Database connection parameters
db_params = {
    'host': 'localhost',
    'database': 'insurance_app_db',
    'user': 'postgres',
    'password': 'priyanshu'
}

# Function to establish a connection
def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(**db_params)
        print("Connection to PostgreSQL successful")
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    return connection

# Policyholder CRUD functions
def create_policyholder(policyholder_data: dict) -> Policyholder:
    sql = """
    INSERT INTO policyholders (policyholder_id, name, address, contact_info)
    VALUES (%(policyholder_id)s, %(name)s, %(address)s, %(contact_info)s)
    RETURNING policyholder_id, name, address, contact_info;
    """
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, policyholder_data)
            connection.commit()
            created_policyholder = cursor.fetchone()
            return Policyholder(**policyholder_data)
    except psycopg2.Error as e:
        print(f"Error creating policyholder: {e}")
    finally:
        if connection:
            connection.close()

def read_policyholder(policyholder_id: int) -> Optional[Policyholder]:
    sql = "SELECT * FROM policyholders WHERE policyholder_id = %s;"
    connection = create_connection()
    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql, (policyholder_id,))
            policyholder_data = cursor.fetchone()
            if policyholder_data:
                # Convert DictCursor result to regular dictionary
                policyholder_dict = dict(policyholder_data)
                return Policyholder(**policyholder_dict)
            return None
    except psycopg2.Error as e:
        print(f"Error reading policyholder: {e}")
    finally:
        if connection:
            connection.close()

def update_policyholder(policyholder_id: int, data: dict) -> Optional[Policyholder]:
    sql = """
        UPDATE policyholders
        SET name = %(name)s, address = %(address)s, contact_info = %(contact_info)s
        WHERE policyholder_id = %(policyholder_id)s;
    """
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            update_data = {
                'policyholder_id': policyholder_id,
                'name': data.get('name'),
                'address': data.get('address'),
                'contact_info': data.get('contact_info')
            }
            cursor.execute(sql, update_data)
            connection.commit()
            return read_policyholder(policyholder_id)
    except psycopg2.Error as e:
        print(f"Error updating policyholder: {e}")
    finally:
        if connection:
            connection.close()
    return None

def delete_policyholder(policyholder_id: int) -> bool:
    sql = "DELETE FROM policyholders WHERE policyholder_id = %s;"
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (policyholder_id,))
            connection.commit()
            return cursor.rowcount > 0
    except psycopg2.Error as e:
        print(f"Error deleting policyholder: {e}")
        return False
    finally:
        if connection:
            connection.close()

# Policy CRUD functions
def create_policy(policy_data: dict) -> Policy:
    sql = """
        INSERT INTO policies (policy_id, policyholder_id, policy_type, start_date, end_date, premium_amount)
        VALUES (%(policy_id)s, %(policyholder_id)s, %(policy_type)s, %(start_date)s, %(end_date)s, %(premium_amount)s)
        RETURNING *
    """
    connection = create_connection()
    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql, policy_data)
            connection.commit()
            created_policy = cursor.fetchone()
            if created_policy:
                return Policy(**dict(created_policy))
            else:
                raise Exception('Failed to create policy')
    except psycopg2.Error as e:
        print(f"Error creating policy: {e}")
    finally:
        if connection:
            connection.close()

def read_policy(policy_id: int) -> Policy:
    sql = "SELECT * FROM policies WHERE policy_id = %s;"
    connection = create_connection()
    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql, (policy_id,))
            policy_data = cursor.fetchone()
            if policy_data:
                return Policy(**dict(policy_data))
            return None
    except psycopg2.Error as e:
        print(f"Error reading policy: {e}")
    finally:
        if connection:
            connection.close()

def update_policy(policy_id: int, update_data: dict) -> Policy:
    sql = """
    UPDATE policies
    SET policyholder_id = %(policyholder_id)s, policy_type = %(policy_type)s,
        start_date = %(start_date)s, end_date = %(end_date)s, premium_amount = %(premium_amount)s
    WHERE policy_id = %(policy_id)s
    RETURNING *
    """
    connection = create_connection()
    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            update_data['policy_id'] = policy_id
            cursor.execute(sql, update_data)
            connection.commit()
            updated_policy = cursor.fetchone()
            if updated_policy:
                return Policy(**dict(updated_policy))
            return None
    except psycopg2.Error as e:
        print(f"Error updating policy: {e}")
    finally:
        if connection:
            connection.close()

def delete_policy(policy_id: int) -> bool:
    sql = "DELETE FROM policies WHERE policy_id = %s;"
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (policy_id,))
            connection.commit()
            return cursor.rowcount > 0
    except psycopg2.Error as e:
        print(f"Error deleting policy: {e}")
        return False
    finally:
        if connection:
            connection.close()

# Claim CRUD functions
def create_claim(claim_data: dict) -> Optional[Claim]:
    insert_claim_sql = """
    INSERT INTO claims (claim_id, policy_id, claim_date, claim_amount, status)
    VALUES (%(claim_id)s, %(policy_id)s, %(claim_date)s, %(claim_amount)s, %(status)s)
    RETURNING claim_id, policy_id, claim_date, claim_amount, status;
    """
    
    update_policy_sql = """
    UPDATE policies
    SET premium_amount = premium_amount - %s
    WHERE policy_id = %s
    RETURNING policy_id, premium_amount;
    """

    connection = create_connection()
    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            # Validate claim amount against policy premium amount
            policy_id = claim_data['policy_id']
            claim_amount = claim_data['claim_amount']
            
            cursor.execute("SELECT premium_amount FROM policies WHERE policy_id = %s;", (policy_id,))
            policy_data = cursor.fetchone()
            if policy_data and policy_data['premium_amount'] < claim_amount:
                raise ValueError('Claim amount cannot exceed policy premium amount')
            
            # Insert claim
            cursor.execute(insert_claim_sql, claim_data)
            created_claim = cursor.fetchone()
            
            # Commit the transaction for the claim insertion
            connection.commit()
            
            if claim_data['status'] == 'Approved':
                # Update policy if status is Approved
                cursor.execute(update_policy_sql, (claim_amount, policy_id))
                updated_policy = cursor.fetchone()
                
                # Commit the transaction for the policy update
                connection.commit()

                if not updated_policy:
                    raise Exception('Failed to update policy')
            
            return Claim(**dict(created_claim))
    except psycopg2.Error as e:
        print(f"Error creating claim or updating policy: {e}")
    except ValueError as ve:
        print(f"Validation error: {ve}")
    finally:
        if connection:
            connection.close()
    return None

def read_claim(claim_id: int) -> Optional[Claim]:
    sql = """
    SELECT claim_id, policy_id, claim_date, claim_amount, status
    FROM claims
    WHERE claim_id = %s;
    """

    connection = create_connection()
    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(sql, (claim_id,))
            claim_data = cursor.fetchone()
            if claim_data:
                return Claim(**claim_data)
            return None
    except psycopg2.Error as e:
        print(f"Error reading claim: {e}")
    finally:
        if connection:
            connection.close()
    return None

def update_claim(claim_id: int, update_data: dict) -> Optional[Claim]:
    connection = create_connection()
    try:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            # Fetch current claim details
            cursor.execute("SELECT * FROM claims WHERE claim_id = %s;", (claim_id,))
            current_claim = cursor.fetchone()

            if not current_claim:
                return None

            # Fetch the current premium amount from the policies table
            cursor.execute("SELECT premium_amount FROM policies WHERE policy_id = %s;", (update_data['policy_id'],))
            policy = cursor.fetchone()

            if not policy:
                return None

            premium_amount = policy['premium_amount']

            # Update the claims table
            update_sql = """
            UPDATE claims
            SET policy_id = %(policy_id)s, claim_date = %(claim_date)s,
                claim_amount = %(claim_amount)s, status = %(status)s
            WHERE claim_id = %(claim_id)s
            RETURNING claim_id, policy_id, claim_date, claim_amount, status;
            """
            cursor.execute(update_sql, {**update_data, 'claim_id': claim_id})
            connection.commit()

            updated_claim = cursor.fetchone()

            # Check if the claim status is 'Approved' and the claim amount is less than the premium amount
            if updated_claim['status'] == 'Approved':
                if updated_claim['claim_amount'] <= premium_amount:
                    # Update the policies table to subtract the claim amount from the premium amount
                    cursor.execute(
                        "UPDATE policies SET premium_amount = premium_amount - %s WHERE policy_id = %s;",
                        (updated_claim['claim_amount'], updated_claim['policy_id'])
                    )
                    connection.commit()
                else:
                    # If the claim amount is greater than the premium amount, set status to 'Rejected'
                    cursor.execute(
                        "UPDATE claims SET status = 'Rejected' WHERE claim_id = %s;",
                        (claim_id,)
                    )
                    connection.commit()
                    updated_claim['status'] = 'Rejected'

            return Claim(**dict(updated_claim))
    except psycopg2.Error as e:
        print(f"Error updating claim: {e}")
    finally:
        if connection:
            connection.close()
    return None

def delete_claim(claim_id: int) -> bool:
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Check if the claim exists
            cursor.execute("SELECT * FROM claims WHERE claim_id = %s;", (claim_id,))
            claim = cursor.fetchone()

            if not claim:
                return False

            # Delete the claim
            delete_sql = "DELETE FROM claims WHERE claim_id = %s;"
            cursor.execute(delete_sql, (claim_id,))
            connection.commit()

            return cursor.rowcount > 0
    except psycopg2.Error as e:
        print(f"Error deleting claim: {e}")
        return False
    finally:
        if connection:
            connection.close()

