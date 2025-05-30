from datetime import date, datetime
import uuid

from sqlalchemy import Column, ForeignKey, String, Integer, Date, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship



Base = declarative_base()


class BatchModel(Base):
    __tablename__ = "batches"

    oid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    shift_task_name: Mapped[str] = mapped_column(String, nullable=False)
    work_center: Mapped[str] = mapped_column(String, nullable=False)
    shift: Mapped[str] = mapped_column(String, nullable=False)
    brigade: Mapped[str] = mapped_column(String, nullable=False)

    batch_number: Mapped[int] = mapped_column(Integer, nullable=False)
    batch_date: Mapped[date] = mapped_column(Date, nullable=False)

    nomenclature: Mapped[str] = mapped_column(String, nullable=False)
    ekn_code: Mapped[str] = mapped_column(String, nullable=False)
    rc_identifier: Mapped[str] = mapped_column(String, nullable=False)

    shift_start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    shift_end_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    products: Mapped[list["ProductItemModel"]] = relationship("ProductItemModel", back_populates="batch")


class ProductItemModel(Base):
    __tablename__ = "product_items"

    oid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    batch_oid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("batches.oid"), nullable=False
    )
    batch: Mapped["BatchModel"] = relationship("BatchModel", back_populates="products")

    unique_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_aggregated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    aggregated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
