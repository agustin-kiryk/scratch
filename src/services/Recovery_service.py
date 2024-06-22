from src.repositories.User_repository import UserRepository
from src.repositories.PasswordRecovery_repository import PasswordRecoveryRepository
from src.client.Flask_mail_client import send_verification_email
from src.utils.Api_response import ApiResponse
from src.models.PasswordRecovery_model import PasswordRecovery
import secrets
import bcrypt
from src.errorHandler.error_codes import codes
import logging

logger = logging.getLogger(__name__)


class RecoveryService:

    @staticmethod
    def request_password_recovery(email: str):
        user_repo = UserRepository()
        recovery_repo = PasswordRecoveryRepository()
        user = user_repo.find_by_email(email)
        if not user:
            return ApiResponse(message='User not found', code=codes.BAD_REQUEST).to_response()

        recovery_code = secrets.token_hex(4)
        password_recovery = PasswordRecovery(
            email=email,
            recovery_code=recovery_code,
            validate_code=False
        )
        recovery_repo.insert(password_recovery)

        try:
            send_verification_email(email, recovery_code)
            return ApiResponse(message='Recovery code sent successfully', code=codes.SUCCESS).to_response()
        except Exception as e:
            return ApiResponse(message='Failed to send recovery email', code=codes.INTERNAL_SERVER_ERROR, data=str(e)).to_response()

    @staticmethod
    def verify_recovery_code(email: str, recovery_code: str):
        recovery_repo = PasswordRecoveryRepository()
        password_recovery = recovery_repo.find_by_email(email)
        if not password_recovery or password_recovery.recovery_code != recovery_code:
            return ApiResponse(message='Invalid recovery code or email', code=codes.BAD_REQUEST).to_response()

        password_recovery.validate_code = True
        recovery_repo.update(password_recovery)
        return ApiResponse(message='Recovery code verified', code=codes.SUCCESS).to_response()

    @staticmethod
    def set_new_password(email: str, new_password: str):
        user_repo = UserRepository()
        recovery_repo = PasswordRecoveryRepository()

        user = user_repo.find_by_email(email)
        if not user:
            return ApiResponse(message='User not found', code=codes.NOT_FOUND).to_response()

        password_recovery = recovery_repo.find_by_email(email)
        if not password_recovery:
            return ApiResponse(message='Recovery session not found', code=codes.NOT_FOUND).to_response()

        # Logging to verify the state of password_recovery and its recovery_code
        logger.warning(f"password_recovery: {password_recovery}")
        logger.warning(f"password_recovery.recovery_code: {password_recovery.recovery_code}")

        if not password_recovery.validate_code:
            return ApiResponse(message='Not validate code', code=codes.CODE_NOT_VALIDATED).to_response()

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_password
        user_repo.update(user)
        recovery_repo.delete_by_email(email)
        return ApiResponse(message='Password updated successfully', code=codes.SUCCESS).to_response()
