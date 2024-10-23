# Import all the models, so that Base has them before being
# imported by Alembic
from blooddonor.db.base_class import Base  # noqa
from blooddonor.models.usermodel import DonorModel, ProfileModel  # noqa
