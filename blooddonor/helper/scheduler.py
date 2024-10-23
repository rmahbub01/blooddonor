import datetime
import logging

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession as Session

from blooddonor.models.usermodel import DonorModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def update_donor_availability(db: Session):
    """
    Update 'is_available' to True for donors who donated more than 3 months ago and are not already available.
    """
    try:
        three_months_ago = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
            days=90
        )

        # Perform a bulk update using a single query for efficiency
        result = await db.execute(
            update(DonorModel)
            .where(DonorModel.donated_on < three_months_ago)
            .where(
                DonorModel.is_available is False
            )  # Only update if is_available is False
            .values(is_available=True)
        )

        # Commit the transaction to persist the changes
        await db.commit()

        # Log the number of rows updated
        logger.info(f"Donor availability updated for {result.rowcount} donors.")

    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating donor availability: {str(e)}")
        raise
    finally:
        await db.close()
