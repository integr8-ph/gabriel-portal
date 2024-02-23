from fastapi import Depends
from src.auth.dependencies import get_current_active_superuser


SuperUserDep = Depends(get_current_active_superuser)
