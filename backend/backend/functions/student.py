from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from backend import DEBUG
from backend.database import get_connection


class Student:
    def __init__(self) -> None:
        self.connection = get_connection(not DEBUG)

    def getAll(self, class_id: Optional[str], page: int = 1, per_page: int = 10) -> dict[str, bool | list[dict] | int]:
        """
        Get all students from a class with pagination

        :param class_id: Class ID
        :param page: Page number (default is 1)
        :param per_page: Number of records per page (default is 10)
        :return: a list of students
        """
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = self.connection.cursor()

        offset = (page - 1) * per_page

        query = """
            SELECT s.*, c.class_name AS current_class,
            cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', s.date_of_birth) as int) AS age
            FROM students s
            LEFT JOIN classes c ON s.current_class_id = c.class_id
            WHERE 1=1
        """

        if class_id:
            query += " AND s.current_class_id = ?"
            args = (class_id,)
        else:
            args = None

        query += f" LIMIT {per_page} OFFSET {offset}"

        if args:
            cursor.execute(query, args)
        else:
            cursor.execute(query)

        data = [dict(row) for row in cursor.fetchall()]

        cursor.close()

        return dict(success=True, data=data, count=len(data), page=page)

    def get(self, id: str) -> dict:
        """
        Get a student by ID

        :param id: Student ID
        :return: Full details of the student
        """
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = self.connection.cursor()

        cursor.execute(
            "SELECT s.*, c.class_name AS current_class, cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', s.date_of_birth) as int) AS age FROM students s LEFT JOIN classes c ON s.current_class_id = c.class_id WHERE s.student_id = ?;",
            (id,)
        )

        data = cursor.fetchone()

        if data is None:
            return dict(success=False, message="Student not found")

        cursor.execute(
            'SELECT m.marks, s.subject_name FROM marks m LEFT JOIN subjects s ON m.subject_id = s.subject_id WHERE m.student_id = ? AND m.class_id = ?;',
            (data['student_id'], data['current_class_id'])
        )

        marks = {i['subject_name']: i['marks'] for i in cursor.fetchall()}
        percentage = sum(marks.values()) / len(marks)

        cursor.execute(
            'SELECT grade FROM grades WHERE ? BETWEEN min_percentage AND max_percentage LIMIT 1',
            (percentage,)
        )
        grade = cursor.fetchone()[0]

        cursor.close()

        return dict(
            success=True,
            **dict(data),
            marks=marks,
            percentage=round(percentage, 2),
            grade=grade,
        )

    def filter(
            self,
            name: Optional[str],
            class_name: Optional[str],
            class_id: Optional[str],
            age: Optional[str],
            max_age: Optional[str],
            min_age: Optional[str],
            percentage: Optional[str],
            min_percentage: Optional[str],
            max_percentage: Optional[str],
            grade: Optional[str],
            stream: Optional[str],
            total_marks: Optional[str],
            min_marks: Optional[str],
            max_marks: Optional[str],
            total_subjects: Optional[str],
            min_subjects: Optional[str],
            max_subjects: Optional[str],
            page: int = 1,
            per_page: int = 10
    ) -> dict[str, bool | list[dict] | int]:
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = self.connection.cursor()

        offset = (page - 1) * per_page

        # COMPLETED-TODO: Make the query more faster in case of filtering data on basis of Grades.
        #                 Current Avg. Time: 25sec.

        # Old Query Avg. Time: 25sec.
        """
        SELECT DISTINCT
            s.*, c.class_name AS current_class,
            cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', s.date_of_birth) as int) AS age,
            (SELECT SUM(tm.marks) FROM marks tm WHERE s.student_id = tm.student_id) AS total_marks,
            (SELECT COUNT(*) FROM marks tm WHERE s.student_id = tm.student_id) AS total_subjects,
            ROUND(CAST ((SELECT SUM(tm.marks) FROM marks tm WHERE s.student_id = tm.student_id) as float)/CAST ((SELECT COUNT(*) FROM marks tm WHERE s.student_id = tm.student_id) as float), 2) as percentage,
            (SELECT grade FROM grades WHERE ROUND(CAST ((SELECT SUM(tm.marks) FROM marks tm WHERE s.student_id = tm.student_id) as float)/CAST ((SELECT COUNT(*) FROM marks tm WHERE s.student_id = tm.student_id) as float), 2) BETWEEN min_percentage AND max_percentage LIMIT 1) AS grade
        FROM students AS s
        LEFT JOIN classes c ON s.current_class_id = c.class_id
        LEFT JOIN marks m ON s.student_id = m.student_id
        LEFT JOIN subjects sb ON m.subject_id = sb.subject_id
        WHERE 1=1
        """

        # New Query Avg. Time: 45ms.
        query = """
            WITH student_data AS (
                SELECT
                    s.*,
                    c.class_name AS current_class,
                    cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', s.date_of_birth) as int) AS age,
                    COALESCE(SUM(m.marks), 0) AS total_marks,
                    COUNT(m.marks) AS total_subjects,
                    COALESCE(ROUND(SUM(m.marks) / NULLIF(COUNT(m.marks), 0), 2), 0) AS percentage
                FROM
                    students s,
                    classes c,
                    marks m
                WHERE
                    s.current_class_id = c.class_id AND s.student_id = m.student_id
                GROUP BY s.student_id, s.full_name, s.date_of_birth, s.current_class_id, c.class_name
            )
            SELECT
                *,
                (SELECT g.grade FROM grades g WHERE percentage BETWEEN g.min_percentage AND g.max_percentage) AS grade
            FROM student_data WHERE 1=1
        """

        params = []

        if name:
            query += " AND full_name LIKE ?"
            params.append(f"%{name}%")

        if class_name:
            query += " AND current_class LIKE ?"
            params.append(f"%{class_name}%")

        if class_id and class_id.isdigit():
            query += " AND current_class_id = ?"
            params.append(int(class_id))

        if age and age.isdigit():
            query += " AND age = ?"
            params.append(int(age))

        if max_age and max_age.isdigit():
            query += " AND age <= ?"
            params.append(int(max_age))

        if min_age and min_age.isdigit():
            query += " AND age >= ?"
            params.append(int(min_age))

        if percentage and percentage.replace(".", "", 1).isdigit():
            query += " AND percentage = ?"
            params.append(float(percentage))

        if min_percentage and min_percentage.replace(".", "", 1).isdigit():
            query += " AND percentage >= ?"
            params.append(float(min_percentage))

        if max_percentage and max_percentage.replace(".", "", 1).isdigit():
            query += " AND percentage <= ?"
            params.append(float(max_percentage))

        if grade:
            query += " AND grade = ?"
            params.append(grade)

        if stream:
            query += " AND stream LIKE ?"
            params.append(f"%{stream}%")

        if total_marks and total_marks.replace(".", "", 1).isdigit():
            query += " AND total_marks = ?"
            params.append(float(total_marks))

        if min_marks and min_marks.replace(".", "", 1).isdigit():
            query += " AND total_marks >= ?"
            params.append(float(min_marks))

        if max_marks and max_marks.replace(".", "", 1).isdigit():
            query += " AND total_marks <= ?"
            params.append(float(max_marks))

        if total_subjects and total_subjects.isdigit():
            query += " AND total_subjects = ?"
            params.append(int(total_subjects))

        if min_subjects and min_subjects.isdigit():
            query += " AND total_subjects >= ?"
            params.append(int(min_subjects))

        if max_subjects and max_subjects.isdigit():
            query += " AND total_subjects <= ?"
            params.append(int(max_subjects))

        query += f" LIMIT ? OFFSET ?"
        params.extend([per_page, offset])

        cursor.execute(query, params)
        data = [dict(row) for row in cursor.fetchall()]

        cursor.close()
        return dict(success=True, data=data, count=len(data), page=page)

    def delete(self, id: str) -> dict:
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = self.connection.cursor()

        if isinstance(id, str):
            cursor.execute("SELECT COUNT(*) AS stu_count FROM students WHERE student_id = ?;", (id,))

            if cursor.fetchone()['stu_count'] == 0:
                return dict(success=False, message="Student not found")

            cursor.execute("DELETE FROM students WHERE student_id = ?;", (id,))
            cursor.execute("DELETE FROM marks WHERE student_id = ?;", (id,))
            self.connection.commit()

            cursor.close()
            return dict(success=True, message="Student deleted successfully")
        elif isinstance(id, (list, tuple)):
            placeholders = ','.join(['?'] * len(id))
            cursor.execute(f"DELETE FROM students WHERE student_id IN ({placeholders});", id)
            deleted_count = cursor.rowcount

            cursor.execute(f"DELETE FROM marks WHERE student_id IN ({placeholders});", id)

            self.connection.commit()
            cursor.close()

            if deleted_count > 0:
                return dict(
                    success=True,
                    message=f"{deleted_count} student{'\'s' if deleted_count > 1 else ''} record{'s' if deleted_count > 1 else ''} deleted successfully"
                )
        return dict(
            success=False,
            message="Nothing to delete."
        )

    def update(self, id: str, updates: dict) -> dict:
        if isinstance(self.connection, psycopg2.extensions.connection):
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = self.connection.cursor()

        cursor.execute(
            "SELECT s.*, c.class_name AS current_class, cast(strftime('%Y.%m%d', 'now') - strftime('%Y.%m%d', s.date_of_birth) as int) AS age FROM students s LEFT JOIN classes c ON s.current_class_id = c.class_id WHERE s.student_id = ?;",
            (id,)
        )

        data = cursor.fetchone()

        if data is None:
            return dict(success=False, message="Student not found")

        cursor.execute(
            'SELECT m.marks, s.subject_name FROM marks m LEFT JOIN subjects s ON m.subject_id = s.subject_id WHERE m.student_id = ? AND m.class_id = ?;',
            (data['student_id'], data['current_class_id'])
        )

        marks = {i['subject_name']: i['marks'] for i in cursor.fetchall()}

        params = []
        isUpdated = False
        query = "UPDATE students"

        if data['full_name'] != updates['full_name']:
            isUpdated = True
            query += " SET full_name = ?"
            params.append(updates['full_name'])

        if data['date_of_birth'] != updates['date_of_birth']:
            if len(params) == 0:
                query += " SET date_of_birth = ?"
            else:
                query += ", date_of_birth = ?"
            isUpdated = True
            params.append(updates['date_of_birth'])

        if isUpdated:
            query += " WHERE student_id = ?;"
            params.append(data['student_id'])

            cursor.execute(query, params)
            self.connection.commit()

        if updates.get("marks") and isinstance(updates["marks"], dict):
            for sub, score in updates["marks"].items():
                if sub not in marks:
                    return dict(
                        success=False,
                        message="Subject is not alloted to the student, kindly contact Administration."
                    )
                else:
                    if marks[sub] != score:
                        isUpdated = True
                        cursor.execute(
                            "UPDATE marks SET marks = ? WHERE student_id = ? AND subject_id = (SELECT subject_id FROM subjects WHERE subject_name = ?) AND class_id = ?;",
                            (score, data['student_id'], sub, data['current_class_id'])
                        )
                        self.connection.commit()

        if not isUpdated:
            return dict(
                success=False,
                message="Nothing to update."
            )

        return dict(
            success=True,
            message="Student Record updated successfully."
        )