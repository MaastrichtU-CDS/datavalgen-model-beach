from typing import Annotated, Literal, Union
from pydantic import BaseModel
from pydantic import Field


class DataModel(BaseModel):
    # any de-identified ID
    patient_identifier: str = Field(
        ...,
        description="De-identified (research) ID (must not be a real / directly identifiable ID)",
    )

    # TODO: We are not accepting NAs for now, but should we? Perhaps agree on a string like "NA"?
    # TNM staging
    # T stage
    patient_t_stage: Literal["Tx", "T1a", "T1b", "T1c", "T2a", "T2b", "T3", "T4"] = (
        Field(..., description="T stage")
    )
    # N stage
    patient_n_stage: Literal["Nx", "N0", "N1", "N2", "N3"] = Field(
        ..., description="N stage"
    )
    # M stage
    patient_m_stage: Literal["Mx", "M0", "M1a", "M1b", "M1c"] = Field(
        ..., description="M stage"
    )

    # TODO: some more description here?
    patient_overall_stage: Literal[
        "x",
        "0",
        "IA1",
        "IA2",
        "IA3",
        "IB",
        "IIA",
        "IIB",
        "IIIA",
        "IIIB",
        "IIIC",
        "IVA",
        "IVB",
    ] = Field(..., description="Overall stage")

    # only the year, e.g. 1995
    year_of_diagnosis: int = Field(
        ...,
        # TODO: these cutoff years just placeholders, which numbers make sense?
        ge=1890,
        le=2027,
        description="Calendar year of diagnosis (e.g. 1995)",
    )

    # days from diagnosis to death or last follow-up
    interval_diagnosis_to_last_visit_in_days: int = Field(
        ...,
        ge=0,
        description=(
            "Time interval from diagnosis date to date of death or censoring in integer number of days"
        ),
    )

    vital_status: Literal["alive", "dead"] = Field(..., description="Vital status")

    # free-text center name
    centre: str = Field(
        ...,
        min_length=1,
        description="Name of center",
    )

    # days from birth to diagnosis
    # Union: either an annotated int, or the literal string "NA"
    age_at_diagnosis: Union[
        Annotated[int, Field(..., ge=0, le=120 * 365)],
        Literal["NA"]
    ] = Field(
        ...,
        description=(
            "Time interval from birthdate to date of diagnosis in integer number of days"
        ),
    )
