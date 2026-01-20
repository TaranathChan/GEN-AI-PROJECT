import asyncio
import random
import logging

logger = logging.getLogger(__name__)

async def retry_async(
    func,
    retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 5.0,
    retry_exceptions: tuple = (Exception,),
):
    """
    Generic async retry helper with exponential backoff.

    Args:
        func: async callable to execute
        retries: number of retries
        base_delay: initial delay in seconds
        max_delay: maximum delay between retries
        retry_exceptions: exceptions to retry on
    """
    for attempt in range(1, retries + 1):
        try:
            return await func()
        except retry_exceptions as e:
            logger.warning(
                f"Retry {attempt}/{retries} failed: {str(e)}"
            )

            if attempt == retries:
                logger.error("Max retries reached. Raising error.")
                raise

            delay = min(
                base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.3),
                max_delay
            )
            await asyncio.sleep(delay)
