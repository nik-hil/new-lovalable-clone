import pymysql
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self):
        self.host = 'mysql'  # Docker service name
        self.user = 'root'  # Use root for now
        self.password = 'rootpassword'
        self.database = 'lovable_db'
        self.port = 3306
        
    def get_connection(self):
        """Create database connection"""
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    def create_website(self, prompt: str, files_generated: List[str]) -> Optional[int]:
        """Create a new website record and return website_id"""
        connection = self.get_connection()
        if not connection:
            return None
            
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO websites (prompt, files_generated)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (prompt, json.dumps(files_generated)))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating website: {e}")
            return None
        finally:
            connection.close()
    
    def add_prompt_history(self, website_id: int, prompt_text: str, prompt_type: str = 'initial'):
        """Add prompt to history"""
        connection = self.get_connection()
        if not connection:
            return False
            
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO prompt_history (website_id, prompt_text, prompt_type)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (website_id, prompt_text, prompt_type))
                connection.commit()
                return True
        except Exception as e:
            print(f"Error adding prompt history: {e}")
            return False
        finally:
            connection.close()
    
    def get_latest_website(self) -> Optional[Dict]:
        """Get the most recent website with its prompt history"""
        connection = self.get_connection()
        if not connection:
            return None
            
        try:
            with connection.cursor() as cursor:
                # Get latest website
                sql = """
                SELECT id, prompt, files_generated, created_at
                FROM websites 
                ORDER BY created_at DESC 
                LIMIT 1
                """
                cursor.execute(sql)
                website = cursor.fetchone()
                
                if website:
                    # Get prompt history for this website
                    sql = """
                    SELECT prompt_text, prompt_type, created_at
                    FROM prompt_history
                    WHERE website_id = %s
                    ORDER BY created_at ASC
                    """
                    cursor.execute(sql, (website['id'],))
                    history = cursor.fetchall()
                    
                    website['history'] = history
                    website['files_generated'] = json.loads(website['files_generated'])
                    
                return website
        except Exception as e:
            print(f"Error getting latest website: {e}")
            return None
        finally:
            connection.close()
    
    def get_all_prompt_history(self) -> List[Dict]:
        """Get all prompt history ordered by creation time"""
        connection = self.get_connection()
        if not connection:
            return []
            
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT ph.prompt_text, ph.prompt_type, ph.created_at,
                       w.files_generated, w.id as website_id
                FROM prompt_history ph
                JOIN websites w ON ph.website_id = w.id
                ORDER BY ph.created_at DESC
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                
                for result in results:
                    result['files_generated'] = json.loads(result['files_generated'])
                    
                return results
        except Exception as e:
            print(f"Error getting prompt history: {e}")
            return []
        finally:
            connection.close()
    
    def update_website_files(self, website_id: int, files_generated: List[str]):
        """Update files for an existing website"""
        connection = self.get_connection()
        if not connection:
            return False
            
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE websites 
                SET files_generated = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """
                cursor.execute(sql, (json.dumps(files_generated), website_id))
                connection.commit()
                return True
        except Exception as e:
            print(f"Error updating website files: {e}")
            return False
        finally:
            connection.close()
