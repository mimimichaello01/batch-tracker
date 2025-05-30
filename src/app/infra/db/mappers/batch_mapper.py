import uuid
from app.infra.db.models.models import BatchModel
from app.domain.entities.batch import BatchEntity
from app.infra.schemas.batch import BatchCreateSchema


def batch_orm_to_entity(batch: BatchModel) -> BatchEntity:
    """Конвертирует SQLAlchemy модель в доменную сущность."""
    return BatchEntity(
        oid=str(batch.oid),
        is_closed=batch.is_closed,
        closed_at=batch.closed_at,
        shift_task_name=batch.shift_task_name,
        work_center=batch.work_center,
        shift=batch.shift,
        brigade=batch.brigade,
        batch_number=batch.batch_number,
        batch_date=batch.batch_date,
        nomenclature=batch.nomenclature,
        ekn_code=batch.ekn_code,
        rc_identifier=batch.rc_identifier,
        shift_start_datetime=batch.shift_start_datetime,
        shift_end_datetime=batch.shift_end_datetime,
    )


def batch_entity_to_orm(batch: BatchEntity) -> BatchModel:
    """Конвертирует доменную сущность в SQLAlchemy модель."""
    return BatchModel(
        oid=uuid.UUID(batch.oid),
        is_closed=batch.is_closed,
        shift_task_name=batch.shift_task_name,
        work_center=batch.work_center,
        shift=batch.shift,
        brigade=batch.brigade,
        batch_number=batch.batch_number,
        batch_date=batch.batch_date,
        nomenclature=batch.nomenclature,
        ekn_code=batch.ekn_code,
        rc_identifier=batch.rc_identifier,
        shift_start_datetime=batch.shift_start_datetime,
        shift_end_datetime=batch.shift_end_datetime,
    )


def batch_create_schema_to_entity(schema: BatchCreateSchema) -> BatchEntity:
    return BatchEntity(
        is_closed=schema.is_closed,
        shift_task_name=schema.shift_task_name,
        work_center=schema.work_center,
        shift=schema.shift,
        brigade=schema.brigade,
        batch_number=schema.batch_number,
        batch_date=schema.batch_date,
        nomenclature=schema.nomenclature,
        ekn_code=schema.ekn_code,
        rc_identifier=schema.rc_identifier,
        shift_start_datetime=schema.shift_start_datetime,
        shift_end_datetime=schema.shift_end_datetime,
    )
