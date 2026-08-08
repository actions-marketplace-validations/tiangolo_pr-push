import pytest
from pydantic import ValidationError

from pr_push.models import OIDCClaims


def test_claim_properties(claims: OIDCClaims) -> None:
    assert claims.workflow_path == ".github/workflows/pre-commit.yml"
    assert claims.pull_request_number == 123


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("event_name", "push"),
        ("ref", "refs/heads/main"),
    ],
)
def test_claims_reject_unexpected_pull_request(
    claims: OIDCClaims, field: str, value: str
) -> None:
    with pytest.raises(ValidationError):
        OIDCClaims.model_validate({**claims.model_dump(), field: value})


def test_claims_reject_workflow_repository(claims: OIDCClaims) -> None:
    invalid = claims.model_copy(update={"workflow_ref": "other/repo/x.yml@main"})
    with pytest.raises(ValueError):
        _ = invalid.workflow_path


def test_claims_reject_workflow_path(claims: OIDCClaims) -> None:
    invalid = claims.model_copy(
        update={"workflow_ref": "fastapi/fastapi/not-a-workflow@main"}
    )
    with pytest.raises(ValueError):
        _ = invalid.workflow_path
