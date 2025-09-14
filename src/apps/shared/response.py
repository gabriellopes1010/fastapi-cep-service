"""
Responsibility module for custom response
Used only in facades and services layers for business logic control
"""
from typing import Any, Dict, Optional

class CustomResponse:
    """
    Class Custom Response for facades and services layers
    Used to standardize business logic responses before reaching resources
    """

    @staticmethod
    def success(message: Optional[str] = None, data: Any = None) -> Dict[str, Any]:
        """
        Method responsible for success responses in business logic

        Args:
            message: Success message
            data: Response data

        Returns:
            Dictionary with success response structure
        """
        return {
            "status": "success",
            "message": message,
            "data": data
        }

    @staticmethod
    def failure(message: Optional[str] = None, data: Any = None) -> Dict[str, Any]:
        """
        Method responsible for failure responses in business logic

        Args:
            message: Error message
            data: Additional error data

        Returns:
            Dictionary with failure response structure
        """
        return {
            "status": "failure",
            "message": message,
            "data": data
        }
