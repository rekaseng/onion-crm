from functools import wraps
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Any, Callable


def handle_db_errors(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)

        except IntegrityError as e:
            # Handle specific database errors
            if "foreign key constraint" in str(e.orig):
                return {
                    "error_message": "Foreign key constraint failed",
                    "success": False,
                    "error_code": status.HTTP_409_CONFLICT,
                    "result": []
                }
            return {
                "error_message": str(e),
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": []
            }
        except HTTPException as e:
            return {
                "error_message": e.detail,
                "success": False,
                "error_code": e.status_code,
                "result": []
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "result": []
            }

    return wrapper